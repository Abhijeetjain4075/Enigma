"""Transactional application services for the local simulator laboratory only."""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, cast

from sqlalchemy import select, update
from sqlalchemy.engine import CursorResult, Result
from sqlalchemy.orm import Session

from enigma.adapters import (
    ADAPTER_VERSION,
    PROTOCOL,
    PROTOCOL_VERSION,
    TRANSFORMATION_VERSION,
    ProviderFailure,
    provider_registry,
    scenario_supported,
)
from enigma.domain import (
    TRANSITIONS,
    InvalidTransition,
    TransactionStatus,
    utc_now,
    validate_transition,
)
from enigma.models import (
    EvidenceRecord,
    IdempotencyRecord,
    LedgerEntry,
    ReconciliationRecord,
    Transaction,
    TransactionEvent,
)


@dataclass(slots=True)
class ServiceResponse:
    status_code: int
    body: dict[str, Any]
    replayed: bool = False


class ServiceError(Exception):
    def __init__(
        self,
        status_code: int,
        error_code: str,
        message: str,
        *,
        retryable: bool = False,
        remediation_hint: str | None = None,
        transaction_id: str | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
        self.retryable = retryable
        self.remediation_hint = remediation_hint
        self.transaction_id = transaction_id


def _iso_utc(value: datetime | None) -> str | None:
    if value is None:
        return None
    if value.tzinfo is None:
        value = value.replace(tzinfo=UTC)
    return value.astimezone(UTC).isoformat()


def _rowcount(result: Result[Any]) -> int:
    return cast(CursorResult[Any], result).rowcount


def _cdr_values(payload: dict[str, object]) -> tuple[int, str]:
    amount = payload.get("amount_minor")
    currency = payload.get("currency")
    if type(amount) is not int or amount <= 0 or not isinstance(currency, str):
        raise ServiceError(
            502, "provider_payload_invalid", "Provider CDR amount or currency is invalid."
        )
    return amount, currency


def canonical_hash(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def get_idempotent_response(
    session: Session, tenant_id: str, key: str, request_hash: str
) -> ServiceResponse | None:
    record = session.scalar(
        select(IdempotencyRecord).where(
            IdempotencyRecord.tenant_id == tenant_id, IdempotencyRecord.key == key
        )
    )
    if record is None:
        return None
    if record.request_hash != request_hash:
        raise ServiceError(
            409,
            "idempotency_key_reused",
            "The idempotency key was already used for a different request.",
            remediation_hint="Use a new idempotency key for a materially different operation.",
            transaction_id=record.transaction_id,
        )
    return ServiceResponse(record.response_status, dict(record.response_json), replayed=True)


def save_idempotency(
    session: Session,
    tenant_id: str,
    key: str,
    request_hash: str,
    transaction_id: str,
    response: ServiceResponse,
) -> None:
    session.add(
        IdempotencyRecord(
            tenant_id=tenant_id,
            key=key,
            request_hash=request_hash,
            transaction_id=transaction_id,
            response_status=response.status_code,
            response_json=response.body,
        )
    )
    session.flush()


def transaction_dict(transaction: Transaction) -> dict[str, Any]:
    return {
        "transaction_id": transaction.transaction_id,
        "tenant_id": transaction.tenant_id,
        "provider_id": transaction.provider_id,
        "scenario": transaction.scenario,
        "status": transaction.status,
        "reconciliation_status": transaction.reconciliation_status,
        "currency": transaction.currency,
        "expected_amount_minor": transaction.expected_amount_minor,
        "billed_amount_minor": transaction.billed_amount_minor,
        "refunded_amount_minor": transaction.refunded_amount_minor,
        "correlation_id": transaction.correlation_id,
        "version": transaction.version,
        "created_at": _iso_utc(transaction.created_at),
        "updated_at": _iso_utc(transaction.updated_at),
        "started_at": _iso_utc(transaction.started_at),
        "completed_at": _iso_utc(transaction.completed_at),
        "safety_classification": "simulated_physical_world_action; no provider is contacted",
    }


def _event(
    session: Session,
    transaction: Transaction,
    event_type: str,
    payload: dict[str, Any],
    *,
    provider_id: str | None = None,
    external_event_id: str | None = None,
    occurred_at: datetime | None = None,
) -> bool:
    if external_event_id is not None:
        exists = session.scalar(
            select(TransactionEvent.event_id).where(
                TransactionEvent.tenant_id == transaction.tenant_id,
                TransactionEvent.provider_id == provider_id,
                TransactionEvent.external_event_id == external_event_id,
            )
        )
        if exists:
            return False
    now = utc_now()
    expected_version = transaction.version
    result = session.execute(
        update(Transaction)
        .where(
            Transaction.transaction_id == transaction.transaction_id,
            Transaction.tenant_id == transaction.tenant_id,
            Transaction.version == expected_version,
        )
        .values(version=expected_version + 1, updated_at=now)
    )
    if _rowcount(result) != 1:
        raise ServiceError(
            409,
            "concurrent_update",
            "Transaction changed concurrently; retrieve current state before retrying.",
            transaction_id=transaction.transaction_id,
            remediation_hint="Fetch the transaction and retry with its current version.",
        )
    transaction.version = expected_version + 1
    transaction.updated_at = now
    session.add(
        TransactionEvent(
            event_id=str(uuid.uuid4()),
            tenant_id=transaction.tenant_id,
            aggregate_id=transaction.transaction_id,
            aggregate_type="transaction",
            event_type=event_type,
            event_version=transaction.version,
            occurred_at=occurred_at or now,
            received_at=now,
            producer="enigma-simulator",
            provider_id=provider_id,
            external_event_id=external_event_id,
            correlation_id=transaction.correlation_id,
            causation_id=None,
            schema_version="1.0",
            payload=payload,
        )
    )
    session.flush()
    return True


def _transition(
    session: Session,
    transaction: Transaction,
    target: TransactionStatus,
    event_type: str,
    payload: dict[str, Any],
    *,
    provider_id: str | None = None,
    external_event_id: str | None = None,
    occurred_at: datetime | None = None,
) -> None:
    current = TransactionStatus(transaction.status)
    try:
        validate_transition(current, target)
    except InvalidTransition as exc:
        raise ServiceError(
            409, "invalid_state_transition", str(exc), transaction_id=transaction.transaction_id
        ) from exc
    if external_event_id is not None:
        exists = session.scalar(
            select(TransactionEvent.event_id).where(
                TransactionEvent.tenant_id == transaction.tenant_id,
                TransactionEvent.provider_id == provider_id,
                TransactionEvent.external_event_id == external_event_id,
            )
        )
        if exists:
            return
    expected_version = transaction.version
    now = utc_now()
    result = session.execute(
        update(Transaction)
        .where(
            Transaction.transaction_id == transaction.transaction_id,
            Transaction.tenant_id == transaction.tenant_id,
            Transaction.version == expected_version,
        )
        .values(status=target.value, version=expected_version + 1, updated_at=now)
    )
    if _rowcount(result) != 1:
        raise ServiceError(
            409,
            "concurrent_update",
            "Transaction changed concurrently; retrieve current state before retrying.",
            transaction_id=transaction.transaction_id,
        )
    transaction.status = target.value
    transaction.version = expected_version + 1
    transaction.updated_at = now
    session.add(
        TransactionEvent(
            event_id=str(uuid.uuid4()),
            tenant_id=transaction.tenant_id,
            aggregate_id=transaction.transaction_id,
            aggregate_type="transaction",
            event_type=event_type,
            event_version=transaction.version,
            occurred_at=occurred_at or now,
            received_at=now,
            producer="enigma-simulator",
            provider_id=provider_id,
            external_event_id=external_event_id,
            correlation_id=transaction.correlation_id,
            causation_id=None,
            schema_version="1.0",
            payload={"from": current.value, "to": target.value, **payload},
        )
    )
    session.flush()


def _evidence(
    session: Session,
    transaction: Transaction,
    *,
    source: str,
    external_id: str,
    observed_at: datetime,
    payload: dict[str, Any],
    conflict_status: str = "none",
    confidence: float = 1.0,
) -> str:
    evidence_id = str(uuid.uuid4())
    session.add(
        EvidenceRecord(
            evidence_id=evidence_id,
            tenant_id=transaction.tenant_id,
            transaction_id=transaction.transaction_id,
            source=source,
            provider_id=transaction.provider_id,
            namespace=f"simulator:{transaction.provider_id}",
            external_id=external_id,
            observed_at=observed_at,
            received_at=utc_now(),
            expires_at=None,
            protocol=PROTOCOL,
            protocol_version=PROTOCOL_VERSION,
            retrieval_method="deterministic-simulator-response",
            adapter_version=ADAPTER_VERSION,
            transformation_version=TRANSFORMATION_VERSION,
            confidence=confidence,
            conflict_status=conflict_status,
            evidence_level="E4-simulated",
            raw_reference=f"simulated://{transaction.provider_id}/{external_id}",
            normalized_payload=payload,
        )
    )
    session.flush()
    return evidence_id


def _post_simulated_ledger(
    session: Session,
    transaction: Transaction,
    amount_minor: int,
    reference: str,
    *,
    refund: bool = False,
) -> None:
    """Create balanced, immutable, explicitly simulated ledger entries; never moves funds."""
    magnitude = -amount_minor if refund else amount_minor
    session.add_all(
        [
            LedgerEntry(
                entry_id=str(uuid.uuid4()),
                tenant_id=transaction.tenant_id,
                transaction_id=transaction.transaction_id,
                account="provider_payable",
                entry_type="refund" if refund else "service_charge_expected",
                amount_minor=magnitude,
                currency=transaction.currency,
                reference=reference,
                simulation_only=True,
            ),
            LedgerEntry(
                entry_id=str(uuid.uuid4()),
                tenant_id=transaction.tenant_id,
                transaction_id=transaction.transaction_id,
                account="service_revenue_offset",
                entry_type="refund" if refund else "service_charge_expected",
                amount_minor=-magnitude,
                currency=transaction.currency,
                reference=reference,
                simulation_only=True,
            ),
        ]
    )
    session.flush()


def _set_reconciliation(
    session: Session,
    transaction: Transaction,
    *,
    status: str,
    observed_amount: int | None,
    reason_codes: list[str],
    evidence_ids: list[str],
) -> ReconciliationRecord:
    transaction.reconciliation_status = status
    record = session.scalar(
        select(ReconciliationRecord).where(
            ReconciliationRecord.tenant_id == transaction.tenant_id,
            ReconciliationRecord.transaction_id == transaction.transaction_id,
        )
    )
    if record is None:
        record = ReconciliationRecord(
            reconciliation_id=str(uuid.uuid4()),
            tenant_id=transaction.tenant_id,
            transaction_id=transaction.transaction_id,
            status=status,
            expected_amount_minor=transaction.expected_amount_minor,
            observed_amount_minor=observed_amount,
            currency=transaction.currency,
            difference_minor=(
                observed_amount - transaction.expected_amount_minor
                if observed_amount is not None
                else None
            ),
            reason_codes=reason_codes,
            evidence_ids=evidence_ids,
            owner="operations-unassigned",
        )
        session.add(record)
    else:
        record.status = status
        record.observed_amount_minor = observed_amount
        record.difference_minor = (
            observed_amount - transaction.expected_amount_minor
            if observed_amount is not None
            else None
        )
        record.reason_codes = reason_codes
        record.evidence_ids = list(dict.fromkeys(record.evidence_ids + evidence_ids))
        record.resolution = None
        record.resolved_at = None
    session.flush()
    return record


def _reconciliation_dict(record: ReconciliationRecord) -> dict[str, Any]:
    return {
        "reconciliation_id": record.reconciliation_id,
        "transaction_id": record.transaction_id,
        "status": record.status,
        "expected_amount_minor": record.expected_amount_minor,
        "observed_amount_minor": record.observed_amount_minor,
        "currency": record.currency,
        "difference_minor": record.difference_minor,
        "reason_codes": record.reason_codes,
        "evidence_ids": record.evidence_ids,
        "owner": record.owner,
        "resolution": record.resolution,
    }


def _save_response(
    session: Session,
    tenant_id: str,
    key: str,
    request_hash: str,
    transaction: Transaction,
    status_code: int,
    body: dict[str, Any],
) -> ServiceResponse:
    response = ServiceResponse(status_code, body)
    save_idempotency(session, tenant_id, key, request_hash, transaction.transaction_id, response)
    session.commit()
    return response


def create_transaction(
    session: Session,
    *,
    tenant_id: str,
    key: str,
    request_body: dict[str, Any],
    correlation_id: str,
) -> ServiceResponse:
    request_hash = canonical_hash({"operation": "create", "body": request_body})
    replay = get_idempotent_response(session, tenant_id, key, request_hash)
    if replay:
        return replay
    provider_id = str(request_body["provider_id"])
    scenario = str(request_body["scenario"])
    if not scenario_supported(provider_id, scenario):
        raise ServiceError(
            422,
            "scenario_not_supported",
            "This simulator scenario is not supported by that provider.",
        )
    adapter = provider_registry()[provider_id]
    body: dict[str, Any]
    transaction = Transaction(
        transaction_id=str(uuid.uuid4()),
        tenant_id=tenant_id,
        provider_id=provider_id,
        scenario=scenario,
        status=TransactionStatus.CREATED.value,
        reconciliation_status="pending",
        currency=str(request_body["currency"]),
        expected_amount_minor=int(request_body["expected_amount_minor"]),
        billed_amount_minor=None,
        refunded_amount_minor=0,
        correlation_id=correlation_id,
        version=1,
        created_at=utc_now(),
        updated_at=utc_now(),
    )
    session.add(transaction)
    session.flush()
    now = utc_now()
    session.add(
        TransactionEvent(
            event_id=str(uuid.uuid4()),
            tenant_id=tenant_id,
            aggregate_id=transaction.transaction_id,
            aggregate_type="transaction",
            event_type="transaction.created",
            event_version=1,
            occurred_at=now,
            received_at=now,
            producer="enigma-simulator",
            provider_id=None,
            external_event_id=None,
            correlation_id=correlation_id,
            causation_id=None,
            schema_version="1.0",
            payload={"status": "created", "simulation_only": True},
        )
    )
    session.flush()
    capability = next(
        c for c in adapter.get_capabilities(scenario) if c.operation == "availability"
    )
    if capability.state == "stale":
        evidence_id = _evidence(
            session,
            transaction,
            source="simulated_capability",
            external_id="availability:stale",
            observed_at=capability.observed_at,
            payload={"state": "stale", "expires_at": _iso_utc(capability.expires_at)},
            conflict_status="stale",
        )
        _transition(
            session,
            transaction,
            TransactionStatus.VALIDATED,
            "transaction.validated",
            {"capability_check": "passed with stale availability recorded"},
        )
        _transition(
            session,
            transaction,
            TransactionStatus.REJECTED,
            "transaction.rejected",
            {"reason_code": "stale_availability", "evidence_id": evidence_id},
        )
        body = {"transaction": transaction_dict(transaction), "error_code": "stale_availability"}
        return _save_response(session, tenant_id, key, request_hash, transaction, 409, body)
    _transition(
        session,
        transaction,
        TransactionStatus.VALIDATED,
        "transaction.validated",
        {
            "provider_capability": "simulated_supported",
            "protocol": PROTOCOL,
            "protocol_version": PROTOCOL_VERSION,
        },
    )
    try:
        auth_result = adapter.authorize(transaction.transaction_id, scenario)
        auth_evidence = _evidence(
            session,
            transaction,
            source="provider_simulator",
            external_id=auth_result.external_id,
            observed_at=auth_result.observed_at,
            payload=auth_result.payload,
        )
        _transition(
            session,
            transaction,
            TransactionStatus.AUTHORIZED,
            "provider.authorization.accepted",
            {"evidence_id": auth_evidence},
            provider_id=provider_id,
            external_event_id=auth_result.external_id,
            occurred_at=auth_result.observed_at,
        )
        _transition(
            session,
            transaction,
            TransactionStatus.INITIATED,
            "transaction.initiated",
            {"safety_classification": "simulated_physical_world_action"},
        )
        start_result = adapter.start(transaction.transaction_id, scenario)
        start_evidence = _evidence(
            session,
            transaction,
            source="provider_simulator",
            external_id=start_result.external_id,
            observed_at=start_result.observed_at,
            payload=start_result.payload,
        )
        transaction.started_at = start_result.observed_at
        _transition(
            session,
            transaction,
            TransactionStatus.ACTIVE,
            "provider.session.started",
            {"evidence_id": start_evidence, "state": "active"},
            provider_id=provider_id,
            external_event_id=start_result.external_id,
            occurred_at=start_result.observed_at,
        )
        body = {"transaction": transaction_dict(transaction)}
        return _save_response(session, tenant_id, key, request_hash, transaction, 201, body)
    except ProviderFailure as exc:
        evidence_id = _evidence(
            session,
            transaction,
            source="provider_simulator_error",
            external_id=f"error:{uuid.uuid4()}",
            observed_at=utc_now(),
            payload={"error_code": exc.code, "retryable": exc.retryable},
            conflict_status="provider_error",
        )
        if TransactionStatus.FAILED in TRANSITIONS[TransactionStatus(transaction.status)]:
            _transition(
                session,
                transaction,
                TransactionStatus.FAILED,
                "provider.operation.failed",
                {"error_code": exc.code, "evidence_id": evidence_id},
                provider_id=provider_id,
            )
        body = {
            "transaction": transaction_dict(transaction),
            "error_code": exc.code,
            "message": str(exc),
            "retryable": exc.retryable,
        }
        return _save_response(session, tenant_id, key, request_hash, transaction, 502, body)


def get_transaction(session: Session, tenant_id: str, transaction_id: str) -> Transaction:
    transaction = session.scalar(
        select(Transaction).where(
            Transaction.tenant_id == tenant_id, Transaction.transaction_id == transaction_id
        )
    )
    if transaction is None:
        raise ServiceError(404, "transaction_not_found", "Transaction was not found.")
    return transaction


def list_transactions(
    session: Session, tenant_id: str, limit: int, offset: int
) -> list[Transaction]:
    return list(
        session.scalars(
            select(Transaction)
            .where(Transaction.tenant_id == tenant_id)
            .order_by(Transaction.created_at.desc(), Transaction.transaction_id)
            .limit(limit)
            .offset(offset)
        )
    )


def stop_transaction(
    session: Session,
    *,
    tenant_id: str,
    transaction_id: str,
    key: str,
    expected_version: int,
    correlation_id: str,
) -> ServiceResponse:
    request_hash = canonical_hash(
        {
            "operation": "stop",
            "transaction_id": transaction_id,
            "expected_version": expected_version,
        }
    )
    replay = get_idempotent_response(session, tenant_id, key, request_hash)
    if replay:
        return replay
    transaction = get_transaction(session, tenant_id, transaction_id)
    if transaction.version != expected_version:
        raise ServiceError(
            409,
            "version_conflict",
            "The transaction version does not match If-Match.",
            transaction_id=transaction_id,
            remediation_hint="Fetch the resource and retry using its current version.",
        )
    if transaction.status != TransactionStatus.ACTIVE.value:
        raise ServiceError(
            409,
            "invalid_state_transition",
            "Only an active simulator transaction can be stopped.",
            transaction_id=transaction_id,
        )
    adapter = provider_registry()[transaction.provider_id]
    try:
        stop_result = adapter.stop(
            transaction.transaction_id, transaction.scenario, transaction.expected_amount_minor
        )
        stop_evidence = _evidence(
            session,
            transaction,
            source="provider_simulator",
            external_id=stop_result.external_id,
            observed_at=stop_result.observed_at,
            payload=stop_result.payload,
        )
        transaction.completed_at = stop_result.observed_at
        _transition(
            session,
            transaction,
            TransactionStatus.COMPLETED,
            "provider.session.stopped",
            {"evidence_id": stop_evidence},
            provider_id=transaction.provider_id,
            external_event_id=stop_result.external_id,
            occurred_at=stop_result.observed_at,
        )
        try:
            cdr = adapter.get_cdr(
                transaction.transaction_id,
                transaction.scenario,
                transaction.expected_amount_minor,
                transaction.currency,
            )
        except ProviderFailure as exc:
            missing_id = _evidence(
                session,
                transaction,
                source="provider_simulator_error",
                external_id=f"cdr-missing:{uuid.uuid4()}",
                observed_at=utc_now(),
                payload={"error_code": exc.code, "retryable": exc.retryable},
                conflict_status="missing",
            )
            _transition(
                session,
                transaction,
                TransactionStatus.RECONCILIATION_REQUIRED,
                "reconciliation.cdr_missing",
                {"reason_code": "cdr_missing", "evidence_id": missing_id},
            )
            record = _set_reconciliation(
                session,
                transaction,
                status="unresolved",
                observed_amount=None,
                reason_codes=["cdr_missing"],
                evidence_ids=[missing_id],
            )
            body = {
                "transaction": transaction_dict(transaction),
                "reconciliation": _reconciliation_dict(record),
            }
            return _save_response(session, tenant_id, key, request_hash, transaction, 202, body)
        cdr_evidence = _evidence(
            session,
            transaction,
            source="provider_cdr",
            external_id=cdr.external_id,
            observed_at=cdr.observed_at,
            payload=cdr.payload,
            conflict_status=(
                "mismatch"
                if cdr.payload["amount_minor"] != transaction.expected_amount_minor
                or cdr.payload["currency"] != transaction.currency
                else "none"
            ),
        )
        observed_amount, observed_currency = _cdr_values(cdr.payload)
        matches = (
            observed_amount == transaction.expected_amount_minor
            and observed_currency == transaction.currency
        )
        target = TransactionStatus.BILLED if matches else TransactionStatus.RECONCILIATION_REQUIRED
        _transition(
            session,
            transaction,
            target,
            "provider.cdr.received" if matches else "reconciliation.cdr_mismatch",
            {
                "evidence_id": cdr_evidence,
                "observed_amount_minor": observed_amount,
                "observed_currency": observed_currency,
            },
            provider_id=transaction.provider_id,
            external_event_id=cdr.external_id,
            occurred_at=cdr.observed_at,
        )
        if transaction.scenario == "duplicate_event":
            _event(
                session,
                transaction,
                "provider.cdr.duplicate_suppressed",
                {"external_event_id": cdr.external_id, "deduplicated": True},
                provider_id=transaction.provider_id,
                external_event_id=cdr.external_id,
            )
        if matches:
            transaction.billed_amount_minor = observed_amount
            _post_simulated_ledger(session, transaction, observed_amount, cdr.external_id)
            transaction.reconciliation_status = "matched"
            record = _set_reconciliation(
                session,
                transaction,
                status="matched",
                observed_amount=observed_amount,
                reason_codes=[],
                evidence_ids=[cdr_evidence],
            )
            status_code = 200
        else:
            record = _set_reconciliation(
                session,
                transaction,
                status="unresolved",
                observed_amount=observed_amount,
                reason_codes=[
                    "amount_mismatch"
                    if observed_amount != transaction.expected_amount_minor
                    else "currency_mismatch"
                ],
                evidence_ids=[cdr_evidence],
            )
            status_code = 202
        body = {
            "transaction": transaction_dict(transaction),
            "reconciliation": _reconciliation_dict(record),
        }
        return _save_response(session, tenant_id, key, request_hash, transaction, status_code, body)
    except ProviderFailure as exc:
        raise ServiceError(
            502,
            exc.code,
            str(exc),
            retryable=exc.retryable,
            transaction_id=transaction_id,
            remediation_hint=(
                "Inspect current provider evidence before retrying a physical-world command."
            ),
        ) from exc


def reconcile_transaction(
    session: Session,
    *,
    tenant_id: str,
    transaction_id: str,
    key: str,
    expected_version: int,
) -> ServiceResponse:
    request_hash = canonical_hash(
        {
            "operation": "reconcile",
            "transaction_id": transaction_id,
            "expected_version": expected_version,
        }
    )
    replay = get_idempotent_response(session, tenant_id, key, request_hash)
    if replay:
        return replay
    transaction = get_transaction(session, tenant_id, transaction_id)
    if transaction.version != expected_version:
        raise ServiceError(
            409,
            "version_conflict",
            "The transaction version does not match If-Match.",
            transaction_id=transaction_id,
        )
    existing = session.scalar(
        select(ReconciliationRecord).where(
            ReconciliationRecord.tenant_id == tenant_id,
            ReconciliationRecord.transaction_id == transaction_id,
        )
    )
    if existing is None:
        raise ServiceError(
            409,
            "reconciliation_not_available",
            "No reconciliation result exists yet.",
            transaction_id=transaction_id,
        )
    if existing.status == "matched":
        response = ServiceResponse(
            200,
            {
                "transaction": transaction_dict(transaction),
                "reconciliation": _reconciliation_dict(existing),
            },
        )
        return _save_response(
            session, tenant_id, key, request_hash, transaction, 200, response.body
        )
    if "cdr_missing" in existing.reason_codes and transaction.scenario == "delayed_webhook":
        adapter = provider_registry()[transaction.provider_id]
        cdr = adapter.get_cdr(
            transaction.transaction_id,
            "normal",
            transaction.expected_amount_minor,
            transaction.currency,
        )
        evidence_id = _evidence(
            session,
            transaction,
            source="provider_cdr_replay",
            external_id=cdr.external_id,
            observed_at=cdr.observed_at,
            payload=cdr.payload,
        )
        _transition(
            session,
            transaction,
            TransactionStatus.BILLED,
            "reconciliation.cdr_recovered",
            {"evidence_id": evidence_id},
            provider_id=transaction.provider_id,
            external_event_id=cdr.external_id,
            occurred_at=cdr.observed_at,
        )
        recovered_amount, _ = _cdr_values(cdr.payload)
        transaction.billed_amount_minor = recovered_amount
        _post_simulated_ledger(
            session, transaction, transaction.billed_amount_minor, cdr.external_id
        )
        record = _set_reconciliation(
            session,
            transaction,
            status="matched",
            observed_amount=transaction.billed_amount_minor,
            reason_codes=[],
            evidence_ids=[evidence_id],
        )
        response = ServiceResponse(
            200,
            {
                "transaction": transaction_dict(transaction),
                "reconciliation": _reconciliation_dict(record),
            },
        )
        return _save_response(
            session, tenant_id, key, request_hash, transaction, 200, response.body
        )
    response = ServiceResponse(
        200,
        {
            "transaction": transaction_dict(transaction),
            "reconciliation": _reconciliation_dict(existing),
            "action_required": "manual_review",
            "automatically_resolved": False,
        },
    )
    return _save_response(session, tenant_id, key, request_hash, transaction, 200, response.body)


def create_refund(
    session: Session,
    *,
    tenant_id: str,
    transaction_id: str,
    key: str,
    expected_version: int,
    request_body: dict[str, Any],
) -> ServiceResponse:
    request_hash = canonical_hash(
        {
            "operation": "refund",
            "transaction_id": transaction_id,
            "expected_version": expected_version,
            "body": request_body,
        }
    )
    replay = get_idempotent_response(session, tenant_id, key, request_hash)
    if replay:
        return replay
    transaction = get_transaction(session, tenant_id, transaction_id)
    if transaction.version != expected_version:
        raise ServiceError(
            409,
            "version_conflict",
            "The transaction version does not match If-Match.",
            transaction_id=transaction_id,
        )
    if (
        transaction.status
        not in {
            TransactionStatus.BILLED.value,
            TransactionStatus.SETTLED.value,
            TransactionStatus.PARTIALLY_REFUNDED.value,
        }
        or transaction.billed_amount_minor is None
    ):
        raise ServiceError(
            409,
            "refund_not_available",
            "Only a billed simulated transaction can be refunded.",
            transaction_id=transaction_id,
        )
    amount_minor = request_body.get("amount_minor")
    if amount_minor is None:
        amount_minor = transaction.billed_amount_minor - transaction.refunded_amount_minor
    amount_minor = int(amount_minor)
    refundable = transaction.billed_amount_minor - transaction.refunded_amount_minor
    if amount_minor <= 0 or amount_minor > refundable:
        raise ServiceError(
            422,
            "refund_amount_invalid",
            "Refund must be positive and no greater than the remaining billed amount.",
            transaction_id=transaction_id,
        )
    adapter = provider_registry()[transaction.provider_id]
    try:
        result = adapter.refund(transaction_id, transaction.scenario, amount_minor)
    except ProviderFailure as exc:
        evidence_id = _evidence(
            session,
            transaction,
            source="provider_refund_error",
            external_id=f"refund-error:{uuid.uuid4()}",
            observed_at=utc_now(),
            payload={"error_code": exc.code},
            conflict_status="provider_error",
        )
        _event(
            session,
            transaction,
            "provider.refund.failed",
            {"error_code": exc.code, "evidence_id": evidence_id},
            provider_id=transaction.provider_id,
        )
        response = ServiceResponse(
            502,
            {
                "error_code": exc.code,
                "message": str(exc),
                "retryable": exc.retryable,
                "transaction": transaction_dict(transaction),
            },
        )
        return _save_response(
            session, tenant_id, key, request_hash, transaction, 502, response.body
        )
    evidence_id = _evidence(
        session,
        transaction,
        source="provider_refund",
        external_id=result.external_id,
        observed_at=result.observed_at,
        payload=result.payload,
    )
    new_refunded = transaction.refunded_amount_minor + amount_minor
    target = (
        TransactionStatus.REFUNDED
        if new_refunded == transaction.billed_amount_minor
        else TransactionStatus.PARTIALLY_REFUNDED
    )
    _transition(
        session,
        transaction,
        target,
        "provider.refund.accepted",
        {"amount_minor": amount_minor, "evidence_id": evidence_id},
        provider_id=transaction.provider_id,
        external_event_id=result.external_id,
        occurred_at=result.observed_at,
    )
    transaction.refunded_amount_minor = new_refunded
    _post_simulated_ledger(session, transaction, amount_minor, result.external_id, refund=True)
    body = {
        "transaction": transaction_dict(transaction),
        "refund": {"amount_minor": amount_minor, "status": "simulated_accepted"},
    }
    return _save_response(session, tenant_id, key, request_hash, transaction, 200, body)


def evidence_dict(item: EvidenceRecord) -> dict[str, Any]:
    return {
        "evidence_id": item.evidence_id,
        "transaction_id": item.transaction_id,
        "source": item.source,
        "provider_id": item.provider_id,
        "namespace": item.namespace,
        "external_id": item.external_id,
        "observed_at": _iso_utc(item.observed_at),
        "received_at": _iso_utc(item.received_at),
        "expires_at": _iso_utc(item.expires_at),
        "protocol": item.protocol,
        "protocol_version": item.protocol_version,
        "retrieval_method": item.retrieval_method,
        "adapter_version": item.adapter_version,
        "transformation_version": item.transformation_version,
        "confidence": item.confidence,
        "conflict_status": item.conflict_status,
        "evidence_level": item.evidence_level,
        "raw_reference": item.raw_reference,
        "normalized_payload": item.normalized_payload,
    }


def event_dict(item: TransactionEvent) -> dict[str, Any]:
    return {
        "event_id": item.event_id,
        "aggregate_id": item.aggregate_id,
        "aggregate_type": item.aggregate_type,
        "event_type": item.event_type,
        "event_version": item.event_version,
        "occurred_at": _iso_utc(item.occurred_at),
        "received_at": _iso_utc(item.received_at),
        "producer": item.producer,
        "provider_id": item.provider_id,
        "external_event_id": item.external_event_id,
        "correlation_id": item.correlation_id,
        "causation_id": item.causation_id,
        "schema_version": item.schema_version,
        "payload": item.payload,
    }


def ledger_dict(item: LedgerEntry) -> dict[str, Any]:
    return {
        "entry_id": item.entry_id,
        "transaction_id": item.transaction_id,
        "account": item.account,
        "entry_type": item.entry_type,
        "amount_minor": item.amount_minor,
        "currency": item.currency,
        "reference": item.reference,
        "simulation_only": item.simulation_only,
        "created_at": _iso_utc(item.created_at),
    }
