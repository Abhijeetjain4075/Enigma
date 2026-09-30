# Standards and Protocol Strategy

## Principle

Reuse existing standards wherever they provide adequate interoperability. Do not create a new protocol merely to rename an existing capability.

## OCPI

OCPI is central to EV roaming and supports information exchange between eMSPs and CPOs, including authorization, tariffs, sessions, CDRs and related operations.

Enigma should investigate OCPI deeply before designing proprietary charging interfaces.

## OCPP

OCPP standardizes communication between charging stations and charging management systems.

Enigma should normally integrate above this layer rather than attempting to replace charger control infrastructure.

## OICP

OICP is associated with Hubject's interoperability ecosystem and is relevant when evaluating roaming-hub integrations.

## ISO 15118

ISO 15118 governs vehicle-to-charger communication and includes Plug & Charge capabilities.

It matters because the long-term user experience should minimize manual authentication.

## Payment standards

Payment architecture must be evaluated separately from charging protocols. A charging protocol does not automatically solve merchant acquiring, refunds, KYC, fraud, tax, reconciliation, or regulated payment operations.

## Data standards

Investigate:

- station identifiers
- EVSE identifiers
- connector identifiers
- vehicle identifiers
- location schemas
- tariff models
- CDR structures
- currency and tax representations
- timestamps and time zones
- status vocabularies.

## Enigma approach

Build a canonical internal domain model and maintain protocol adapters at the edge.

Do not make the internal model a one-to-one copy of one external standard.

## Research requirement

Every protocol integration must document:

- version
- supported endpoints
- authentication
- rate limits
- webhook/event semantics
- error behavior
- idempotency
- data freshness
- commercial prerequisites
- certification requirements
- regional limitations.