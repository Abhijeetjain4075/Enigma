# Enigma Observability and Operations

## Three pillars

### Metrics

Measure latency, errors, state transitions, queue depth, provider health and financial reconciliation.

### Logs

Logs should be structured and correlated.

Minimum fields:

- timestamp
- service
- environment
- request_id
- correlation_id
- tenant/provider
- operation
- outcome
- latency
- error_code

Never log secrets, raw payment credentials or unnecessary personal data.

### Traces

Distributed transactions should carry correlation context from client -> Enigma -> adapter -> provider -> webhook/event -> ledger/reconciliation.

## Provider health

Provider health should be multi-dimensional:

- connectivity
- API latency
- authentication health
- data freshness
- command success
- event delivery
- CDR completeness
- settlement health

A single "provider up/down" flag is insufficient.

## Incident states

Suggested provider modes:

- healthy
- degraded
- read_only
- command_disabled
- payment_disabled
- reconciliation_only
- unavailable

## SLOs

SLOs should be attached to specific capabilities, not vague platform availability.

Examples include availability freshness, authorization response latency, command success rate, webhook processing latency, and reconciliation completion time.

## Runbooks

Each production adapter needs runbooks for credential expiry, provider outage, schema change, rate-limit events, duplicate events, stuck sessions, missing CDRs, payment mismatches, and emergency command disablement.
