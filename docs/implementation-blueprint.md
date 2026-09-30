# Implementation Blueprint

## Purpose

Convert Enigma from research architecture into a falsifiable executable system without prematurely building a universal super-app.

## Recommended repository structure

```
apps/
  api/
  worker/
packages/
  canonical-model/
  protocol-ocpi/
  provider-adapter/
  transaction-engine/
  evidence/
  ledger/
  reconciliation/
  policy/
  observability/
  sdk/
simulator/
  cpo/
  emsp/
  roaming-hub/
tests/
  contract/
  integration/
  failure/
  property/
  conformance/
schemas/
  events/
  api/
  evidence/
  ledger/
```

## First executable components

### 1. Canonical model

Entities:
- actor
- organization
- vehicle
- provider
- service
- location
- connector
- capability
- credential
- authorization
- session
- transaction
- tariff
- CDR
- invoice
- settlement
- evidence
- incident

### 2. Capability registry

Every provider capability must include:
- operation
- provider
- protocol
- protocol version
- geography
- contractual scope
- credential type
- freshness
- reliability
- evidence level
- last observed
- expiry
- fallback

### 3. Transaction engine

Required invariants:
- idempotent commands
- monotonic state transitions except explicit compensations
- correlation ID
- provider operation ID
- timeout
- retry policy
- duplicate suppression
- late-event handling
- reconciliation-required state
- manual intervention boundary

### 4. Evidence subsystem

Store:
- source
- raw reference
- observed time
- received time
- transformation version
- signature/hash where appropriate
- actor
- provider
- transaction
- evidence level
- retention class

### 5. Reconciliation engine

Compare:
- authorization
- session
- CDR
- invoice
- settlement
- refunds
- disputes

Output:
- matched
- partially matched
- missing
- conflicting
- duplicate
- unreconciled

### 6. Provider simulator

Simulate:
- success
- authorization rejection
- start timeout
- start accepted but no session
- session starts late
- stop timeout
- duplicate webhook
- contradictory CDR
- tariff mismatch
- provider outage
- replayed event
- refund
- dispute

### 7. Contract tests

Every adapter must prove:
- discovery mapping
- capability mapping
- authorization
- start/stop
- session event mapping
- CDR mapping
- error mapping
- idempotency
- reconciliation

## Release gates

A release cannot claim production readiness without:

- automated tests
- protocol fixtures
- security checks
- dependency checks
- schema compatibility checks
- audit log tests
- reconciliation tests
- load/latency measurements
- rollback plan
- incident runbook
- provider conformance result

## What not to implement yet

- universal consumer super-app
- every mobility domain
- proprietary payment rail
- physical charging network
- unbounded AI automation
- speculative token/crypto layer
- hundreds of provider adapters before one adapter works correctly

## First milestone

A deterministic local simulation proving:

`discover -> authorize -> start -> active -> stop -> CDR -> reconcile -> evidence`

with injected failures and complete audit history.

Second milestone:

one real permitted provider/sandbox using the same adapter contract.

Third milestone:

compare Enigma against the customer's existing roaming/CPMS stack and measure residual value.
