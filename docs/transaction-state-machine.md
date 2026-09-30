# Enigma Transaction and Operation State Model

## Principle

A single status field is insufficient for a distributed transaction.

Enigma should model at least three correlated state machines:

1. intent/transaction state
2. provider operation state
3. money state

## Transaction state

Suggested states:

- created
- validated
- authorized
- initiated
- active
- completed
- billed
- settled
- cancelled
- expired
- failed
- disputed
- reconciliation_required
- partially_refunded
- refunded

State transitions must be explicit and validated.

## Provider operation state

Examples:

- requested
- accepted
- rejected
- queued
- started
- running
- stopped
- unknown
- timed_out
- provider_error

Provider state must not automatically overwrite commercial state.

## Money state

Examples:

- not_applicable
- payment_method_verified
- authorized
- captured
- partially_captured
- refunded
- partially_refunded
- chargeback_open
- chargeback_resolved
- payable_created
- payable_settled
- reconciliation_required

## Invariants

1. A refund cannot exceed the refundable amount.
2. A captured amount cannot be silently rewritten.
3. A provider timeout does not prove that the provider operation did not occur.
4. Retries must use idempotency keys.
5. Every external operation needs a correlation identifier.
6. Every financial mutation needs an audit event.
7. Reconciliation is a state, not a background assumption.

## Distributed failure example

Enigma sends a remote-start request.

The provider starts the session but the response times out.

Correct behavior:

1. mark the request as uncertain/timeout;
2. do not immediately issue a second non-idempotent start;
3. query provider state where supported;
4. correlate asynchronous events;
5. resolve to started, failed, or reconciliation_required;
6. preserve the original evidence.

## Event model

Every meaningful transition should produce an immutable event with:

- event_id
- event_type
- aggregate_id
- aggregate_type
- event_version
- occurred_at
- received_at
- producer
- correlation_id
- causation_id
- payload schema version

Events are append-only evidence. Current state is a projection.

## Idempotency

Client and provider operations should support:

- idempotency key
- request hash
- actor
- operation type
- expiration policy
- response replay

A repeated request with the same valid key must not create a duplicate financial or physical-world action.

## Reconciliation

Reconciliation compares Enigma's expected state with provider evidence.

Examples:

- session exists at provider but not Enigma
- Enigma captured payment but provider CDR is missing
- provider CDR differs from expected energy
- refund succeeded externally but internal state remains pending

Unresolved mismatches must be visible to operations.
