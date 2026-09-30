# Readiness gates for the simulator milestone

## Gate A — local/CI demonstration

Pass only when all are true: unit/API failure suite passes; migration upgrades and downgrade/upgrade succeed; linter/formatter/type/security checks pass; SQLite migration parity holds; PostgreSQL RLS test passes under the restricted runtime role; the app health/readiness and authenticated lifecycle work end-to-end; output and docs explicitly label simulator evidence; no real-provider egress path exists.

## Gate B — isolated partner sandbox (not yet authorized)

Requires documented partner permission, approved sandbox credentials, contract/API scope, provider support contact, version/capability matrix, provider conformance tests, signed event delivery/replay protection, secrets lifecycle, tenant/RBAC scopes, support and escalation ownership, data processing/retention review, and security/rollback approval. Successful simulator tests do not pass this gate.

## Gate C — production transaction processing (not passed)

Requires all product/provider/financial/legal/operations/evidence controls in `docs/launch-readiness.md`, an accountable named owner for every control, penetration/risk testing, reviewed SLO/alerts/incident response, tested backup and restore, measured load/DR, operational kill switch, controlled canary transactions, and actual production evidence. A production readiness claim is prohibited until evidence is reviewed and signed by the responsible owner.

## Current disposition

Gate A is being verified by repository tests and CI configuration. Gates B and C remain blocked; see `docs/implementation-status-2026-09-30.md`.

The current build now refuses application startup in both `staging` and `production` because the only implemented providers are deterministic simulators. Local Compose binds to loopback and defaults to `development`; this guard prevents the existing simulator from being presented as a live provider integration. It is not a substitute for implementing and validating real provider adapters.
