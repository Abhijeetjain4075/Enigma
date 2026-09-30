"""Versioned API for a local transaction simulator; no real-world provider control."""

import json
import logging
import secrets
import threading
import time
import uuid
from collections import defaultdict, deque
from collections.abc import Generator
from typing import Annotated, Any

from fastapi import Depends, FastAPI, Header, HTTPException, Query, Request, Response, Security
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
from sqlalchemy import event, select, text
from sqlalchemy.orm import Session

from enigma.adapters import provider_registry
from enigma.database import initialize_local_schema, make_engine, make_session_factory
from enigma.models import (
    EvidenceRecord,
    LedgerEntry,
    ReconciliationRecord,
    TransactionEvent,
)
from enigma.schemas import (
    ErrorBody,
    LifecycleEnvelope,
    RefundCreate,
    RefundEnvelope,
    StartEnvelope,
    TransactionCreate,
    TransactionEnvelope,
    TransactionList,
)
from enigma.service import (
    ServiceError,
    _reconciliation_dict,
    create_refund,
    create_transaction,
    event_dict,
    evidence_dict,
    get_transaction,
    ledger_dict,
    list_transactions,
    reconcile_transaction,
    stop_transaction,
    transaction_dict,
)
from enigma.settings import ConfigurationError, Settings


class ProcessLocalRateLimiter:
    """Local guardrail only; production limits belong at a shared gateway."""

    def __init__(self, limit: int = 120, period_seconds: int = 60) -> None:
        self.limit = limit
        self.period_seconds = period_seconds
        self._requests: dict[str, deque[float]] = defaultdict(deque)
        self._lock = threading.Lock()

    def allow(self, key: str) -> bool:
        with self._lock:
            now = time.monotonic()
            queue = self._requests[key]
            while queue and queue[0] <= now - self.period_seconds:
                queue.popleft()
            if len(queue) >= self.limit:
                return False
            queue.append(now)
            return True


def _correlation(request: Request) -> str:
    return getattr(request.state, "correlation_id", str(uuid.uuid4()))


def _idempotency(key: str | None) -> str:
    if key is None or not key.strip() or len(key) > 128:
        raise ServiceError(
            400, "idempotency_key_required", "Provide an Idempotency-Key of 1-128 characters."
        )
    return key.strip()


def _expected_version(if_match: str | None) -> int:
    if if_match is None:
        raise ServiceError(
            428, "if_match_required", "Provide the transaction version in the If-Match header."
        )
    value = if_match.strip().strip('"')
    if value.startswith("W/") or not value.isdigit():
        raise ServiceError(
            400,
            "if_match_invalid",
            "If-Match must be the numeric transaction version returned by Enigma.",
        )
    return int(value)


def _service_response(result: Any) -> JSONResponse:
    headers = {"Idempotency-Replayed": "true" if result.replayed else "false"}
    return JSONResponse(status_code=result.status_code, content=result.body, headers=headers)


def create_app(settings: Settings | None = None, *, database_url: str | None = None) -> FastAPI:
    config = settings or Settings.from_env()
    if database_url is not None:
        config = Settings(
            environment=config.environment,
            database_url=database_url,
            api_keys=config.api_keys,
            max_request_bytes=config.max_request_bytes,
        )
    config.validate()
    if config.environment in {"staging", "production"}:
        raise ConfigurationError(
            "No real provider adapters are available; refusing to start "
            "with simulator-only providers."
        )
    engine = make_engine(config.database_url)
    if config.environment in {"development", "test"} and config.database_url.startswith("sqlite"):
        initialize_local_schema(engine)
    session_factory = make_session_factory(engine)
    if engine.dialect.name == "postgresql":

        def set_postgres_tenant_context(
            session: Session, transaction: Any, connection: Any
        ) -> None:
            tenant_id = session.info.get("tenant_id")
            if not tenant_id:
                raise RuntimeError(
                    "PostgreSQL tenant context is required for every application transaction"
                )
            connection.execute(
                text("SELECT set_config('app.tenant_id', :tenant_id, true)"),
                {"tenant_id": tenant_id},
            )

        event.listen(session_factory, "after_begin", set_postgres_tenant_context)
    limiter = ProcessLocalRateLimiter()

    app = FastAPI(
        title="Enigma Transaction Lab API",
        summary="A simulator-only, auditable transaction orchestration laboratory.",
        description=(
            "No real providers, money, or physical equipment are contacted or controlled. "
            "Simulator evidence is not production or provider-conformance evidence."
        ),
        version="1.0.0",
        telemetry={"auto_configure": False},
        openapi_url="/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
    )
    app.state.settings = config
    app.state.engine = engine
    app.state.session_factory = session_factory
    app.state.rate_limiter = limiter

    @app.middleware("http")
    async def request_controls(request: Request, call_next: Any) -> Response:
        started_at = time.perf_counter()
        request_id = str(uuid.uuid4())
        supplied_correlation = request.headers.get("X-Correlation-ID", "")
        try:
            correlation_id = (
                str(uuid.UUID(supplied_correlation)) if supplied_correlation else request_id
            )
        except (ValueError, AttributeError):
            correlation_id = request_id
        request.state.request_id = request_id
        request.state.correlation_id = correlation_id
        request.state.tenant_id = None
        content_length = request.headers.get("content-length")
        if (
            content_length
            and content_length.isdigit()
            and int(content_length) > config.max_request_bytes
        ):
            response = JSONResponse(
                status_code=413,
                content={
                    "error_code": "request_too_large",
                    "message": "Request body exceeds the configured limit.",
                    "retryable": False,
                    "correlation_id": correlation_id,
                },
            )
        elif request.url.path.startswith("/v1/") and not limiter.allow(
            request.client.host if request.client else "unknown"
        ):
            response = JSONResponse(
                status_code=429,
                content={
                    "error_code": "rate_limited",
                    "message": "Local request rate limit exceeded.",
                    "retryable": True,
                    "correlation_id": correlation_id,
                },
                headers={"Retry-After": "60"},
            )
        else:
            response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Correlation-ID"] = correlation_id
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Cache-Control"] = "no-store"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["X-Frame-Options"] = "DENY"
        route = request.scope.get("route")
        logging.getLogger("enigma.request").info(
            json.dumps(
                {
                    "event": "http_request_complete",
                    "request_id": request_id,
                    "correlation_id": correlation_id,
                    "tenant_id": getattr(request.state, "tenant_id", None),
                    "method": request.method,
                    "route": getattr(route, "path", "unmatched"),
                    "status_code": response.status_code,
                    "duration_ms": round((time.perf_counter() - started_at) * 1000, 3),
                },
                separators=(",", ":"),
            )
        )
        return response

    def tenant_for_key(raw_key: str | None) -> str:
        if not raw_key:
            raise ServiceError(401, "unauthorized", "A valid tenant API key is required.")
        tenant_id: str | None = None
        for configured_key, configured_tenant in config.api_keys.items():
            if secrets.compare_digest(raw_key.encode(), configured_key.encode()):
                tenant_id = configured_tenant
        if tenant_id is None:
            raise ServiceError(401, "unauthorized", "A valid tenant API key is required.")
        return tenant_id

    def db_session(request: Request) -> Generator[Session, None, None]:
        tenant_id = tenant_for_key(request.headers.get("x-api-key"))
        request.state.tenant_id = tenant_id
        with session_factory() as session:
            session.info["tenant_id"] = tenant_id
            try:
                yield session
            except Exception:
                session.rollback()
                raise

    api_key_scheme = APIKeyHeader(name="X-API-Key", auto_error=False)

    def authenticate(
        request: Request,
        x_api_key: Annotated[str | None, Security(api_key_scheme)] = None,
    ) -> str:
        tenant = tenant_for_key(x_api_key)
        request.state.tenant_id = tenant
        return tenant

    Db = Annotated[Session, Depends(db_session)]
    Tenant = Annotated[str, Depends(authenticate)]

    @app.exception_handler(ServiceError)
    async def service_error_handler(request: Request, exc: ServiceError) -> JSONResponse:
        body = ErrorBody(
            error_code=exc.error_code,
            message=exc.message,
            retryable=exc.retryable,
            correlation_id=_correlation(request),
            remediation_hint=exc.remediation_hint,
            transaction_id=exc.transaction_id,
        ).model_dump(exclude_none=True)
        return JSONResponse(status_code=exc.status_code, content=body)

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        # Do not echo rejected inputs: they may contain identifiers or other customer data.
        issues = [
            {
                "path": ".".join(str(part) for part in item.get("loc", ())),
                "code": item.get("type", "invalid"),
            }
            for item in exc.errors()
        ]
        return JSONResponse(
            status_code=422,
            content={
                "error_code": "request_validation_failed",
                "message": "Request did not satisfy the API contract.",
                "retryable": False,
                "correlation_id": _correlation(request),
                "issues": issues,
            },
        )

    @app.exception_handler(ConfigurationError)
    async def configuration_error_handler(
        request: Request, exc: ConfigurationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={
                "error_code": "configuration_error",
                "message": str(exc),
                "correlation_id": _correlation(request),
            },
        )

    @app.get("/health/live", tags=["health"], include_in_schema=False)
    def liveness() -> dict[str, str]:
        return {"status": "alive"}

    @app.get("/health/ready", tags=["health"], include_in_schema=False)
    def readiness() -> dict[str, str]:
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return {"status": "ready", "database": "reachable"}
        except Exception as exc:
            raise HTTPException(status_code=503, detail="database unavailable") from exc

    @app.get("/v1/providers", tags=["providers"])
    def providers(_: Tenant) -> dict[str, Any]:
        items = []
        for provider_id, adapter in provider_registry().items():
            items.append(
                {
                    "provider_id": provider_id,
                    "display_name": "Deterministic Simulator A"
                    if provider_id == "simulator-a"
                    else "Failure-Injection Simulator B",
                    "mode": "simulator_only",
                    "real_provider_connected": False,
                    "health": adapter.health_check(),
                    "supported_scenarios": [
                        "normal" if provider_id == "simulator-a" else "normal",
                        *(
                            [
                                "delayed_webhook",
                                "duplicate_event",
                                "cdr_mismatch",
                                "refund_failure",
                                "provider_outage",
                                "stale_availability",
                            ]
                            if provider_id == "simulator-b"
                            else []
                        ),
                    ],
                    "capabilities": [
                        {
                            "operation": cap.operation,
                            "state": cap.state,
                            "protocol": cap.protocol,
                            "protocol_version": cap.protocol_version,
                            "evidence_level": cap.evidence_level,
                            "observed_at": cap.observed_at.isoformat(),
                            "expires_at": cap.expires_at.isoformat() if cap.expires_at else None,
                            "source": cap.source,
                        }
                        for cap in adapter.get_capabilities("normal")
                    ],
                    "unsupported_or_external": [
                        "real_provider_api",
                        "real_payment",
                        "real_settlement",
                        "physical_charger_control",
                    ],
                }
            )
        return {
            "items": items,
            "count": len(items),
            "data_source": "local deterministic simulators",
        }

    @app.get("/v1/transactions", tags=["transactions"], response_model=TransactionList)
    def transactions(
        tenant: Tenant,
        db: Db,
        limit: int = Query(50, ge=1, le=100),
        offset: int = Query(0, ge=0, le=1_000_000),
    ) -> dict[str, Any]:
        records = list_transactions(db, tenant, limit, offset)
        return {
            "items": [transaction_dict(item) for item in records],
            "limit": limit,
            "offset": offset,
            "count": len(records),
        }

    @app.post(
        "/v1/transactions",
        tags=["transactions"],
        status_code=201,
        response_model=StartEnvelope,
        responses={409: {"model": StartEnvelope}, 502: {"model": StartEnvelope}},
    )
    def create_transaction_route(
        body: TransactionCreate,
        request: Request,
        db: Db,
        tenant: Tenant,
        idempotency_key: Annotated[str | None, Header(alias="Idempotency-Key")] = None,
    ) -> Any:
        result = create_transaction(
            db,
            tenant_id=tenant,
            key=_idempotency(idempotency_key),
            request_body=body.model_dump(),
            correlation_id=_correlation(request),
        )
        return _service_response(result)

    @app.get(
        "/v1/transactions/{transaction_id}",
        tags=["transactions"],
        response_model=TransactionEnvelope,
    )
    def transaction_detail(transaction_id: str, tenant: Tenant, db: Db) -> dict[str, Any]:
        return {"transaction": transaction_dict(get_transaction(db, tenant, transaction_id))}

    @app.post(
        "/v1/transactions/{transaction_id}/stop",
        tags=["transactions"],
        response_model=LifecycleEnvelope,
    )
    def stop_transaction_route(
        transaction_id: str,
        request: Request,
        db: Db,
        tenant: Tenant,
        idempotency_key: Annotated[str | None, Header(alias="Idempotency-Key")] = None,
        if_match: Annotated[str | None, Header(alias="If-Match")] = None,
    ) -> Any:
        result = stop_transaction(
            db,
            tenant_id=tenant,
            transaction_id=transaction_id,
            key=_idempotency(idempotency_key),
            expected_version=_expected_version(if_match),
            correlation_id=_correlation(request),
        )
        return _service_response(result)

    @app.post(
        "/v1/transactions/{transaction_id}/reconcile",
        tags=["reconciliation"],
        response_model=LifecycleEnvelope,
    )
    def reconcile_route(
        transaction_id: str,
        db: Db,
        tenant: Tenant,
        idempotency_key: Annotated[str | None, Header(alias="Idempotency-Key")] = None,
        if_match: Annotated[str | None, Header(alias="If-Match")] = None,
    ) -> Any:
        result = reconcile_transaction(
            db,
            tenant_id=tenant,
            transaction_id=transaction_id,
            key=_idempotency(idempotency_key),
            expected_version=_expected_version(if_match),
        )
        return _service_response(result)

    @app.post(
        "/v1/transactions/{transaction_id}/refunds",
        tags=["transactions"],
        response_model=RefundEnvelope,
        responses={502: {"model": StartEnvelope}},
    )
    def refund_route(
        transaction_id: str,
        body: RefundCreate,
        db: Db,
        tenant: Tenant,
        idempotency_key: Annotated[str | None, Header(alias="Idempotency-Key")] = None,
        if_match: Annotated[str | None, Header(alias="If-Match")] = None,
    ) -> Any:
        result = create_refund(
            db,
            tenant_id=tenant,
            transaction_id=transaction_id,
            key=_idempotency(idempotency_key),
            expected_version=_expected_version(if_match),
            request_body=body.model_dump(),
        )
        return _service_response(result)

    @app.get("/v1/transactions/{transaction_id}/events", tags=["evidence"])
    def transaction_events(transaction_id: str, tenant: Tenant, db: Db) -> dict[str, Any]:
        get_transaction(db, tenant, transaction_id)
        items = list(
            db.scalars(
                select(TransactionEvent)
                .where(
                    TransactionEvent.tenant_id == tenant,
                    TransactionEvent.aggregate_id == transaction_id,
                )
                .order_by(TransactionEvent.event_version)
            )
        )
        return {"items": [event_dict(item) for item in items], "count": len(items)}

    @app.get("/v1/transactions/{transaction_id}/evidence", tags=["evidence"])
    def transaction_evidence(transaction_id: str, tenant: Tenant, db: Db) -> dict[str, Any]:
        get_transaction(db, tenant, transaction_id)
        items = list(
            db.scalars(
                select(EvidenceRecord)
                .where(
                    EvidenceRecord.tenant_id == tenant,
                    EvidenceRecord.transaction_id == transaction_id,
                )
                .order_by(EvidenceRecord.received_at, EvidenceRecord.evidence_id)
            )
        )
        return {"items": [evidence_dict(item) for item in items], "count": len(items)}

    @app.get("/v1/transactions/{transaction_id}/reconciliation", tags=["reconciliation"])
    def transaction_reconciliation(transaction_id: str, tenant: Tenant, db: Db) -> dict[str, Any]:
        get_transaction(db, tenant, transaction_id)
        record = db.scalar(
            select(ReconciliationRecord).where(
                ReconciliationRecord.tenant_id == tenant,
                ReconciliationRecord.transaction_id == transaction_id,
            )
        )
        if record is None:
            raise ServiceError(
                404,
                "reconciliation_not_found",
                "No reconciliation record exists yet.",
                transaction_id=transaction_id,
            )
        return {"reconciliation": _reconciliation_dict(record)}

    @app.get("/v1/transactions/{transaction_id}/ledger", tags=["ledger"])
    def transaction_ledger(transaction_id: str, tenant: Tenant, db: Db) -> dict[str, Any]:
        get_transaction(db, tenant, transaction_id)
        items = list(
            db.scalars(
                select(LedgerEntry)
                .where(
                    LedgerEntry.tenant_id == tenant, LedgerEntry.transaction_id == transaction_id
                )
                .order_by(LedgerEntry.created_at, LedgerEntry.entry_id)
            )
        )
        total = sum(item.amount_minor for item in items)
        return {
            "items": [ledger_dict(item) for item in items],
            "count": len(items),
            "sum_by_single_transaction_currency_minor": total,
            "balanced": total == 0,
            "simulation_only": True,
        }

    @app.get("/v1/openapi.json", include_in_schema=False)
    def versioned_openapi() -> dict[str, Any]:
        # Canonical versioned path for tooling; FastAPI's generated schema is versioned 1.0.0.
        return app.openapi()

    return app
