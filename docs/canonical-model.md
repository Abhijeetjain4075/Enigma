# Enigma Canonical Domain Model

## Purpose

External protocols differ. Enigma requires a canonical internal model that represents business meaning without copying one external protocol.

## Core entities

### Party

A person or legal/organizational actor.

Fields:

- party_id
- party_type
- legal_name
- jurisdiction
- status
- created_at

### Identity

A credential or identifier used to recognize a party, vehicle, application, fleet member, or delegated principal.

Identity is not the same thing as authentication.

### Vehicle

Represents a vehicle known to Enigma.

Important fields:

- vehicle_id
- vehicle_type
- make/model where permitted
- capabilities
- connector capabilities
- battery/energy characteristics where legitimately available
- owner/controller relationship
- identifiers with provenance

### Asset

A physical or logical service asset.

Examples:

- charging station
- EVSE
- connector
- parking bay
- tolling endpoint
- service location
- battery-swap station

### Provider

A service operator, owner, mobility service provider, eMSP, CPO, OEM, fleet service, payment provider, or other participant.

### Capability

A provider-supported operation with explicit scope and evidence.

Examples:

- discover
- quote
- reserve
- authorize
- start
- stop
- monitor
- bill
- refund

### Service

A user-facing or business-facing service definition.

### Session

An instance of a service being performed.

For charging this may represent the charging session. For parking it may represent a parking stay.

### Transaction

The commercial and operational envelope around a service session.

A transaction can contain multiple provider operations.

### Money movement

A separate model for:

- authorization
- capture
- refund
- chargeback/dispute
- fee
- tax
- payable
- receivable
- settlement

### Contract

The commercial authorization under which two participants can transact.

### Journey

A sequence of services associated with a trip or operational objective.

### Evidence

An observation supporting a state, price, capability, or transaction outcome.

Evidence should include:

- source
- observed_at
- received_at
- expires_at where applicable
- provenance
- confidence
- correlation identifier

## Key relationships

Person -> controls -> identity

Identity -> authorizes -> operation

Person/organization -> controls -> vehicle

Provider -> owns/operates -> asset

Provider -> exposes -> capability

Capability -> implemented_by -> adapter

Transaction -> contains -> session

Transaction -> causes -> money movements

Operation -> produces -> evidence

Journey -> contains -> services and transactions

## Design rule

No universal identifier should be assumed merely because two systems use a similar-looking ID.

External identifiers must be stored with:

- namespace
- issuer/provider
- identifier
- validity period
- verification state

## Privacy rule

The canonical model must separate:

- identity data
- operational data
- financial data
- location data
- telemetry
- derived intelligence

A feature should request the minimum category needed to perform its operation.

## Extensibility

New domains should reuse stable primitives:

Provider, Asset, Capability, Identity, Authorization, Service, Session, Transaction, MoneyMovement, Evidence, Contract, Journey.

Do not create an entirely new domain architecture for every adjacent service.
