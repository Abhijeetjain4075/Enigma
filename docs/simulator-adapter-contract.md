# Simulator adapter contract and protocol-evidence boundary

## Contract implemented

The Python adapter boundary exposes deterministic operations for capability discovery, health, authorization, start, stop, CDR retrieval, and refund. The registry currently contains only `simulator-a` and failure-injection `simulator-b`. Capability records identify operation, current/stale/simulator state, observation and expiry times, declared protocol/version labels, source, and evidence level. Unsupported provider/scenario combinations are rejected explicitly.

Provider errors are typed with a stable error code and retryability. Simulator responses have deterministic external references suitable for idempotency/deduplication tests. Provider API keys, URLs, network clients, and real remote calls are not present.

## Evidence and protocol labels

Every simulated provider/capability/evidence result is `E4-simulated`. `protocol` and `protocol_version` fields are metadata for the adapter boundary and provenance record, not proof that OCPI, OCPP, OICP, ISO 15118, payment, webhook, identity, or certification behavior is conformant. No production standard profile is represented as implemented.

A future real adapter must include, at minimum: the precise standard/profile/version and supported feature subset; permission/contract and sandbox evidence; capability provenance and freshness rules; credentials/secrets rotation; signed webhook validation and replay protection; retry/backoff and provider-specific idempotency semantics; error mapping; conformance fixtures; version negotiation; health and circuit-breaker behavior; provider support/escalation ownership; data retention/security review; and a controlled kill-switch/rollback plan.
