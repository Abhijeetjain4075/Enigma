# Enigma

> Software interoperability for the world around movement, vehicles, energy, services, and transactions.

Enigma is a software-only platform concept inspired by the role UPI plays in payments: create a common digital interoperability layer without owning the underlying banks, chargers, vehicles, parking infrastructure, toll infrastructure, service businesses, or energy assets.

## Core thesis

The original observation was simple: an EV driver can encounter fragmented charging networks, each with its own app, account, wallet, authentication flow, pricing, and payment experience.

The deeper opportunity is broader:

**Do not build another charging network. Build software that makes independent networks and services interoperable.**

Charging is an entry point, not the boundary.

## What Enigma may connect

- EV charging networks
- Battery swapping
- Home charging
- Parking
- Tolls
- Navigation and journey services
- Vehicle servicing and maintenance
- Roadside assistance
- Parts and service marketplaces
- Rentals and mobility
- Fleet operations
- Insurance integrations
- Financing integrations
- Energy, solar, storage, and grid services
- Vehicle and mobility data
- Payments, billing, identity, authorization, and settlement

## Product layers

1. Universal identity - identity for people, vehicles, organizations, and service relationships.
2. Authorization - permission to access a service without forcing users through separate provider flows.
3. Payment and settlement - transaction orchestration, billing, reconciliation, refunds, and provider settlement.
4. Interoperability API - one software interface across fragmented providers and protocols.
5. Orchestration - coordinate multi-step mobility and energy workflows.
6. Trust and intelligence - normalize data and expose reliability, pricing, compatibility, and operational signals.
7. Interfaces - consumer app, OEM integrations, fleet software, partner APIs, SDKs, and embedded experiences.

## Design principle

The user should think in terms of an outcome:

> I need to charge, park, travel, maintain my vehicle, or solve a journey problem.

The user should not need to understand which underlying provider operates every component.

## Important distinction

Enigma is **software-only**. It does not require owning or manufacturing:

- chargers
- vehicles
- batteries
- parking hardware
- toll hardware
- energy infrastructure

The platform connects software systems and commercial participants.

## Initial direction

The strongest initial wedge to investigate is EV charging interoperability, because it exposes the fundamental fragmentation problem:

**discovery -> availability -> compatibility -> authorization -> session -> payment -> billing -> settlement -> trust**

The longer-term thesis is to generalize the same interoperability model across mobility, vehicle services, and energy.

## Competitive reality

The one app for multiple charging networks proposition already exists in multiple forms. Enigma therefore must not rely on generic aggregation as its differentiation.

The repository now treats the strategic problem as **transaction interoperability plus evidence, reliability, programmable integration, and cross-domain orchestration**, subject to empirical validation.

## Status

Concept and research repository. No production product or universal network is implied.

## Repository map

### Strategy and research

- docs/vision.md
- docs/problem.md
- docs/competitive-landscape.md
- docs/competitive-matrix.md
- docs/strategy.md
- docs/ideas.md
- docs/open-questions.md
- docs/decision-framework.md
- docs/research-sources.md
- docs/audit-2026-09-30.md

### Architecture and transaction model

- docs/architecture.md
- docs/canonical-model.md
- docs/transaction-state-machine.md
- docs/integration-contract.md
- docs/error-taxonomy.md
- docs/observability.md

### Standards, security, and regulation

- docs/standards.md
- docs/security-privacy.md
- docs/regulatory.md
- SECURITY.md
- CONTRIBUTING.md

### Product and economics

- docs/scope.md
- docs/business-model.md
- docs/roadmap.md
- docs/metrics.md

## Guiding rule

Do not confuse a large feature list with a coherent platform.

Every future capability should answer:

1. What fragmented system does it connect?
2. What common identity, capability, service, or transaction does it expose?
3. Why does interoperability create value?
4. Who pays for the software?
5. What evidence proves the operation works?
6. What regulatory responsibility attaches to the flow?
7. What becomes harder to replicate as the network grows?
