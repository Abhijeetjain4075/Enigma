# Operations runbook (simulator milestone)

## Service checks

- Liveness: `GET /health/live`
- Readiness (database connectivity): `GET /health/ready`
- API docs: `/docs`; machine-readable schema: `/openapi.json`
- Every response carries `X-Request-ID` and `X-Correlation-ID`; structured request logs intentionally omit request bodies, API keys, and raw provider secrets.
- Current limiter is per-process/per-IP and resets on restart. It is not a distributed tenant quota or DDoS defense.

## Failure scenarios

Only `simulator-b` supports the named deterministic cases:

- `provider_outage`: authorization fails and a failed transaction plus error evidence is preserved.
- `stale_availability`: stale capability evidence results in rejection; stale is never rendered as available.
- `delayed_webhook`: stop is accepted, missing CDR is marked unresolved, and explicit reconcile replays a deterministic late simulator CDR.
- `duplicate_event`: repeated CDR external IDs are suppressed by tenant/provider/event uniqueness.
- `cdr_mismatch`: no ledger charge is posted; the discrepancy stays unresolved for a human review process outside this milestone.
- `refund_failure`: refund failure is recorded; no refund ledger entries are added.

These are test fixtures, not evidence of a live provider's failure behavior.

## Transaction/evidence review

1. Fetch `GET /v1/transactions/{id}` using the same tenant API key.
2. Inspect `/events`, `/evidence`, `/reconciliation`, and `/ledger` subresources.
3. Confirm ordered event versions, UTC timestamps, source/adapter/protocol/transformation versions, evidence-level label, external event ID, conflict status, and correlation ID.
4. Reconcile only with a new `Idempotency-Key` and current numeric `If-Match` version. Replays return the original result.
5. Never edit an event/evidence/ledger row to make a mismatch disappear. PostgreSQL triggers prohibit UPDATE/DELETE for these append-only tables; preserve unresolved cases for manual review.

## Incident response (current limits)

- Restrict or remove API ingress at the hosting/network layer; this milestone has no real-world provider kill switch because no live provider exists.
- Revoke the compromised API key in the deployment secret store and rotate affected keys. There is no self-service key administration endpoint.
- Preserve database snapshots and application logs with their request/correlation IDs. Logs must remain free of credentials and request bodies.
- Determine impacted tenants and transaction IDs using tenant-isolated data; review idempotency entries, transaction events, evidence, and ledger entries.
- Contact the deployment owner; this repository does not yet define a staffed 24/7 escalation or customer-support commitment.

## Restore and rollback

Back up PostgreSQL with the hosting provider's encrypted, access-controlled backup/PITR service and test restoring into an isolated environment. After restore, verify migration head, RLS policies, immutable-table triggers, table counts, and tenant isolation using a restricted runtime role before directing traffic. No backup/restore drill has been executed in this task, so disaster recovery is not claimed as proven.

Rollback the application image only when its schema is backward-compatible. `alembic downgrade base` is exercised in CI for the initial schema, but production data rollback, PITR, and operator approval workflows are not yet qualified.
