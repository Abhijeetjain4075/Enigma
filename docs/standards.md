# Standards and Protocol Strategy

## Principle

Reuse existing standards wherever they provide adequate interoperability. Do not create a new protocol merely to rename an existing capability.

## EV charging protocol stack

### OCPI

OCPI is the principal open interface to investigate for CPO/eMSP roaming and related interoperability.

The official OCPI repository currently identifies **OCPI 2.3.0** as the latest official release. OCPI modules cover locations, tariffs, tokens, sessions, CDRs, commands, charging profiles and hub connectivity.

Sources:
- https://github.com/ocpi/ocpi
- https://ocpi-protocol.com/

Enigma must support versioned adapters and must not assume that every provider implements the same OCPI version or optional module set.

### OCPP

OCPP standardizes communication between charging stations and central systems. OCA currently documents OCPP 1.6, 2.0.1 and 2.1.

OCPP 2.1 adds functionality including ISO 15118-20 support, bidirectional charging, DER control, battery swapping, local cost calculation and expanded authorization/payment options.

Enigma should normally integrate above the CSMS/charger-control layer rather than replacing OCPP infrastructure.

Sources:
- https://openchargealliance.org/protocols/
- https://openchargealliance.org/faq/

### OICP

OICP is associated with Hubject's interoperability ecosystem and should be treated as a versioned external roaming protocol when Hubject integrations are evaluated.

Source:
https://www.hubject.com/company/download

### ISO 15118

ISO 15118 governs EV-to-EVSE communication and supports automated authentication/Plug & Charge concepts as well as bidirectional energy-transfer use cases.

ISO 15118-20:2022 is current and has a 2026 amendment in the ISO catalogue.

Sources:
- https://www.iso.org/standard/77845.html
- https://www.iso.org/ics/43.120/x/

## Regulatory data interfaces

EU AFIR introduces machine-readable data/API and national-access-point requirements for publicly accessible alternative-fuels infrastructure. Enigma must treat regulatory data access as a separate ingestion pathway from commercial roaming.

Source:
https://eur-lex.europa.eu/eli/reg/2023/1804/oj/eng

## Payment standards and rails

Payment architecture must be evaluated separately from charging protocols.

A charging protocol does not automatically solve:

- merchant acquiring
- payment aggregation
- KYC/AML
- fraud
- refunds
- chargebacks
- tax
- invoicing
- safeguarding
- reconciliation
- cross-border settlement.

Enigma should prefer licensed payment partners where appropriate rather than assuming it can itself hold or route regulated funds.

## Canonical data model

Maintain canonical models for:

- Provider
- Asset
- EVSE
- Connector
- Vehicle
- Identity
- Token
- Authorization
- Tariff
- Session
- CDR
- Transaction
- MoneyMovement
- Settlement
- Evidence
- Contract
- Journey.

External identifiers must include namespace, issuer/provider, value, validity, and verification/provenance.

## Adapter requirements

Every integration must document:

- protocol/API name and version
- supported endpoints/modules
- authentication
- rate limits
- webhook/event semantics
- retry semantics
- idempotency
- error mapping
- data freshness
- commercial prerequisites
- certification/conformance requirements
- regional limitations
- data-protection implications.

## Version policy

External standards evolve independently from Enigma.

Every adapter must pin its external version. Internal canonical contracts must remain stable where possible.

Breaking external changes require:

1. adapter versioning
2. contract tests
3. migration plan
4. compatibility evidence
5. rollback/deprecation strategy
