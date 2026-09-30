# Roadmap

## Phase 0 - Research

Goal: prove the problem and map the ecosystem.

Deliverables:

- competitor database
- standards matrix
- CPO/eMSP integration matrix
- payment and settlement analysis
- regulatory research by target market
- user interviews
- provider interviews
- transaction failure taxonomy.

Exit condition: a specific high-value workflow is identified.

## Phase 1 - Charging data layer

Build:

- provider registry
- canonical charger model
- location search
- status normalization
- connector compatibility
- tariff normalization
- freshness monitoring.

No claim of universal charging access until real integrations exist.

## Phase 2 - Transaction layer

Add:

- authorization
- session lifecycle
- idempotency
- CDR ingestion
- billing
- receipts
- refund workflows
- reconciliation.

## Phase 3 - Roaming network

Add multiple real CPO integrations and evaluate direct OCPI versus roaming-hub connections.

Success metric is completed transactions, not number of listed stations.

## Phase 4 - Developer platform

Release:

- API
- SDK
- webhooks
- sandbox
- documentation
- partner dashboard
- observability.

## Phase 5 - Adjacent mobility

Expand only after charging transaction reliability is proven:

- parking
- tolls
- roadside assistance
- maintenance
- fleet workflows.

## Phase 6 - Energy

Investigate:

- home charging
- solar
- storage
- smart charging
- V2G
- energy optimization.

## Phase 7 - Network intelligence

Use accumulated transaction and operational data to improve:

- reliability
- routing
- price prediction
- availability prediction
- provider quality signals
- fraud detection
- operational optimization.

## Principle

Each phase must produce evidence that justifies the next. Avoid building every domain simultaneously.