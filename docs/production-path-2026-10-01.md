# Enigma Production Path — 2026-10-01

## Current verified state

The repository is an executable simulator transaction laboratory, not a production interoperability service. The existing fail-closed production guard remains intact.

The new backendless protocol prototype is intentionally separate from the simulator API and database. It provides signed, portable transaction primitives without requiring an Enigma-operated database.

## Architecture direction

**Enigma protocol mandatory; Enigma hosting optional.**

The core protocol carries portable transaction intent, local state, signed events, evidence and reconciliation material. Provider APIs, payment processors, identity systems and physical/service state remain external authorities.

Deployment modes:

- direct client/operator mode
- customer/operator-owned Enigma node
- optional relay/gateway mode

## What changed

Added:

- `enigma/protocol.py`
- `tests/test_backendless_protocol.py`
- `docs/backendless-architecture-2026-10-01.md`

Updated:

- `pyproject.toml` to include the Ed25519 cryptography dependency.

The existing simulator, database schema, API, production refusal and provider boundary were not removed.

## Provider path

No provider credentials or authorization are currently available to this implementation. Therefore no live provider integration is claimed.

The first real provider proof remains externally blocked on:

- provider agreement/authorization
- sandbox or controlled access
- credentials
- provider-specific permissions
- payment/merchant context if money movement is included
- webhook/event access if required

Public documentation can be used to build fixture adapters, but fixture tests are not provider-conformance tests.

## Acceptance criteria

A real provider proof is complete only when Enigma demonstrates:

1. authorized sandbox access;
2. provider-specific authentication;
3. capability discovery;
4. real transaction/session initiation;
5. provider-authoritative state observation;
6. signed/authenticated event or CDR evidence;
7. timeout recovery;
8. duplicate/replay handling;
9. reconciliation;
10. repeated successful and failed transactions;
11. credential rotation/revocation;
12. evidence retention.

## Backend elimination

The protocol core does not require:

- Enigma database
- Enigma webhook server
- Enigma-owned queue
- Enigma-owned identity database
- Enigma-owned payment ledger

Some providers may still require a server-side integration. In that case the server should be customer/operator-owned or an optional Enigma-compatible node/relay.

## Render/Vercel

Render currently fails closed because the simulator-only application refuses production/staging startup and the service has no required production configuration. Vercel's deployment status does not establish backend correctness; the known public alias returned a function invocation failure.

Neither platform should drive the architecture.

If the protocol core is the primary product, the required deployment surface can instead be client/SDK artifacts plus optional nodes/relays.

## Safety boundary

The LLM is not part of transaction authority.

It must not decide:

- physical-world execution
- financial movement
- legal settlement
- security authorization
- authoritative transaction state

Deterministic code and external authorities perform those functions.

## Next engineering sequence

1. finish protocol conformance tests;
2. add signed capability/delegation manifests;
3. add provider-adapter fixture contract;
4. research and select an accessible provider sandbox based on evidence;
5. implement one provider adapter;
6. obtain authorized sandbox credentials;
7. execute repeated controlled provider transactions;
8. add real evidence/reconciliation tests;
9. only then decide whether any optional relay/node is required.

## Readiness

Backendless protocol core: PARTIAL — prototype implemented, provider compatibility unverified.

Real provider integration: BLOCKED_EXTERNAL.

Production transaction processing: NOT_IMPLEMENTED.

Provider conformance: NOT_IMPLEMENTED.

Hosted Enigma backend: OPTIONAL by architecture, not currently required by the protocol core.
