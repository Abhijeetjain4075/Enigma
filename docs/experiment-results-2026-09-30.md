# Verification and experiment record — 2026-09-30

This record distinguishes executable test evidence from external provider or production evidence. All transaction outcomes here use deterministic simulators.

## Automated checks

| Check | Command / environment | Result |
|---|---|---|
| Formatting and lint | `uv run ruff format --check .`; `uv run ruff check .` | Passed; 85 files formatted/checked, no lint findings |
| Static typing | `uv run mypy enigma` | Passed; 10 application modules, no issues |
| Unit/API/failure tests | `ENIGMA_TEST_POSTGRES_URL=... uv run pytest --cov=enigma --cov-report=term-missing --cov-fail-under=80` | **22 passed**, 88.00% total coverage; PostgreSQL test ran, no skips |
| SQLite migration | `alembic upgrade head`; `alembic check` against a fresh temporary SQLite database | Passed; no model drift |
| PostgreSQL migration | PostgreSQL 16: `upgrade head`, `downgrade base`, `upgrade head`, `alembic check` | Passed; no model drift |
| PostgreSQL tenant/data controls | Restricted non-owner `NOBYPASSRLS` runtime role; tenant-one create/stop/reconcile/ledger; tenant-two lookup; missing-context SELECT; attempted event UPDATE | Passed; cross-tenant access returns not found, no-context sees no tenant rows, append-only trigger rejects event mutation |
| SAST | `uv run bandit -q -r enigma` | Passed; no findings |
| Dependency audit | `uv run pip-audit` | Passed; **no known vulnerabilities found** in auditable dependencies. The local, unpublished project itself is skipped because it is not present on PyPI. An earlier pytest advisory was corrected by updating the lower bound and lock to pytest 9.1.1. |
| Lock integrity | `uv lock --check` | Passed |
| Python package build | `uv build --no-sources` | Passed; source distribution and wheel built |

The test run reports one upstream `StarletteDeprecationWarning`: current Starlette still supports its `httpx` TestClient fallback but recommends `httpx2` for future TestClient use. It is test-tool-only; API runtime and production dependencies do not rely on TestClient. This should be reassessed when updating FastAPI/Starlette.

## Manual HTTP/browser and smoke-load checks

A temporary sandbox API instance using a disposable development-only key and SQLite database passed `/health/live`, `/health/ready`, `/openapi.json`, and authenticated `/v1/providers`. The FastAPI Swagger UI `/docs` loaded through the sandbox browser and showed the versioned operations and security scheme. After telemetry auto-configuration was explicitly disabled, the restarted service completed startup without the earlier optional-OpenTelemetry warning.

The bounded local-only `scripts/load_smoke.py` run used 40 create requests and 8 worker threads against `simulator-a`: **40/40 returned HTTP 201**, total elapsed 0.852 seconds, observed throughput 46.94 requests/second, median latency 58.05 ms, and p95 546.55 ms. This is one small smoke run on a shared sandbox, not a load/capacity benchmark, SLO, saturation test, or production performance claim.

## Not verified here

The current sandbox has no Docker daemon/CLI, so the image build is configured in GitHub Actions but was not executed locally. GitHub Actions, live provider/standard conformance, a signed webhook path, production deployment, real payment/refund/settlement, external penetration testing, SLO/alerting, and backup/restore remain unverified. None may be inferred from the checks above.
