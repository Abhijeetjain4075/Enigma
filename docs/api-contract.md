# Enigma API Contract Principles

## API layers

Enigma should expose distinct interfaces for:

1. discovery
2. capability evaluation
3. quote/tariff
4. authorization
5. service operations
6. transaction state
7. events/webhooks
8. reconciliation
9. partner administration

## Resource model

Stable resource identifiers should be opaque and globally unique within Enigma.

External provider IDs must remain provider-scoped.

## Request metadata

Requests should support:

- request_id
- correlation_id
- idempotency_key where mutation applies
- API version
- actor/application identity
- tenant/provider context

## Mutation requirements

Mutating endpoints must document:

- authorization scope
- idempotency
- state preconditions
- timeout semantics
- retry semantics
- asynchronous completion behavior
- audit event

## Async operations

Physical-world actions may complete after the HTTP request.

The API must expose:

- operation_id
- current status
- last provider evidence
- next expected event
- reconciliation state

## Webhooks

Webhooks should be versioned events rather than arbitrary provider-shaped payloads.

Consumers should be able to safely replay events.

## Compatibility

Breaking API changes require a new major version or explicitly versioned contract.

Deprecations require:

- notice period
- migration guide
- compatibility window
- telemetry on old-version usage
