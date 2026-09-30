# Competitive Pressure Update — 2026-09-30

## Why this update exists

The current web audit found that several capabilities previously treated as possible Enigma differentiation are already offered by established players. This materially changes the strategic bar.

## Directly overlapping capabilities

### Hubject

Hubject's intercharge describes a shared eRoaming network connecting CPOs and eMSPs, with automated authorization and settlement.

Source:
https://www.hubject.com/intercharge-overview

### Plugsurfing

Plugsurfing currently markets APIs and managed roaming for businesses, including Roam OCPI and Drive API. Its 2026 material describes roaming operations, CPO connectivity, tariffs, CDRs, invoicing and network operations.

Sources:
https://plugsurfing.com/api
https://plugsurfing.com/blog/roam-ocpi-in-action-electra/
https://plugsurfing.com/blog/roaming-operations-interview-aaron-rubenstein/

### ChargeHub

ChargeHub operates consumer and B2B roaming/connectivity products. Its 2026 material describes Passport Hub, eMSP/CPO connectivity, payments, roaming sessions and API/business solutions.

Sources:
https://chargehub.com/en/
https://chargehub.com/en/ev-charging-news/2025-ev-roaming-year-in-review

### GIREVE

GIREVE documents eMIP for roaming authorization, clearing-house functions and charging-point data, and supports OCPI.

Sources:
https://www.gireve.com/wp-content/uploads/2022/09/Gireve_Tech_eMIP-V0.7.4_ProtocolDescription_1.0.14-en.pdf
https://www.gireve.com/ocpi-2-2-1-is-now-available-on-gireves-platform/

### Last Mile Solutions

Last Mile Solutions publishes roaming tariff and CDR operational information and supports OCPI roles across CPO/eMSP/hub contexts.

Source:
https://www.lastmilesolutions.com/roaming-information/

### India

IONAGE markets a hardware-agnostic software layer, roaming enablement through IONAGE Nexus, and multi-platform connectivity.

Source:
https://www.ionage.in/why-ionage

Numocity markets an EV charging and energy-management platform for CPOs, eMSPs, fleets and utilities, including roaming and interoperability.

Sources:
https://www.numocity.com/
https://www.numocity.com/solutions

## Strategic consequence

The following are **not safe standalone moats**:

- multi-network charger discovery
- OCPI connectivity
- managed roaming
- CPO/eMSP authorization
- CDR handling
- tariff normalization
- payment integration
- basic reliability dashboards
- "one API to many chargers"

Existing products already cover combinations of these capabilities.

## The remaining strategic question

Enigma needs a problem that is difficult even after a company adopts a roaming hub, eMSP platform, CSMS, OEM platform, or direct OCPI integration.

Candidate research areas:

1. Cross-provider transaction assurance with independently verifiable evidence.
2. A provider-neutral capability graph spanning multiple mobility domains, not just charging.
3. Cross-domain transaction orchestration where charging, parking, tolling and vehicle services participate in one journey.
4. Neutral reconciliation across multiple commercial relationships rather than one roaming network's own clearing process.
5. Portable authorization/delegation across providers and applications.
6. Reliability intelligence derived from independent cross-network transaction outcomes.
7. A developer abstraction that can combine multiple existing roaming hubs rather than replacing them.
8. Neutral routing of a requested outcome across competing providers based on capability, price, reliability, contractual permissions and user policy.
9. Evidence-based transaction recovery when provider state is uncertain.
10. A protocol-agnostic transaction graph for mobility and energy.

## Important correction

Even these candidate areas are hypotheses. They must be tested against existing products before being described as unique.

## Competitive research rule

Every future Enigma strategy claim must answer:

**Who already does this? What exact capability do they provide? What remains unsolved after using their product? Why would a customer pay Enigma instead of combining existing products?**

This is now a mandatory research gate.
