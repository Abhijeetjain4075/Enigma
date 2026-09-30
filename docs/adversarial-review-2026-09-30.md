# Adversarial implementation review — 2026-09-30

## Claim under review

The narrow claim is: the local simulator API can demonstrate deterministic transaction transitions, tenant-key-scoped API reads/writes, idempotent replay, evidence/event capture, and safe non-posting behavior on unresolved CDR mismatch. It does not claim live provider support, money movement, settlement, regulatory compliance, or production capacity.

## Attack/failure attempts and controls

- **Cross-tenant resource guessing:** API queries include tenant predicate; PostgreSQL migration adds forced RLS with transaction-local tenant setting. Unit isolation exists; PostgreSQL test is in CI and must use a non-owner `NOBYPASSRLS` role. Superusers/BYPASSRLS roles can bypass policy; production role setup is an explicit deployment condition.
- **Concurrent stale writes:** stop/reconcile/refund require numeric `If-Match`; status/version update is compare-and-swap, and DB event aggregate versions are unique. Current contention behavior has not been stress-tested against PostgreSQL.
- **Retry after uncertain response:** mutation endpoints require `Idempotency-Key`, hash canonical request parameters, and replay the saved status/body. Same key with changed request is a conflict. Key retention, expiry, and cross-region idempotency remain undecided.
- **Duplicate provider CDR:** tenant/provider/external event uniqueness and explicit lookup avoid double-appending. PostgreSQL unique-violation races in concurrent identical webhook ingestion are not exercised because there is no webhook endpoint.
- **Stale availability:** simulator observation explicitly marked stale rejects creation and preserves stale evidence.
- **CDR disagreement:** unresolved mismatch blocks posting and requires manual review; no auto-correction path is present.
- **Delayed CDR:** accepted stop with missing CDR is marked unresolved; explicit operator-like API reconciliation can retrieve a deterministic late simulator result. No signed webhook intake, background retry queue, or real operator identity exists.
- **Refund outage/over-refund:** simulated provider failure does not create refund ledger entries; bounds use remaining billed amount; ledger signs balance after partial/full refund. No payment rail is called.
- **Credential disclosure through responses/logs:** API keys are compared but never intentionally emitted; request logs omit headers, body, and query values. There is no external log redaction/retention platform yet.
- **Oversized/chunked request:** `Content-Length` is bounded, but chunked bodies can bypass that app-layer check; enforce a hard size limit at ingress before any public deployment.
- **Abuse/load:** a thread-safe sliding window is process-local and keyed by client IP; it resets on restart, is not distributed, and can be wrong behind untrusted proxies. Use gateway/WAF/distributed tenant limits before exposure.
- **Database operator writes:** PostgreSQL migration triggers reject UPDATE/DELETE on event/evidence/ledger tables; superusers can disable triggers. Use restricted roles and monitored privileged access.
- **Schema/deployment rollback:** initial Alembic migration provides downgrade, but no data-preserving blue/green upgrade, canary, PITR restore, or rollback drill is complete.

## Residual release risks

No actual protocol certification, provider contract, payment/tax/MoR analysis, data protection/legal review, penetration test, signed webhook processing, external secrets manager, broad RBAC, metrics/tracing/alerts, on-call model, product demand evidence, or real end-to-end transaction has been delivered. These are blockers, not assumptions.
