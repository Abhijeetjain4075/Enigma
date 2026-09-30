# ADR-0003: Simulator-first executable transaction lab

- **Status:** Accepted for the first executable milestone
- **Date:** 2026-09-30
- **Decision owners:** Engineering (implementation); product/provider/legal approvals remain external

## Context

The repository previously held research, domain specifications, and launch gates but no executable transaction service or real partner permissions/credentials. A real charging, payment, refund, or settlement call could have physical, financial, contractual, and regulatory consequences. Simulator behavior cannot demonstrate that a protocol or provider is actually supported.

## Decision

Implement an API-backed, PostgreSQL-capable **simulator-only transaction lab** with a deterministic adapter boundary, explicit failure scenarios, optimistic state-version checks, idempotency, tenant-scoped persistence, evidence/event provenance, simulated double-entry ledger postings, and reconciliation. Real provider calls, payments, settlement, and equipment control are intentionally absent and must remain absent until contracts, security design, test credentials, operational authority, and provider-specific certification exist.

PostgreSQL enforces tenant row-level security (RLS) using transaction-local `app.tenant_id` context and rejects application-level mutation of event, evidence, and ledger rows. Production deployments must use a non-superuser, `NOBYPASSRLS`, non-owner runtime role; migration privileges must be separated from runtime privileges.

## Alternatives considered

1. **Implement an unverified live provider integration:** rejected because no contract, production/test credentials, provider support contact, or transaction authority was supplied.
2. **Stop at architecture-only documentation:** rejected because deterministic implementation and failure tests materially improve evidence and falsifiability.
3. **Build a broad UI/SDK before a verified engine:** rejected because it would add surface area without improving the central transaction correctness claim.

## Consequences

- The deliverable can demonstrate API, lifecycle, tenant, idempotency, evidence, recovery, and ledger invariants against simulators; it cannot demonstrate production provider conformance, real payment handling, settlement, or operational readiness.
- Simulated evidence is labeled `E4-simulated`; a simulator result is not provider attestation.
- Unresolved CDR mismatch is preserved for manual review; the system does not silently rewrite financial records.
- External legal/commercial decisions, production credentials, customer support, and provider approvals remain explicit launch blockers.
- This decision should be revisited only with an approved provider sandbox, contract/permission evidence, an operator owner, and a documented rollback plan.
