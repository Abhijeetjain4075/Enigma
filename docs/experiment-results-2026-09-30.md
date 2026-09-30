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

The GitHub Actions CI run for implementation commit `cabc66fcffe0f1cf131d2d583d3ac89116ba18fe` completed successfully: [run 36748878873](https://github.com/Abhijeetjain4075/Enigma/actions/runs/36748878873). The completed public-source synthesis is recorded in [the current competitive, standards and regulatory audit](current-competitive-standards-regulatory-audit-2026-09-30.md); that research does not establish any private integration or legal conclusion.

## Not verified here

The current sandbox has no Docker daemon/CLI, so the image build was verified only by the successful GitHub Actions run, not built locally. Live provider/standard conformance, a signed webhook path, production deployment, real payment/refund/settlement, external penetration testing, SLO/alerting, and backup/restore remain unverified. None may be inferred from the checks above.


## Fail-closed production-boundary follow-up — 2026-10-01 (local, pre-push)

The hardening changed the environment default to `production`, removed the implicit development API key, requires an explicit tenant API-key map in every environment, and rejects `staging`/`production` app construction before engine creation while no real provider adapter exists. The Docker image defaults to production; Compose explicitly defaults to development and binds the API to loopback only. A regression test covers both rejected environments and the no-default-credential behavior.

Local verification on the follow-up tree: **24 passed, 1 PostgreSQL-only test skipped, 89.14% coverage**. Ruff formatting/lint, mypy, Bandit, pip-audit, lock integrity, SQLite migration/model parity, package build, whitespace, and scan for removed default/sample credential strings passed. The skipped RLS test was then run separately against a newly migrated PostgreSQL 16 database using a restricted non-owner `NOBYPASSRLS` role; it passed. The test-only Starlette `httpx` TestClient deprecation warning remains, and pip-audit skips the unpublished local project because it is not a PyPI distribution. GitHub Actions run 36761240411 initially failed because the integration configured `staging`, which is now prohibited for simulator-backed startup. The test was corrected to explicit `test` mode, and test/development schema creation was restricted to SQLite. The local sandbox has no Docker daemon; the corrected PostgreSQL test and production-container refusal check require the next GitHub Actions run, linked from the implementation-status report.
