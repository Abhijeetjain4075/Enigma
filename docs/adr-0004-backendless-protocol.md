# ADR-0004: Backend-Independent Enigma Protocol

- Status: Accepted
- Date: 2026-10-01
- Supersedes: the assumption that the FastAPI/database transaction lab is the required Enigma runtime
- Scope: protocol and deployment boundary

## Context

The existing Enigma repository contains a FastAPI/SQLAlchemy simulator transaction laboratory. It is useful for deterministic testing, tenancy, state-machine experiments, failure injection, reconciliation experiments and CI.

It is not evidence that Enigma must operate a centralized production backend.

External EV interoperability protocols already assume participating platforms, provider systems and endpoints. A central Enigma database is therefore not inherently part of interoperability.

## Decision

Enigma is defined as a **backend-independent interoperability protocol and execution SDK**.

The mandatory layer is:

- canonical transaction model
- deterministic intent identity
- authorization/delegation references
- capability model
- provider adapter contract
- deterministic state machine
- event/evidence model
- replay/idempotency semantics
- reconciliation protocol
- recovery/export/import format
- versioning and compatibility rules

Enigma-hosted infrastructure is optional.

Supported deployment modes:

1. Direct client/operator mode
2. Customer/operator-owned Enigma node
3. Optional Enigma-compatible relay

## Consequences

### Positive

- no mandatory Enigma database
- no mandatory Enigma webhook service
- no mandatory Enigma queue
- lower infrastructure cost for direct deployments
- portable transaction history
- local-first operation and offline recovery become first-class
- customer/operator control over sensitive credentials is possible
- protocol can outlive any individual hosting implementation

### Negative

- multi-device synchronization becomes a participant responsibility
- discovery may need external indexes
- some providers require server-to-server credentials or inbound endpoints
- global rate limiting cannot be guaranteed without shared infrastructure
- bilateral reconciliation is straightforward; global reconciliation still needs coordination
- key revocation/discovery requires a trust mechanism
- provider-specific commercial contracts remain unavoidable

## Authority rule

The protocol distinguishes:

- requested state
- client-observed state
- provider-authoritative state
- evidence-backed state
- unknown state
- reconciliation-required state
- financial settlement state

A signed client event never overrides provider-authoritative physical-world state.

## Existing FastAPI application

The current simulator remains.

Its role is:

- executable laboratory
- conformance fixture harness
- failure-injection environment
- database-backed reference implementation
- local API demonstration
- CI verification target

It is not required for every Enigma deployment.

## Cryptography

The first dependency-free protocol proof uses HMAC-SHA256 with a local verifier key registry. This is deliberately not treated as the production public-key trust model.

Production protocol identity should use an asymmetric signature mechanism and explicit key discovery, rotation and revocation semantics. Ed25519 is a candidate; final selection requires a dedicated cryptographic/security review.

## Provider boundary

Provider authorization is never inferred from an Enigma protocol object.

Provider-specific requirements remain authoritative:

- credentials
- certificates
- OAuth/OIDC
- OCPI credentials
- OICP contracts
- registered endpoints
- webhook requirements
- IP allowlists
- commercial agreements
- payment permissions

## Falsification

This decision must be narrowed if real provider integrations demonstrate that Enigma cannot operate its intended value proposition without Enigma-owned centralized coordination.

The response is not to force decentralization. The response is to move only the minimum required infrastructure into an optional Enigma node/relay.

## Implementation status

- Protocol primitives: implemented
- Portable bundle: implemented
- Bilateral reconciliation proof: implemented
- Provider integration: external blocker
- Production cryptographic trust model: not implemented
- Provider conformance: not implemented
