# Enigma Provider Integration Contract

## Goal

Make provider integrations repeatable rather than bespoke application code.

## Adapter boundary

Every adapter should expose canonical operations where the provider supports them:

- discover_assets
- get_asset
- get_availability
- get_tariff
- authorize
- reserve
- start
- stop
- get_session
- receive_events
- receive_cdr
- refund
- health_check

Unsupported operations must be represented explicitly as unsupported, not simulated.

## Provider capability declaration

Each provider integration should declare:

- domains
- geography
- protocol
- protocol version
- authentication method
- supported operations
- data freshness
- rate limits
- webhook support
- retry semantics
- idempotency behavior
- certification requirements
- contractual prerequisites
- commercial prerequisites

## Integration lifecycle

1. research
2. commercial qualification
3. technical discovery
4. credentials exchange
5. sandbox integration
6. contract tests
7. conformance testing
8. controlled production
9. monitoring
10. reconciliation
11. incident review
12. version upgrade

## Protocol strategy

Prefer standards and official APIs. Use direct proprietary integrations only when the value is material and contractual permission exists.

## Versioning

An adapter must pin external protocol/API versions.

Internal canonical contracts should evolve independently.

Breaking changes require:

- new adapter version
- migration plan
- compatibility tests
- rollback path

## Reliability requirements

Each adapter needs:

- timeout policy
- retry policy
- circuit breaker
- rate-limit handling
- dead-letter handling
- replay strategy
- provider incident mode
- stale-data behavior

## Commercial boundary

Technical connectivity does not imply permission to initiate a paid service.

The integration record must separately track:

- data-access permission
- transaction permission
- payment permission
- settlement permission
- brand/display permission
- geographic permission

## Conformance evidence

For every production adapter retain evidence of:

- endpoint behavior
- test cases
- provider certification if required
- contract approval
- observed production outcomes
- known limitations
