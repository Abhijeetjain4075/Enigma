# Enigma Testing and Conformance Strategy

## Test pyramid

### Unit tests

Canonical models, state transitions, money arithmetic, error mapping, policy evaluation.

### Contract tests

Verify each adapter against its provider's documented contract.

### Protocol conformance

Use official certification/conformance tooling where available.

### Integration tests

Exercise provider sandbox APIs and event flows.

### Failure tests

Simulate:

- timeout
- duplicate event
- out-of-order event
- malformed response
- provider restart
- stale data
- payment failure
- refund failure
- CDR mismatch
- partial outage

### End-to-end tests

Validate the complete path:

request -> capability match -> authorization -> provider operation -> event -> session -> billing -> reconciliation.

## Property/invariant testing

Important invariants include:

- no negative balance unless explicitly supported;
- no duplicate financial capture from one idempotency key;
- no illegal state transition;
- refund <= captured amount;
- every financial mutation has an audit event;
- external identifiers remain namespaced.

## Certification

Where an external standard provides official certification, distinguish:

- specification compliance
- certification
- commercial approval
- production readiness

They are different gates.

## Release gate

A transaction-capable adapter should not reach broad production until:

- security review passes;
- contract tests pass;
- failure tests pass;
- reconciliation tests pass;
- observability exists;
- rollback/disablement exists;
- commercial permission is documented.
