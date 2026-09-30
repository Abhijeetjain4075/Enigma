# Enigma Software Architecture

## High-level model

Client and partner applications
-> Enigma API
-> identity and authorization
-> capability and provider registry
-> orchestration engine
-> protocol adapters
-> provider systems

Payment and settlement services operate across the transaction lifecycle.

## Major services

### Identity

Models people, vehicles, organizations, fleets, applications, and provider relationships.

### Provider registry

Stores provider capabilities, service types, geographic coverage, supported protocols, tariffs, operational state, and integration metadata.

### Capability engine

Answers whether a requested action is possible for a specific vehicle, user, location, provider, and time.

### Orchestration engine

Converts an outcome into provider-specific operations.

Example:

Find suitable charger
-> validate connector and power
-> retrieve tariff
-> authorize
-> start session
-> monitor
-> stop
-> create CDR
-> calculate charge
-> settle
-> issue receipt.

### Protocol adapter layer

Adapters should isolate provider-specific protocols and APIs from the core domain model.

Initial standards to investigate include OCPI, OCPP, OICP, ISO 15118, and payment APIs.

### Transaction ledger

Every externally meaningful operation should have an auditable lifecycle, idempotency key, provider reference, timestamps, monetary amounts, status transitions, and reconciliation state.

### Trust and intelligence

Normalize:

- availability
- reliability
- price
- compatibility
- latency
- historical failures
- provider health
- user reports.

### Developer platform

Expose:

- REST APIs
- webhooks
- SDKs
- OAuth or equivalent delegated authorization
- sandbox
- documentation
- test fixtures
- observability.

## Architectural principles

1. Provider-neutral core.
2. Standards before proprietary protocols where practical.
3. Idempotent financial operations.
4. Event-driven transaction state.
5. Explicit audit trails.
6. Zero-trust integration boundaries.
7. Capability-based authorization.
8. Geographic and regulatory isolation.
9. Provider failures must not corrupt the global transaction ledger.
10. The consumer application must not be the only interface.

## Canonical transaction state

Proposed generic lifecycle:

created -> authorized -> initiated -> active -> completed -> billed -> settled

Exceptional states:

rejected, expired, failed, cancelled, disputed, refunded, partially_refunded, reconciliation_required.