# Enigma Provider Compatibility Research — 2026-10-01

This document records current public evidence relevant to the no-Enigma-hosted-backend thesis. Public documentation is not provider authorization.

## Core protocol evidence

OCPI 2.3.0 is the current official OCPI release. OCPI explicitly covers authorization, locations, sessions, CDRs, tariffs, tokens and commands. Its credentials module exchanges HTTP authorization tokens between platforms and its version endpoint advertises server endpoints. This means an OCPI integration is fundamentally a platform-to-platform integration, not inherently a mobile-client protocol.

Sources:
- https://github.com/ocpi/ocpi
- https://github.com/ocpi/ocpi/blob/2.3.0/release/core/credentials.asciidoc
- https://github.com/ocpi/ocpi/blob/2.3.0/release/core/version_information_endpoint.asciidoc
- https://github.com/ocpi/ocpi/blob/2.3.0/release/core/mod_cdrs.asciidoc
- https://github.com/ocpi/ocpi/blob/2.3.0/release/core/mod_sessions.asciidoc

OCPI also explicitly describes recovery after communication loss through re-synchronization/pull. This supports Enigma's event/evidence/reconciliation model, but does not remove the need for an endpoint when a party is acting as an OCPI platform.

## Candidate integration paths

| Candidate | Public technical evidence | Backendless implication | External dependency |
|---|---|---|---|
| Hubject / intercharge | OICP 2.3 documentation and QA environment are public; Hubject says service requests are processed when a valid CPO/EMP contract exists. | Direct consumer-to-Hubject is not the normal trust boundary. Enigma can operate as a partner platform/node; an endpoint is required for applicable flows. | Contract, partner role, credentials/certificates, endpoint, QA onboarding |
| GIREVE | Public OCPI 2.2.1 integration guide; HTTPS, endpoint exchange, IP filtering and mutual TLS are documented. | Strong evidence against pure mobile-only direct mode for this integration path. Customer/operator node or relay is appropriate. | Roaming agreement, HTTPS endpoint, IP allowlist, certificates/tokens |
| e-clearing.net | Public support documentation says OCPI/OCHP are supported and describes a dedicated testing environment for partners. | Partner-platform model. Enigma protocol can remain backend-independent while an operator node provides the required endpoint. | Partner onboarding, test access, credentials, integration endpoint |
| Plugsurfing | Public Drive API and Roam OCPI products. Roam OCPI uses API-key credentials and exposes locations/sessions/CDRs; status can be pulled at intervals. | A client-facing Drive API may permit a thinner client path depending on contract, but Roam OCPI remains platform-to-platform. | Product agreement, API credentials, rate limits, contractual scope |
| ChargeHub / Passport Hub | Public Passport Hub integration prerequisites include live public stations, location/tariff/session APIs and a roaming agreement. Separate ChargeHub POI API exists for data. | Passport is a managed roaming hub, not evidence for a backendless direct transaction path. Enigma can integrate as an operator platform/node. | Roaming agreement, API access, working eMSP/CPO capabilities |

## Hubject

Hubject states that exchange between Hubject and eMobility/charge-point backends uses REST APIs and that service requests require a valid contract. Its QA environment is explicitly for testing and its production environment is for live eRoaming/financial transactions.

Sources:
- https://support.hubject.com/hc/en-us/articles/13833641509277-Hubject-Portal-101
- https://github.com/hubject/oicp
- https://support.hubject.com/hc/en-us/articles/11903831472925-CPO-Integration-Checklist

## GIREVE

GIREVE's current public OCPI guide states that connections exchange tokens and endpoints and that HTTPS is required. It also documents IP filtering and client certificates. The guide explicitly describes communication between the partner's backend and GIREVE's platform.

Source:
- https://www.gireve.com/wp-content/uploads/2025/01/Gireve_Tech_OCPI-V2.2.1_ImplementationGuide_V1.2-_en.pdf

## e-clearing.net

e-clearing.net states that it supports OCPI and OCHP and provides a dedicated testing environment for integration partners.

Sources:
- https://www.e-clearing.net/customer-support
- https://www.e-clearing.net/starter-package

## Plugsurfing

Plugsurfing publicly documents two distinct integration products: Drive API and Roam OCPI. Roam OCPI uses an API key exchanged through the OCPI Credentials handshake and exposes globally unique location, session and CDR identifiers. Plugsurfing's documentation also states that Roam OCPI is a managed roaming integration and that Plugsurfing handles agreements, communication and invoicing with CPOs.

Sources:
- https://developer.plugsurfing.com/docs/plugsurfings-apis
- https://developer.plugsurfing.com/docs/accessing-the-api
- https://developer.plugsurfing.com/docs/about-roam-ocpi

## ChargeHub

ChargeHub publicly documents Passport Hub integration prerequisites and a standard roaming agreement. Its separate developer portal documents POI and dynamic-status APIs.

Sources:
- https://chargehub.com/en/ev-business-solutions/passport-ev-roaming-hub
- https://developer.chargehub.com/

## OCPP boundary

OCPP is a standardized communication protocol between charging stations and central systems. OCPP 2.1 is the current major release, while OCPP 2.0.1 remains a major deployed/certified version. OCPP therefore does not by itself solve Enigma's provider/eMSP interoperability problem; it primarily standardizes charge-point-to-central-system communication.

OCPP 2.0.1 moved transaction-ID generation to the charging station and added sequence-based transaction events, which is particularly relevant to Enigma's portable event-history model.

Sources:
- https://openchargealliance.org/protocols/open-charge-point-protocol/
- https://openchargealliance.org/ocpp-info-whitepapers/what-is-new-in-ocpp-2-0-1/
- https://openchargealliance.org/new-editions-of-ocpp-2-1-and-2-0-1-now-available/
- https://openchargealliance.org/ocpp-info-whitepapers/security-operations-guide/

## Architecture conclusion from current evidence

The evidence does **not** support the claim that Enigma can eliminate backend infrastructure for every provider.

It **does** support a stronger and more precise architecture:

**Enigma protocol is backend-independent; deployment infrastructure is provider-dependent.**

The protocol should therefore be implemented once and carried by:

1. a consumer/device SDK;
2. a provider adapter at the edge;
3. a customer/operator node when provider credentials or inbound endpoints require it;
4. an optional relay where neither the client nor operator can host the required integration endpoint.

Enigma itself does not need to own the database, queue, webhook endpoint or credential store in order for the protocol to work.

## Immediate falsification target

The next research/engineering proof is not another generic simulator.

It is to implement one real protocol adapter against an authorized sandbox and determine empirically:

- which credentials must be server-held;
- whether the provider requires an inbound callback endpoint;
- whether the customer can run that endpoint;
- whether a client can safely perform the transaction directly;
- which provider evidence can be carried in the Enigma event/evidence bundle;
- whether provider reconciliation can be completed bilaterally.

No public documentation alone establishes these permissions.
