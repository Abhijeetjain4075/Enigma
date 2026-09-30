# Competitive System Map — 2026-09-30

## Purpose

This document maps the ecosystem by function rather than treating every company as a direct competitor.

## Layer A — Infrastructure operators

Charge Point Operators own/operate charging sites and equipment. Their incentives include utilization, uptime, revenue, roaming reach, energy cost, site economics, and service quality.

Enigma must not assume that CPOs want to be disintermediated. Existing roaming systems generally sell them additional demand and connectivity.

## Layer B — Charging management / CPMS

Examples evidenced in current research include Driivz, AMPECO, Monta, Numocity, Statiq/EVlinq and others.

Typical capabilities include:

- OCPP connectivity
- charger monitoring/control
- tariffs
- users
- sessions
- payments
- roaming
- APIs
- energy management
- fleet workflows

Driivz explicitly supports Hubject, GIREVE and e-clearing.net integrations plus direct OCPI roaming. AMPECO supports OCPI/OICP roaming. Monta supports roaming hubs, direct OCPI, settlement, APIs and energy/grid workflows. Numocity positions its platform across charging, roaming, fleets and distributed energy. Statiq positions EVlinq as a roaming platform.

Sources:
- https://driivz.com/solutions/electric-vehicle-service-provider/
- https://www.ampeco.com/ev-charging-platform/ev-roaming/
- https://monta.com/en/
- https://www.numocity.com/
- https://www.statiq.in/ev-charging-software/evlinq

## Layer C — Roaming hubs / clearing

Major documented systems include Hubject/intercharge, GIREVE, e-clearing.net, ChargeHub Passport Hub and Plugsurfing's Roam OCPI model.

They reduce bilateral integration complexity and can cover authorization, session exchange, tariffs, CDRs, commercial agreements, settlement/reconciliation and support.

Sources:
- https://www.hubject.com/intercharge-overview
- https://www.gireve.com/
- https://www.e-clearing.net/
- https://chargehub.com/en/ev-business-solutions/passport-ev-roaming-hub
- https://plugsurfing.com/network

## Layer D — eMSPs / consumer access

Examples include Plugsurfing, ChargePoint, ChargeHub, Chargemap, Elli, Electroverse and other regional providers.

The common pattern is a user-facing identity/account/app/card with access to many external networks.

ChargePoint documents roaming partner access from its app. Plugsurfing documents more than one million charging places across Europe through CPO partners.

Sources:
- https://www.chargepoint.com/drivers/roaming
- https://support.plugsurfing.com/hc/en-us/articles/11002094199453-What-is-Plugsurfing

## Layer E — data aggregation / navigation

CIRRANTIC and Eco-Movement illustrate a separate but adjacent layer: normalized charging content, availability, prices, enrichment and reliability indicators for maps, navigation, in-car and digital platforms.

Sources:
- https://actions.cirrantic.com/integration-data
- https://www.eco-movement.com/eco-movement-enhances-global-charging-data-with-direct-payment-capabilities-via-cariqa-partnership/

## Layer F — Plug & Charge / trust infrastructure

Hubject and GIREVE operate Plug & Charge/PKI capabilities. A 2025 Hubject-GIREVE-Irdeto partnership described interoperability across their Plug & Charge ecosystems.

Sources:
- https://www.hubject.com/products/plug-and-charge
- https://www.gireve.com/plug-and-charge-services/
- https://www.gireve.com/gireve-hubject-irdeto-form-strategic-partnership-to-expand-plug-charge-network-access/

## Layer G — regulatory/open data

The EU AFIR framework requires public alternative-fuels infrastructure data availability and API access. EU implementing rules specify data formats and update expectations, including dynamic data updates no later than one minute after a change and static data no later than 24 hours after a change. The planned Common European Access Point adds another public-data layer.

Sources:
- https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202500655
- https://op.europa.eu/en/publication-detail/-/publication/132a219e-f3f5-11ef-b7db-01aa75ed71a1/language-en

## Layer H — payments and settlement

Charging systems can use existing payment infrastructure, wallets, cards, bank rails and provider-specific settlement. Roaming hubs often sit between technical events and commercial settlement.

The Enigma design must avoid assuming that “payment API” equals “regulated payment business.” Regulatory perimeter, money flow, custody, merchant-of-record status and settlement obligations must be explicitly modelled.

## Layer I — energy and flexibility

Charging software increasingly overlaps with load management, smart charging, V2G and grid flexibility. Numocity, Monta, Electric Miles and ev.energy illustrate the convergence.

Sources:
- https://www.numocity.com/
- https://monta.com/en/
- https://electricmiles.com/
- https://www.ev.energy/platform/overview

## Layer J — adjacent mobility transactions

Parking, tolls, rentals, maintenance, roadside assistance and MaaS systems can be interoperable domains, but each introduces separate identities, contracts, liability, pricing, regulatory and operational semantics.

India's NETC/FASTag is an important architectural comparator: NPCI describes interoperable toll payment with clearing, settlement and dispute management across toll plazas.

Sources:
- https://www.npci.org.in/product/netc/about-netc

## Critical system insight

Enigma is not entering an empty “app fragmentation” market. It would sit above a stack containing:

`hardware -> CPO/CSMS -> roaming/clearing -> eMSP/OEM -> data/navigation -> payment/settlement -> energy/regulatory systems`

The residual opportunity, if any, must therefore be demonstrated at the boundaries between these layers.
