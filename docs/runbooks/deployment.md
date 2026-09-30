# Deployment runbook (current simulator-only milestone)

## Scope and warning

This deploys the **simulator-only** API for local development only. It does not connect to a real provider, initiate a payment, move funds, or operate a charger. The application factory now refuses to start in `staging` or `production` while this build has no real provider adapter. `compose.yaml` is a loopback-bound local-development scaffold, not staging infrastructure or production certification. Do not expose its Postgres port or use a superuser application credential on the public internet.

## Local development

Requirements: Python 3.12+ and an empty writable working directory.

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip uv
uv sync --all-extras --frozen
export ENIGMA_ENV=development
export DATABASE_URL=sqlite:///./enigma-dev.db
export ENIGMA_API_KEYS="$(python -c 'import json,secrets; print(json.dumps({secrets.token_urlsafe(32): "tenant-local"}))')"
uvicorn enigma.main:app --host 127.0.0.1 --port 8000
```

Every environment requires an explicit API-key-to-tenant map; no default development credential exists. The database tables are created locally at app construction; staging/production never auto-create schema.

## Container/Compose scaffold

Create a private `.env` (never commit it), use a 32+ character random key, and set `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, and `ENIGMA_API_KEYS` as a JSON object mapping API keys to tenant IDs. Prefer hexadecimal secrets for the local Compose DSN to avoid URL-encoding ambiguity.

```bash
umask 077
api_key="$(openssl rand -hex 32)"
db_password="$(openssl rand -hex 32)"
printf 'POSTGRES_DB=enigma\nPOSTGRES_USER=enigma_owner\nPOSTGRES_PASSWORD=%s\nENIGMA_ENV=development\nENIGMA_API_KEYS={"%s":"tenant-local"}\n' \
  "$db_password" "$api_key" > .env
export ENIGMA_LOAD_API_KEY="$api_key"
unset api_key db_password
```

The command generates unique local credentials and stores them in a private `.env`; no example or fallback credential is used. Compose binds the API to `127.0.0.1` and defaults to development. Its initial database owner is for a disposable local stack only. Do not use it as a production API runtime role or set `ENIGMA_ENV=staging` to bypass the real-provider startup gate.

```bash
docker compose build
docker compose run --rm --entrypoint alembic api upgrade head
docker compose up -d
curl --fail http://127.0.0.1:8000/health/ready
```

Migrations are **not** run automatically by the API process. In production, run them as a reviewed deployment step with a migration role; start the API with a restricted runtime role.

## Production prerequisites not supplied by this repository

Before any production traffic:

1. Provision separate migration-owner and API-runtime database roles. Runtime must be non-superuser, `NOBYPASSRLS`, not table owner, and limited to required CRUD/sequence privileges; immutable-table triggers still reject update/delete.
2. Verify PostgreSQL RLS policies are active and test using the exact runtime role. Do not test RLS as a superuser/owner.
3. Store API keys in a managed secret store; define key issuance, rotation, and revocation. Use TLS at the edge and to PostgreSQL according to the hosting environment.
4. Deploy behind a trusted ingress/load balancer, configure trusted proxy networks, request-size limits for chunked requests, distributed rate limits, WAF/DDOS controls, and network egress denial for provider integrations.
5. Add managed backups, point-in-time recovery, restore drills, alerting, service SLOs, incident ownership, and a reviewed rollback strategy.
6. Obtain actual provider agreements, approved test credentials, provider-specific certification, merchant/payment/legal decisions, privacy review, support escalation, and operational authority. None is represented as complete by the simulator.

## Smoke check

```bash
curl --fail http://127.0.0.1:8000/health/live
curl --fail http://127.0.0.1:8000/health/ready
curl --fail -H "X-API-Key: $ENIGMA_LOAD_API_KEY" http://127.0.0.1:8000/v1/providers
```

For a bounded local API-only load probe, set `ENIGMA_LOAD_API_KEY` to a disposable tenant key and run `python scripts/load_smoke.py --requests 40 --workers 8`. This does not certify capacity or real-provider behavior.
