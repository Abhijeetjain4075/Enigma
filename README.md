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
- docs/audit-2026-09-30-v2.md
- docs/research-evidence-model.md
- docs/research-backlog.md
- docs/research-sources.md
- docs/standards-evidence.md
- docs/competitive-matrix.md
- docs/competitive-pressure-2026.md
- docs/domain-expansion.md
- docs/non-goals.md

### Architecture and transaction model

- docs/architecture.md
- docs/canonical-model.md
- docs/transaction-state-machine.md
- docs/authorization-policy.md
- docs/ledger-reconciliation.md
- docs/api-contract.md
- docs/data-provenance.md
- docs/tenant-and-multitenancy.md
- docs/partner-onboarding.md
- docs/testing-conformance.md
- docs/integration-contract.md
- docs/error-taxonomy.md
- docs/observability.md

### Standards, security, and regulation

- docs/standards.md
- docs/security-privacy.md
- docs/security-threat-model.md
- docs/consent-and-data-governance.md
- docs/governance.md
- docs/launch-readiness.md
- docs/glossary.md
- docs/adr-0001-platform-boundary.md
- docs/adr-0002-charging-wedge.md
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


## Deep audit and competitive research

The latest research pass is recorded in:

- docs/audit-2026-09-30-v3.md
- docs/competitive-system-map-2026.md
- docs/competitive-strategies-2026.md
- docs/competitive-evidence-register-2026.md
- docs/residual-gap-hypotheses.md
- docs/research-methodology-2026.md
- docs/implementation-blueprint.md

These documents deliberately distinguish public evidence from hypotheses and unverified capabilities. The competitive analysis covers roaming hubs, clearing, eMSPs, CPMS/CSMS, charging-data providers, Plug & Charge trust infrastructure, energy/flexibility systems, toll interoperability, and regulatory data infrastructure.

## Current implementation warning

Enigma is not yet a production interoperability service. The repository currently contains a research and architecture foundation. The next validation step is executable transaction orchestration with a deterministic provider simulator, protocol fixtures, evidence capture, reconciliation, automated tests, and then one authorized real provider or sandbox.

## Fresh external evidence

Key current sources include:

- Hubject intercharge: https://www.hubject.com/intercharge-overview
- GIREVE: https://www.gireve.com/
- e-clearing.net: https://www.e-clearing.net/
- ChargeHub Passport Hub: https://chargehub.com/en/ev-business-solutions/passport-ev-roaming-hub
- Plugsurfing: https://plugsurfing.com/network
- Driivz: https://driivz.com/solutions/electric-vehicle-service-provider/
- AMPECO: https://www.ampeco.com/ev-charging-platform/ev-roaming/
- Monta: https://monta.com/en/
- E-Flux by Road: https://www.e-flux.io/products/roaming
- Statiq EVlinq: https://www.statiq.in/ev-charging-software/evlinq
- Numocity: https://www.numocity.com/
- CIRRANTIC: https://actions.cirrantic.com/integration-data
- Eco-Movement: https://www.eco-movement.com/eco-movement-enhances-global-charging-data-with-direct-payment-capabilities-via-cariqa-partnership/
- OCPI: https://github.com/ocpi/ocpi
- OCPP: https://openchargealliance.org/protocols/
- EU AFIR data rules: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202500655
- EU Common European Access Point research: https://op.europa.eu/en/publication-detail/-/publication/132a219e-f3f5-11ef-b7db-01aa75ed71a1/language-en
- NPCI NETC/FASTag: https://www.npci.org.in/product/netc/about-netc


## Adversarial audit v4

The 2026-09-30 v4 audit added:
- adversarial competitive universe expansion
- open-source implementation audit
- current OCPI/OCPP/ISO 15118 evolution
- EU AFIR/CEAP data-layer analysis
- India aggregation falsification
- reproducible experiment protocols
- explicit hard-stop criteria

See:
- docs/audit-2026-09-30-v4.md
- docs/competitive-universe-expansion-2026.md
- docs/open-source-competitive-audit-2026.md
- docs/experiment-protocols-2026.md
- docs/standards-update-2026.md

The central research question remains: what measurable residual transaction or orchestration problem survives after existing roaming hubs, CPMS/CSMS, eMSPs, data providers, payment infrastructure, open-source systems and regulatory data layers are composed?

Enigma must prove that residual gap experimentally before claiming a moat.
