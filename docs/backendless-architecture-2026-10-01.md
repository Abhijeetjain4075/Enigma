# Enigma Backendless Architecture — 2026-10-01

## Decision

Enigma should not require an Enigma-operated long-running backend for its core interoperability protocol.

The protocol itself must be portable and verifiable by participating clients, providers, and optional operator infrastructure.

This does **not** mean that the surrounding ecosystem has no servers. Provider APIs, charging networks, roaming hubs, payment processors, identity providers, enterprise systems, and optional relays remain external systems.

The architectural boundary is:

**Enigma protocol = mandatory; Enigma hosting = optional.**

## Why this is technically credible

The first prototype in `enigma/protocol.py` demonstrates that these primitives can exist without an Enigma database:

- deterministic transaction identifiers
- signed transaction intents
- Ed25519 signature verification
- local event state
- hash-linked event histories
- signed evidence objects
- replay detection
- independent-history reconciliation
- portable export/import
- process-recovery semantics

The prototype is deliberately offline and has no network or database dependency.

It is not provider conformance evidence and does not prove that any provider permits direct client-to-provider orchestration.

## Responsibility placement

| Function | Default owner | Enigma-hosted backend required? |
|---|---|---|
| Transaction intent | client/operator | No |
| Local state machine | client/operator | No |
| Event history | client/operator/provider | No |
| Evidence object | evidence producer/holder | No |
| Provider physical/service state | provider | No |
| Provider API | provider | No |
| Payment authorization/capture | licensed payment provider / merchant context | No |
| Reconciliation | participants | No, for bilateral reconciliation |
| Multi-device sync | user/operator storage or optional relay | No |
| Discovery | provider registries / signed manifests / optional index | No |
| Credential storage | client/operator secret store | No |
| Enterprise fleet coordination | operator node or existing enterprise platform | No |
| Public search/indexing | optional indexer | No |
| Webhook termination | provider endpoint or user/operator node | No |
| Cross-party durable queue | participant-owned infrastructure or optional relay | No |
| Analytics | client/operator/indexer | No |
| Enigma API gateway | optional | No |

## The unavoidable caveat

Some workflows require durable coordination somewhere.

Examples:

- a provider that only accepts server-to-server OAuth
- a provider that requires a registered webhook URL
- multi-user enterprise coordination
- high-volume asynchronous event delivery
- cross-party queueing
- long-lived credential management
- centralized search over very large datasets

These do not prove that Enigma itself must host the infrastructure. They prove that **some participant must host coordination**.

The protocol therefore supports three deployment modes:

1. **Direct mode** — client/operator talks to provider directly.
2. **Node mode** — customer/operator runs an Enigma node.
3. **Relay mode** — an optional Enigma-compatible relay/gateway is used.

The same signed transaction/evidence model operates across all three.

## Protocol objects

### Transaction intent

A signed intent contains:

- protocol/version
- issuer key
- nonce
- principal
- operation
- provider
- resource
- request time
- authorization reference
- parameters
- deterministic transaction ID

The signature authenticates the issuer. It does not grant provider authorization.

### Event

Each event contains:

- transaction ID
- sequence
- event type
- predecessor hash
- state
- occurred time
- authority
- producer key
- payload
- event hash
- signature

An event chain provides tamper evidence and portable history.

### Evidence

Evidence is a separately signed object with:

- source
- evidence type
- transaction ID
- observation time
- authority
- payload
- content identifier

Operational logs and evidence remain distinct.

## State authority model

Enigma must never treat every state as equally authoritative.

- **Provider-authoritative:** provider confirms the physical/service operation.
- **Client-authoritative:** client records what it requested.
- **Observed:** Enigma/client has observed an external response.
- **Evidence-backed:** a signed/content-addressed artifact supports a claim.
- **Unknown:** the evidence required to decide has not arrived.
- **Reconciliation required:** independent histories disagree.
- **Financial settlement:** only the payment/settlement system can establish final money movement.

A timeout is therefore not equivalent to failure.

## Idempotency without a central database

A protocol-level transaction ID is deterministic from issuer key, nonce and intent.

Participants additionally maintain a local seen-set of event/content IDs.

This provides deterministic duplicate detection, but not global exactly-once execution.

For physical-world operations, provider-native idempotency or provider-side transaction references remain necessary.

## Conflict model

The protocol does not elect a winner when two authorities disagree.

Instead:

- preserve both histories
- identify the divergent sequence
- classify the transaction as uncertain/reconciliation_required
- require an authoritative source or explicit reconciliation rule

This prevents a compromised client from overwriting provider truth.

## Discovery and capabilities

Capability manifests should be signed by their issuer and include:

- provider/issuer
- protocol and version
- operations
- authentication mechanisms
- supported lifecycle operations
- webhook/polling mode
- idempotency semantics
- rate limits
- evidence types
- validity period
- contractual prerequisites

A discovery document proves what an issuer claims to support; it does not prove contractual permission.

## Authorization

The portable authorization layer should model:

`principal -> delegation -> audience/provider -> capability/scope -> validity -> revocation reference`

OAuth/OIDC, OCPI credentials/tokens, OICP contracts, ISO 15118 certificates, RFID credentials and proprietary API keys remain provider/protocol-specific credentials. Enigma should reference them rather than pretending they are interchangeable.

## Payments and settlement

Enigma should not become the payment rail merely because the protocol can carry money-state references.

The protocol may carry:

- payment authorization reference
- capture reference
- refund reference
- invoice reference
- settlement reference
- reconciliation evidence

The actual funds movement remains with the licensed/payment/merchant context.

## Security model

Threats requiring explicit controls:

- stolen client key -> revoke/rotate delegation; provider authorization remains separate
- replay -> nonce, deterministic IDs, provider idempotency
- event forgery -> signatures
- event reordering -> sequence/predecessor verification
- rollback -> monotone sequence + external authoritative state
- split brain -> preserve competing histories and reconcile
- malicious provider -> evidence is attributed, not blindly trusted
- duplicate payment intent -> payment-provider idempotency and transaction IDs
- key compromise -> short-lived delegation and rotation
- malicious discovery -> signed manifest + validity/issuer policy
- optional relay SSRF -> strict provider allowlists and egress policy
- supply chain -> signed releases, lockfiles, immutable CI dependencies

Cryptography authenticates messages; it does not establish legal or commercial authority.

## Provider compatibility boundary

Backendless operation is provider-dependent.

If a provider offers a mobile/client-safe protocol, direct mode may be possible.

If a provider requires server-to-server credentials or registered webhooks, Enigma must use:

- an operator-owned node,
- provider/roaming infrastructure,
- or an optional Enigma relay.

The protocol remains backend-independent even when a particular deployment needs a node.

## Production acceptance gate

The first real provider proof requires:

1. documented provider authorization;
2. approved sandbox or equivalent controlled environment;
3. provider-specific adapter;
4. authenticated provider requests;
5. provider-native idempotency or equivalent transaction reference;
6. real provider session lifecycle;
7. authenticated event/CDR evidence;
8. timeout and recovery test;
9. repeated transaction tests;
10. reconciliation against provider evidence;
11. credential rotation/revocation test;
12. audit/evidence retention test.

No simulator result satisfies this gate.

## Current deployment implication

Render and Vercel are not architectural requirements for the core protocol.

The likely artifact set is:

- Python/TypeScript SDK
- client application
- provider adapters
- optional operator node
- optional relay
- documentation/developer portal
- optional discovery/index service

The existing FastAPI transaction lab should remain available for controlled simulator testing and must not be relabeled as the protocol runtime.

## Falsification criteria

The backendless protocol thesis should be rejected or narrowed if repeated provider research shows that target providers universally require:

- Enigma-hosted server-side secrets,
- Enigma-hosted webhooks,
- centralized Enigma coordination for every transaction,
- or infrastructure that cannot be delegated to the customer/provider/operator.

In that case Enigma can still remain a protocol/SDK layer with optional hosted infrastructure rather than abandoning the abstraction.

## Current status

- Protocol prototype: implemented in repository.
- Real provider integration: blocked externally.
- Provider conformance: not implemented.
- Production transaction processing: not implemented.
- Backendless feasibility: technically credible for the protocol core; provider-specific workflows remain conditional.
