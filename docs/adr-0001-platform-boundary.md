# ADR-0001: Platform Boundary

## Status

Accepted as a research architecture decision.

## Context

The original problem is fragmented EV charging access, but generic charging aggregation and roaming are already established markets.

## Decision

Enigma will be designed as a **software interoperability and transaction-orchestration layer**, not as a physical infrastructure owner.

The architecture must support multiple providers and protocols while keeping provider ownership, user applications, payment providers and physical infrastructure as separate parties.

## Consequences

Positive:

- provider neutrality
- lower capital intensity
- reusable canonical model
- ability to consume multiple existing networks
- cross-domain expansion path

Negative:

- integration and contracting burden
- dependency on provider permissions
- difficult reconciliation
- potential regulatory exposure
- competition with mature interoperability providers

## Reversal condition

Reconsider this boundary if evidence shows that the software layer cannot obtain sufficient permissions, data quality or economic value without owning infrastructure.
