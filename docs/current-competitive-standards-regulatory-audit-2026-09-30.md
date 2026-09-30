# Enigma current competitive, standards and regulatory audit

**Retrieval date:** 2026-09-30

**Scope:** Public primary-source review of commercial e-mobility platforms, roaming hubs, CPMS/CSMS products, open-source substitutes, protocols, payment/security standards, and selected EU/India/U.S. regulatory material.

> **Important evidence boundary.** This report is not a product certification, legal opinion, penetration test, conformance test, financial audit, or production-readiness assessment. Public-source review **cannot verify private contract capabilities, legal compliance, certification scope, tenant configuration, commercial entitlement, or real integration behavior**. A vendor's marketing claim is not independent evidence. **Enigma is not called production ready anywhere in this report; it should not be treated as production ready on the basis of this review.** “Not publicly verified” means exactly that—not absent.

## 1. Executive synthesis

The market separates into four materially different layers:

1. **Roaming/interoperability brokers:** Hubject/intercharge/OICP, GIREVE, e-clearing.net, ChargeHub Passport Hub, Plugsurfing Roam OCPI, GreenFlux roaming, Monta managed roaming, EVlinq, NumoHub and similar products connect CPOs and EMPs. They are not interchangeable with a charger-authoritative transaction ledger.
2. **CPMS/CSMS and operational platforms:** Driivz, AMPECO, Last Mile Solutions, E-Flux by Road, chargecloud, Virta, GreenFlux, ChargeLab, ChargePilot, Noodoe, EV Connect, AmpUp, OpenCPO, CitrineOS, EVtivity, SteVe and others cover some combination of OCPP termination, station control, authorization, sessions, billing, reports and partner integration.
3. **eMSP/access and payment facades:** Chargemap, Electroverse, Elli, Allego, IONAGE and Plugsurfing expose driver access, app/RFID/Plug & Charge and consumer billing, while depending on CPO-supplied data and partner contracts.
4. **Standards and regulatory overlays:** OCPI, OICP, OCPP, ISO 15118/Plug & Charge, AFIR, DPDP, RBI/NETC, U.S. federal/state rules, PCI DSS, OAuth/OIDC, OpenAPI/AsyncAPI and CloudEvents define portions of an interoperability, privacy, payment-security or public-data control plane—but do not, alone, provide a complete refund, dispute, settlement, CDR, or legally admissible evidence system.

### Bottom-line audit finding

A credible Enigma architecture must keep the following bounded and separately evidenced:

- **Protocol termination:** OCPP, OCPI, OICP, eMIP, OCHP and ISO 15118/PKI are different surfaces. Version and profile negotiation must be explicit.
- **Authorization:** RFID/token, app/remote, Plug & Charge, guest and real-time/offline authorization have different trust and failure semantics.
- **Session and metering evidence:** source operator, meter values, session IDs, CDRs, late arrivals, corrections, credit CDRs and signed data must retain lineage.
- **Commercial ledger:** tariffs, taxes, pre-authorizations, captures, invoices, credit notes, payouts, refunds, chargebacks and settlement finality cannot be inferred from a session API or “automated settlement” claim.
- **Reliability/evidence:** status pages, product claims, protocol logs, webhook signatures and uptime targets are not the same as an independent SLA, immutable audit trail or metrology certification.
- **Regulatory controls:** legal requirements are jurisdiction- and role-specific. Protocol conformance does not establish payment, privacy, accessibility, tax, consumer-protection or financial-services compliance.

## 2. Evidence levels and interpretation

| Level | Meaning | Permitted conclusion |
|---|---|---|
| **A — Normative primary source** | Regulation, official standard/specification, official API/OpenAPI, official project source/release | The cited requirement or interface is publicly documented, subject to edition/version and implementation caveats. |
| **B — Official implementation/product documentation** | Vendor technical guide, support article, official repository README, official status page | The vendor/project publicly states the behavior or interface; implementation, entitlement and runtime behavior remain unverified. |
| **C — Official product/marketing/legal statement** | Product page, announcement, terms, FAQ, customer story | A public claim or contractual statement exists; it is not independent technical or legal assurance. |
| **D — Not publicly verified** | No authoritative public evidence in the supplied successful results | Treat as an explicit gap; do not infer absence or presence. |

**Source weighting rules:** legal obligations are sourced to official legal texts where available; standards are not laws unless incorporated; vendor certifications are not treated as verified scope unless the certificate/attestation and applicability are public; a public API description is not proof that Enigma has access or that a particular tenant has enabled it.

## 3. Cross-subject capability matrix

Legend: **V** = publicly verified at the level stated; **C** = conditional/claim or profile-specific; **U** = not publicly verified; **N/A** = not a product capability for a standards/regulatory subject.

| Subject | Role | API / SDK | Auth | Cross-domain / delegation | Evidence / reliability | Payment / settlement | Protocols | Sessions / CDR | Refund / dispute / recon. |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Hubject intercharge | Roaming broker + optional Financial Services | V docs/code; SDK U | V | V routing; general delegated authority U | V monitoring; independent SLA U | V clearing claims; base inclusion/funds U | OICP 2.3 V | V CDR / 90-day recovery | partial invoice correction; refunds/chargebacks U |
| GIREVE | Roaming/clearing hub | V eMIP/OCPI/API workspace; SDK U | V OAuth/flows | V hub + PKI trust; general delegation U | V published 99.85% target; independent U | V clearing/invoices; PSP/funds U | eMIP 1.0.17, OCPI 2.2.1 V | V sessions/CDRs/BOOST | V CDR disputes; consumer refunds/chargebacks U |
| e-clearing.net | Roaming/data clearing hub | Specs/WSDL; product API U | V OCHP_direct TLS/basic | V OCHP_direct; general federation U | Monitoring claims; SLA/independent U | Data-level only; funds/PSP U | OCHP 1.4, OCHP_direct .2, OCPI claims | V OCHP CDR states | U |
| Plugsurfing | eMSP + managed roaming | V Drive API; SDK U | V API-key/RBAC, tokens | V managed roaming; consent/agency U | V signed webhooks/retries, SLA/status | V two clearing modes/Stripe | Drive proprietary; OCPI 2.2.1 profile | V async sessions/CDRs | refund claim; exact API/chargebacks U |
| Virta | CPMS/eMSP/roaming | V REST/OpenAPI/streaming; SDK U | V OAuth client credentials | V driver-on-behalf-of + roaming | Kafka/Avro controls; SLA/replay U | V payments/VAT/monthly payout claims | REST/Kafka/OCPP/OCPI claims | V sessions/CDRs | disputes/holds partial; general refund/chargeback U |
| Driivz | CPMS/business operations | API marketing; docs gated; SDK U | V app/payment/RFID claims | V hub/P2P/roles; delegation U | V monitoring/security claims; SLA/evidence U | V gateways/invoicing/reports | OCPP 1.6/2.0.1/2.1, OCPI etc claims | V OCPP/meter/CDR claims | U |
| Last Mile Solutions | CPMS/eMSP/finance intermediary | V public REST/OCPI; SDK U | V OAuth + OCPI tokens | V OCPI directional trust; on-behalf-of U | V status/ISO claims; SLA U | V payment, payouts, VAT claims | API, OCPI 2.1.1, OCPP 1.5/1.6 V | V mutable transactions/OCPI CDR | credit-note statuses; refund/chargeback U |
| E-Flux by Road | CPMS/eMSP/roaming/billing | V REST API; SDK U | V JWT/RBAC; ERE OAuth | V multi-tenant roaming; delegation U | V signed at-least-once webhooks; SLA claims conflict | V payment/reimbursement/refund claims | OCPP 2.0.1/2.1, OCPI profile V | V sessions/CDR/settlement correction | overpayment/refund claim; full workflow U |
| AMPECO | CPMS/API/roaming | V OpenAPI v3.256.0; SDK U | V bearer/OAuth | V partner-scoped API/OCPI; general delegation U | V raw logs/audit/webhooks; SLA/retention U | V PSP orchestration/settlement reports | OCPP/OCPI/OICP/OpenADR claims | V rich sessions/CDR v2 | retry/free billing; refund/chargeback API U |
| Monta | CPMS/eMSP/managed + self-managed roaming | V API/OpenAPI/CLI; SDK example only | V OAuth/scopes | V partner/team controls; delegation U | V HMAC webhooks/status; SLA/retention U | managed vs self-managed distinct; funds role conditional | OCPP 1.6J/2.0.1, OCPI, OICP | V export/logs | wallet refund/adjustment V; card disputes U |
| GreenFlux | CPMS/roaming/billing | API claims; SDK/auth/schema U | Header only documented | V tenant/sub-CPO/roaming claims | V ISO/security/99.9% claims; independent U | V payment/roaming settlement claims | OCPP 1.5/1.6/2.0.1, OCPI 2.2.1 | V session/CDR claims | U |
| ChargeLab | CSMS/API | Early-access API; SDK/auth U | App/RFID only public | OCPI 2.2 claim; delegation U | V logs/monitoring/SOC claim; SLA U | V host payouts/roaming separation | OCPP 1.6/2.0.1, OSCP 1.0, OCPI 2.2 | session/report evidence; CDR U | preauth refund V; native disputes U |
| FLO | Network operator/eMSP | API high-level only | App/RFID/guest/P&C | V partner roaming; delegation U | V 98% target/method; independent U | V billing/PCI claim; payout/funds U | OCPP, OCPI, OpenADR, ISO/DIN claims | receipts/session history; CDR U | billing correction/credit; workflow U |
| EV Connect | CSMS/network/eMSP | API claim; catalog/SDK U | App/QR/P&C | V OCPI/open access; delegation U | V 99.9% software term; charger/evidence U | V collection/remittance term; ledger U | OCPP 1.6+/2.0.1, OCPI claims | sessions/reports; CDR U | chargeback mention; refund/dispute U |
| AmpUp | CSMS/payment facilitator | API claim only; SDK U | app/QR/RFID/wallet | roles/groups; cross-network U | 99.9/98.5 claims; independent U | V host payout/processor claims | OCPP claims; versions/OCPI U | telemetry/reports; CDR U | refund policy V; chargeback/recon U |
| Noodoe | CPMS | API feature claim; schema/auth U | QR/app/RFID/membership | Bosch OCPI claim; delegation U | 99.9%/AWS claims; independent U | V Stripe transfer/report fields | OCPP 1.6/2.0.1, OCPI integration | session/roaming CDR IDs | support refund; API/workflow U |
| chargecloud | CPMS/finance/roaming | V OpenAPI/Core v1; SDK U | V OAuth/JWT/API key | V roles/context/roaming; general delegation U | V status/Trust Center; SLA/evidence U | V billing/refund/recon claims | OCPP 1.5/1.6/2.0.1, OICP/OCPI claims | V API sessions/CDR feedback | refunds/credit notes V; chargebacks U |
| ChargePilot | Smart charging/control | V REST/OpenAPI + Push; SDK U | API key, mTLS/OCPP | V third-party CSMS proxy; delegation U | V offline queue/fallback/logs | billing backend boundary only | OCPP 1.6J, Modbus, VDV 463 | V completed events/push | U |
| ChargeHub Passport Hub | Roaming hub | Public data API separate; partner API U | P&C PKI; partner auth U | V OCPI bridge/PKI; agency U | lab/SOC claim; SLA U | V commercial/settlement claims; rails/custody U | OCPI; ISO 15118 | V CDR forwarding | recon claim; refunds/disputes U |
| Chargemap | eMSP/access/business | Business API feature claim; SDK U | Pass/app/Auto/P&C | V roaming/business delegation; authority U | terms evidence; SLA/provenance U | V consumer billing/monthly transfer | OCPI/OCPP/ISO claims | history/reports; CDR schema U | claim/reimbursement; formal workflow U |
| Electroverse | eMSP/roaming/payment facade | API/SDK U | RFID/app/business cards | V business/admin; federation U | CPO source/delayed CDR; SLA U | V preauth/Direct Debit/business billing | protocol support U | CPO CDRs, up to 365-day invoicing | complaints; refund/chargeback U |
| Elli | eMSP/platform | V REST/OpenAPI; SDK U | API key + OAuth/OIDC | V delegated user auth; partner delegation U | V OCPP/status claims; SLA/evidence U | V consumer billing; CPO settlement U | REST/OCPP/Hubject/GIREVE | V remote session; CDR U | U |
| Allego | Network/eMSP/fleet | API/webhook claim; SDK U | app/card/contactless/P&C | partner roaming; delegation U | 99% claim; SLA/evidence U | preauth/monthly invoice claims | ISO 15118-2/OCPP 2.0.1 P&C | receipts/history; CDR U | subscription refunds; charging disputes U |
| IONAGE | India CPMS/eMSP/marketplace | Discovery/OCPI; SDK closed beta | Token A/RBAC; OAuth details U | V OCPI/fleet/white-label; delegation U | 75% case claim; independent U | wallet/settlement claims; rails U | OCPI 2.2.1, OCPP claims | session analytics; CDR U | wallet refund policy V; chargebacks U |
| Eco-Movement | Station data/quality broker | V HTTP/JSON/OCPI APIs; SDK U | token + credentials/OAuth option | V distribution roles; delegation U | V quality/freshness process; SLA U | Data only | OCPI 2.2/2.1.1, DATEX/CSV | U | U |
| CIRRANTIC | Data/visibility + wallet | API/feed claim; details U | DUA/content rights | V authorized distribution; technical delegation U | quality claims; SLA/provenance U | wallet/payment claims; settlement U | OCPI/structured formats | wallet sessions; CDR U | U |
| Statiq EVlinq | India roaming/settlement | API/SDK U | U | OCPI-based, single-agreement claim | encrypted/reliability claims; SLA U | T+1 claim; rail/custody U | OCPI version U | session/CDR U | U |
| Numocity | CPMS/roaming | API claim; SDK U | app/RFID/P&C; API auth U | V CPO/eMSP/OEM/Hubject; delegation U | ISO/monitoring claims; SLA U | settlement/recon claims; rail U | OCPP 1.6/2.0.1/2.1 inconsistency, OCPI U | sessions; CDR U | U |
| NPCI NETC/FASTag | Regulated toll network | member APIs; SDK/public API U | issuer/acquirer scheme auth | closed member network; delegation U | signed/Mapper/hotlist rules; SLA U | centralized clearing/NRCS, T+1 cap | RFID, signed XML/HTTPS | transaction lifecycle, no public CDR | chargeback/arbitration/recon V |
| SteVe | Open-source OCPP CSMS | REST/OpenAPI; SDK U | Basic Auth, OCPP profiles | U | validation/logs; HA/evidence U | U (CSV to external billing) | OCPP 1.2/1.5/1.6 | transactions/meter/CSV | U |
| CitrineOS | Open-source CSMS | REST/GraphQL/OCPI; SDK U | OIDC/RBAC, OCPP profiles | OCPI multitenancy; general delegation U | logs/events/health; SLA U | feature-release claims only; PSP U | OCPP 1.6/2.0.1; 2.1 ambiguous; OCPI 2.2.1 | transactions/CDR/OCPI | U |
| OpenCPO | Open-source CSMS | REST/Redis; SDK U | API key/JWT/mTLS | OCPI roles/tokens; agency U | audit/logs/PKI/fallback | plugin boundary; ledger U | OCPP 1.6j/2.0.1, OCPI 2.2.1, ISO scope | sessions/CDRs/invoices | U |
| EVtivity | Open-source CSMS | REST/OpenAPI 706 endpoints; SDK U | JWT/API key, portal auth | OCPI partner roles; delegation U | audit/health/SSE; SLA U | Stripe payment/recon; inter-operator U | OCPP 1.6/2.1, OCPI 2.2.1/2.3, ISO | sessions/CDRs | refund endpoint V; disputes U |
| gocpp | Open-source Go OCPP library | Go API; SDK is the library | Basic/mTLS callbacks | routing/tenant addons; authority U | schema/telemetry/retry; SLA U | wire schemas only; execution U | OCPP 1.6/2.0.1/2.1 | TransactionStore/meter | U |
| OCPI 2.3.0 | Protocol | HTTP/JSON spec; SDK U | credentials token | bilateral/hub roles; general delegation U | Pull recovery/immutable CDR rule; SLA U | optional Payments/Invoice Recon; rail U | OCPI 2.3.0 current | CPO sessions/CDRs/credit CDR | credit CDR/recon; refunds U |
| OCA/OCPP | Standards alliance | specs/OCTT; runtime SDK U | OCPP profiles | protocol boundary; delegation U | conformance/signed meters; SLA U | payment guidance only | OCPP 1.6/2.0.1/2.1 | transaction/meter; CDR outside scope | U |
| ISO 15118/PKI | Standards/trust plane | OPNC/specs; SDK U | certificates/contract auth | multi-root/CTL ecosystem | ATS excludes reliability | contract billing, not rails | ISO 15118-20/-21 | EV/EVSE messages; CDR U | U |
| EU AFIR/API/CEAP | Regulation/policy | mandatory data/API concept; SDK U | security required; scheme U | NAP/common gateway | 1-min dynamic/24h static, quality | ad-hoc payment/price rules; settlement U | DATEX II/CEN data rules | U | U |
| India DPDP | Privacy law | no EV API/SDK | consent/lawful processing | processor contracts/Consent Manager | logs/backups/breach provisions staged | U | technology-neutral | U | U |
| India RBI PA/NETC boundary | Financial regulation/network | member-only APIs; SDK U | RBI authorization + scheme membership | PA contracts/processor responsibility | RBI/NETC controls | escrow for PA; NRCS separate | NETC member interfaces | no public CDR | refunds/chargeback/recon rules V |
| U.S. EV obligations | Federal/state + standards | covered-project API required; SDK U | ad-hoc/P&C/open access | network switching/OCPI | >97% uptime covered ports | contactless/phone/price rules | OCPP/OCPI/ISO requirements | U CDR | U |
| PCI/NIST/OWASP/RFCs | Security standards | contract/inventory/specs | OAuth/mTLS/signatures guidance | RFC 8705/9421 options | telemetry/signature guidance | PCI scope only | OpenAPI/AsyncAPI/HTTP | U | U |
| API/OAuth/OIDC/CloudEvents | Interface standards | OpenAPI/AsyncAPI/CloudEvents | OAuth/OIDC discovery | standards enable delegation | contracts/claims; delivery U | U | HTTP/events | no CDR semantics | U |

## 4. Subject-level evidence and architectural implications

The following profiles preserve the material capability distinction and link claims to the supplied primary sources. URLs are intentionally kept close to the claims; the cited source links are kept with each profile below; the exhaustive URL register follows in §10.

### Roaming brokers and eMSP intermediaries

- **Hubject intercharge / HBS:** OICP 2.3 is the stated baseline for new implementations; authorization, EVSE data/status, CDR forwarding, signed-metering fields, mTLS/IP controls, process monitoring and 90-day CDR recovery are publicly documented. Hubject Financial Services is separately described from the base roaming layer, so settlement, invoice correction and credit-note capability must be feature-gated. Direct sources: [intercharge](https://www.hubject.com/intercharge-overview), [CPO](https://www.hubject.com/products/intercharge-cpo), [EMP](https://www.hubject.com/products/intercharge-emp), [support implementation](https://support.hubject.com/hc/en-us/articles/4403421095953-2-6-Implementation-of-web-services), [OICP repository](https://github.com/hubject/oicp), [Financial Services](https://hubject-fs.com/).
- **GIREVE:** eMIP and OCPI 2.2.1 documentation, hub dispatch, synchronous/asynchronous authorization, CDR quality and clearing/invoice/payment-status capabilities are public. GIREVE's service-level appendix states 99.85% targets under conditions, but this is a contractual target, not independent evidence; it is not publicly verified as a regulated funds processor. Direct sources: [download index](https://www.gireve.com/download/), [OCPI guide](https://www.gireve.com/wp-content/uploads/2026/09/Gireve_Tech_OCPI-V2.2.1_ImplementationGuide_V1.6-_en.pdf), [eMIP](https://www.gireve.com/wp-content/uploads/2025/02/Gireve_Tech_eMIP-V0.7.4_ProtocolDescription_1.0.17-en.pdf), [roaming](https://www.gireve.com/ev-roaming-services/), [clearing](https://www.gireve.com/clearing-services/), [service level](https://www.gireve.com/wp-content/uploads/2022/09/GIREVE-Subscription-Agreement-1.5.2_Appendix-2-GIREVE-Service-Level-1.5.2.pdf).
- **e-clearing.net:** OCHP 1.4/OCHP_direct 0.2 specifications define authorization lists, CDR states, remote controls and direct partner security tokens; the public product pages do not establish current production compatibility, settlement or a public API/SDK. Direct sources: [home](https://www.e-clearing.net/), [starter](https://www.e-clearing.net/starter-package), [Data Guardian](https://www.e-clearing.net/data-guardian), [OCHP](https://github.com/e-clearing-net/OCHP), [OCHP spec](https://github.com/e-clearing-net/OCHP/blob/master/OCHP.md), [OCHP direct](https://github.com/e-clearing-net/OCHP/blob/master/OCHP-direct.md).
- **Plugsurfing:** Drive API and Roam OCPI are separate. Drive API has server-side API keys, RBAC, HMAC webhooks, request IDs and retries; Roam OCPI is a managed OCPI 2.2.1 profile with pushed tokens/CDRs and configurable real-time authorization fallback. Clearing may be partner-managed or Plugsurfing-PSP/Stripe-managed. Direct sources: [APIs](https://developer.plugsurfing.com/docs/plugsurfings-apis), [Drive](https://developer.plugsurfing.com/docs/about-drive-api), [Roam](https://developer.plugsurfing.com/docs/about-roam-ocpi), [auth](https://developer.plugsurfing.com/docs/authorization), [CDR](https://developer.plugsurfing.com/docs/cdr), [payments](https://developer.plugsurfing.com/docs/payments), [SLA](https://developer.plugsurfing.com/docs/sla), [status](https://status.plugsurfing.com/).
- **ChargeHub / Passport Hub:** public evidence supports an OCPI translator/bridge, Plug & Charge PKI/EMAID flow, CDR forwarding, commercial-flow and reconciliation claims, and lab testing; the public developer portal is a separate POI/status API and does not verify the partner Hub API. Direct sources: [Passport Hub](https://chargehub.com/en/ev-business-solutions/passport-ev-roaming-hub), [P&C](https://chargehub.com/en/ev-business-solutions/plug-and-charge), [RAAR](https://chargehub.com/en/ev-charging-news/plug-and-charge-raar-process), [lab](https://chargehub.com/en/ev-business-solutions/charging-lab), [SOC 2 announcement](https://chargehub.com/en/ev-charging-news/chargehub-soc2-type-ii-certification), [developer portal](https://developer.chargehub.com/).
- **Monta:** managed roaming and self-managed roaming have different money responsibilities. Managed roaming claims billing/settlement; self-managed pages say Monta does not settle or move wallet funds. Public API has OAuth/scopes, HMAC webhooks, CDR exports and operator wallet adjustments, but not a general chargeback API. Direct sources: [API](https://monta.com/en-us/developer-hub/api-and-webhooks/), [developer](https://developer.monta.com/), [auth](https://docs.partner-api.monta.com/reference/ref-authentication), [webhooks](https://developer.monta.com/reference/ref-webhooks), [CDR export](https://developer.monta.com/reference/post-cdr-export), [self-managed outbound](https://monta.com/help/en_US/monta-hub-roaming/emsp-self-managed-outbound-roaming), [self-managed inbound](https://monta.com/help/en_US/monta-hub-roaming/cpo-self-managed-inbound-roaming).
- **EVlinq / Statiq:** EVlinq publicly claims an OCPI-based central roaming layer, unified payments, T+1 settlement and one agreement; no public API, OCPI version, CDR schema, auth or settlement evidence was found. Treat the adjacent Statiq CSMS claims as separate. Direct sources: [EVlinq](https://www.statiq.in/ev-charging-software/evlinq), [about](https://www.statiq.in/about-us), [HPCL announcement](https://statiq.in/blog/2025/12/11/statiq-integrates-5100-hpcl-ev-chargers-into-evlinq-to-expand-indias-ev-charging-network/), [CSMS](https://www.statiq.in/ev-charging-software/csms), [terms](https://www.statiq.in/termsandconditions-page).

### CPMS/CSMS and broad business platforms

- **Virta, Driivz, AMPECO, Last Mile Solutions, E-Flux by Road, GreenFlux and chargecloud** all publicly claim broad CPMS/business coverage, but the exact boundary between protocol adapter, system of record, payment orchestration, merchant-of-record and settlement provider differs materially. Enigma should integrate each through a provider-specific adapter and keep an internal evidence/ledger boundary.
- **Virta:** OAuth client credentials, session/CDR APIs, Kafka/Avro streaming, PTC and managed roaming are public; API version matrix, replay/ordering, refunds and SLA are not. Sources: [Virta APIs](https://www.virta.global/virta-api), [docs](https://docs.virta.global/), [auth](https://docs.virta.global/docs/onboarding-guide/branches/main/enterprise/auth/intro), [CDR](https://docs.virta.global/docs/onboarding-guide/branches/main/enterprise/cdr-reports/intro), [streaming](https://docs.virta.global/docs/onboarding-guide/data-streaming/intro), [PTC](https://docs.virta.global/docs/onboarding-guide/ptc/intro), [roaming](https://www.virta.global/charging-solution/roaming).
- **Driivz:** public pages claim OCPP, ISO 15118, OCPI/OICP/eMIP/OCHP, payments, billing, reports, security and API/event bus; the actual docs portal is login-gated and exact refund/chargeback/API semantics are not public. Sources: [interoperability](https://driivz.com/platform/interoperability-and-extensibility/), [operations](https://driivz.com/platform/operations-management/), [billing](https://driivz.com/platform/ev-billing/), [security](https://driivz.com/platform/security-and-compliance/), [API article](https://driivz.com/blog/ev-charging-management-api/), [docs](https://docs.driivz.com/).
- **Last Mile Solutions:** public EVC-net docs provide OAuth2 Platform API, OCPI credentials, transaction backfill/delta sync, invoice-to-transaction drill-down and explicit warning that `lastUpdateDate` is not a completeness guarantee. Sources: [developer page](https://www.lastmilesolutions.com/developer-documentation/), [API overview](https://docs.evc-net.com/docs/overview-1.md), [auth](https://docs.evc-net.com/docs/authentication.md), [OCPI auth](https://docs.evc-net.com/docs/ocpi-authentication.md), [ingest](https://docs.evc-net.com/docs/ingesting-transactions.md), [invoice data](https://docs.evc-net.com/docs/mining-invoice-data.md), [status](https://status.evc-net.com/).
- **E-Flux by Road:** REST API, JWT/RBAC, signed non-ordered at-least-once webhooks, settlement-correction events, OCPP 2.0.1/2.1 claims, OCPI roaming and managed invoicing are public. Uptime claims conflict across official pages and ERE CDR is preview/beta. Sources: [Road API](https://documentation.road.io/reference/introduction), [reference](https://documentation.road.io/reference), [charging](https://documentation.road.io/docs/charge-stations), [roaming](https://documentation.road.io/docs/roaming), [ERE](https://documentation.road.io/reference/getv1eresessions.md), [webhook](https://documentation.road.io/reference/sessionupdatedwebhook.md), [invoice export](https://documentation.road.io/reference/getv2invoicesbyinvoicebillableitemsexport.md), [security](https://www.e-flux.io/security).
- **AMPECO:** Public OpenAPI v3.256.0 documents sessions, CDRs, communications/OCPI logs, partner settlement reports, retry payment and resume billing. Payment proceeds to the selected processor's merchant account; a general refund/chargeback API is not publicly verified. Sources: [overview](https://developers.ampeco.com/docs/overview), [main players](https://developers.ampeco.com/docs/main-players), [auth](https://developers.ampeco.com/reference/authorization-1), [sessions](https://developers.ampeco.com/reference/sessionslisting), [CDRs](https://developers.ampeco.com/reference/cdrslisting), [settlement](https://developers.ampeco.com/reference/partnersettlementreportslisting), [retry](https://developers.ampeco.com/reference/sessionretrypayment), [resume](https://developers.ampeco.com/reference/sessionresumebilling), [payments](https://www.ampeco.com/ev-charging-platform/payments-and-billing/).
- **GreenFlux:** broad public claims cover OCPP 1.5/1.6/2.0.1, OCPI 2.2.1, roaming, billing, CDR validation, payments and ISO 15118 collaboration; direct OCHP/eMIP, refund API, auth scopes, CDR schema and SLA remain U. Sources: [home](https://www.greenflux.com/), [compliance](https://www.greenflux.com/platform/compliance/), [roaming](https://www.greenflux.com/roaming/), [protocol article](https://www.greenflux.com/expertise/blogs/roaming-protocols-ocpi-oicp-ochp-and-emip/), [Charge Assist API](https://ca-api.chargeassist.app/), [API index](https://ca-api.chargeassist.app/apis), [security](https://www.greenflux.com/platform/security/).
- **chargecloud:** one of the strongest public finance/API surfaces: Core API v1/OpenAPI, demo endpoint, OAuth/API-key auth, sessions/meter values/CDR feedback, refunds, credit notes, CAMT/ISO 20022 matching, subledger and ERP transfer. It still does not publicly establish chargeback workflow, payout timing or all tenant entitlements. Sources: [modules](https://www.chargecloud.de/en-de/e-mobility-modules), [fleet/home](https://www.chargecloud.de/en-de/e-mobility-modules/fleet-home-charging), [revenue](https://www.chargecloud.de/en-de/e-mobility-modules/crm-billing-payment), [developer](https://chargecloud.dev/api/core-api), [auth](https://chargecloud.dev/authentication), [OpenAPI](https://chargecloud.dev/api/core-api/crmiapi.json), [status](https://status.chargecloud.de/), [Trust Center](https://trust.chargecloud.com/).
- **Noodoe:** public API article is feature-level only; session statements and Stripe revenue-transfer docs are concrete, while auth, CDR schema, API contract and dispute/settlement behavior remain U. Sources: [EV OS](https://www.noodoe.com/ev-os), [API article](https://www.noodoe.com/blog/what-can-an-ev-charging-api-do-for-your-software), [session report](https://help.noodoe.com/hc/en-us/articles/39130540019993-Understanding-Your-Charging-Session-Statement-Report), [RFID](https://help.noodoe.com/hc/en-us/articles/33569851429657-How-to-Set-Up-and-Activate-Noodoe-Cards-RFID-in-EV-OS), [Stripe transfer](https://help.noodoe.com/hc/en-us/articles/36896422601113-How-to-Set-Up-Automatic-Revenue-Transfer-Stripe-for-your-CPO), [refund](https://help.noodoe.com/hc/en-us/articles/56357640278553-Refund-Inquiry-Guide).
- **ChargeLab, EV Connect and AmpUp:** these are credible CSMS/payment-facilitation substitutes for site operations, but public API/SDK/CDR/reconciliation details are thin. ChargeLab's Developer Program is early access; EV Connect advertises open APIs and a 99.9% software term; AmpUp publicly documents a refund policy and host payout model. Sources: [ChargeLab API](https://chargelab.co/developer-program), [ChargeLab integrations](https://chargelab.co/integrations), [EV Connect software](https://www.evconnect.com/software/), [EV Connect agreement](https://www.evconnect.com/legal/software-license-agreement/), [AmpUp home](https://www.ampup.io/), [AmpUp refund](https://support.ampup.io/hc/en-us/articles/27465149610779-AmpUp-Refund-Policy), [AmpUp fees](https://support.ampup.io/hc/en-us/articles/23521776509339-Understanding-Network-and-Processing-Fees-on-AmpUp).

### Open-source and self-hostable substitutes

- **SteVe:** OCPP 1.2/1.5/1.6 CSMS with REST/OpenAPI, RFID tags, transactions, meter values and CSV export to third-party billing; no payment/settlement, OCPI or OCPP 2.x for standalone is publicly verified. Sources: [repo](https://github.com/steve-community/steve), [OpenAPI](https://raw.githubusercontent.com/steve-community/steve/master/api-docs.json), [configuration](https://github.com/steve-community/steve/wiki/Configuration), [validation](https://github.com/steve-community/steve/wiki/Incoming-OCPP-message-validation), [release](https://github.com/steve-community/steve/releases).
- **CitrineOS:** modular OCPP/OCPI CSMS with REST, GraphQL, RabbitMQ/Postgres, OCPP security, CDR/transaction modules and release-note payment/pricing features. Official materials are internally ambiguous about broad OCPP 2.1 completeness; no financial rails/refunds/settlement are verified. Sources: [repo](https://github.com/citrineos/citrineos-core), [architecture](https://citrineos.github.io/latest/core-concepts/architecture/), [Core API](https://citrineos.github.io/latest/apis/core-api/), [OCPI](https://github.com/citrineos/citrineos-core/blob/main/apps/ocpi-server/README.md), [release 2.0.0](https://github.com/citrineos/citrineos-core/releases/tag/v2.0.0), [LF Energy](https://lfenergy.org/projects/citrineos/).
- **OpenCPO:** self-hosted OCPP 1.6j/2.0.1, OCPI 2.2.1, mTLS/PKI/Bastion, public sessions/CDRs/invoices and payment-plugin boundary. It is a strong protocol/control-plane substitute, not a proven financial ledger. Sources: [site](https://opencpo.io/), [orchestration](https://github.com/opencpo/opencpo), [core](https://github.com/opencpo/opencpo-core), [schema](https://raw.githubusercontent.com/opencpo/opencpo-core/main/db/schema.sql), [sessions API](https://raw.githubusercontent.com/opencpo/opencpo-core/main/api/public_sessions.py), [OCPI management](https://raw.githubusercontent.com/opencpo/opencpo-core/main/api/ocpi_management.py), [Bastion](https://github.com/opencpo/opencpo-bastion).
- **EVtivity:** public OpenAPI v1/706 endpoints, JWT/API keys, Stripe payment/preauth/capture/refund/reconciliation endpoints, OCPP 1.6/2.1, OCPI 2.2.1/2.3, ISO 15118 and audit/SSE. No disputes/chargebacks/settlement or SLA is verified. Sources: [intro](https://www.evtivity.com/docs/getting-started/introduction/), [API](https://evtivity.com/api-reference), [payments](https://www.evtivity.com/api-reference/payments), [sessions](https://www.evtivity.com/api-reference/sessions), [OCPI](https://www.evtivity.com/api-reference/ocpi), [security](https://www.evtivity.com/security), [repo](https://github.com/EVtivity/evtivity-csms).
- **gocpp:** Go OCPP 1.6/2.0.1/2.1 protocol library with typed APIs, schema validation, Basic/mTLS authentication, transaction store and OCPP 2.1 payment/settlement wire models. It does not execute payments or provide a financial ledger; the repository says pre-v1. Sources: [repo](https://github.com/shiv3/gocpp), [usage](https://raw.githubusercontent.com/shiv3/gocpp/main/docs/usage.md), [architecture](https://raw.githubusercontent.com/shiv3/gocpp/main/docs/architecture.md), [TransactionStore](https://raw.githubusercontent.com/shiv3/gocpp/main/core/storage/transaction.go), [auth](https://raw.githubusercontent.com/shiv3/gocpp/main/core/auth/authenticator.go), [NotifySettlement schema](https://raw.githubusercontent.com/shiv3/gocpp/main/v21/schemas/NotifySettlementRequest.json).

### eMSP and access/payment facades

- **Chargemap:** Pass/app/Autocharge/Plug & Charge and business/OCPP export are public; CPO/operator sets underlying tariffs, Chargemap adds a service charge and consolidates/transfers revenue. Public consumer claims and reimbursements are not a machine-readable refund/chargeback contract. Sources: [Pass terms](https://chargemap.com/en-gb/about/cgv), [Pass](https://chargemap.com/en-gb/pass), [Partners](https://www.chargemap-partners.com/en/revenue-optimization), [Business](https://www.chargemap-business.com/en/charging-management-software), [P&C](https://chargemap.com/en-gb/blog/articles/what-is-plug-and-charge).
- **Electroverse:** consumer/business service with RFID/app, CPO-supplied CDRs, preauthorization, late CDRs and up to 365-day invoice timing. No public protocol/API/SDK or settlement contract was found. Sources: [home](https://electroverse.octopus.energy/), [FAQ](https://electroverse.octopus.energy/faqs), [consumer terms](https://electroverse.com/legal/terms), [business terms](https://electroverse.com/legal/business/terms), [privacy](https://electroverse.com/legal/privacy).
- **Elli:** public REST/OpenAPI, API-key read access, OAuth/OIDC user APIs, remote start/stop, virtual-versus-actual session distinction, Hubject/GIREVE roaming and consumer payment. Completed CDR/settlement/refund APIs are not public. Sources: [get started](https://developer.elli.eco/guides-get-started), [user auth](https://developer.elli.eco/guides-user-authorization), [public charging](https://developer.elli.eco/guides-public-charging), [remote start/stop](https://developer.elli.eco/guides-remote-start-and-stop), [Charge & Pay](https://developer.elli.eco/guides-charge-and-pay), [OCPP engineering](https://www.elli.eco/en/about-elli/news/newsroom/elli-engineering/parlez-vous-ocpp).
- **Allego:** business page claims API/webhook integration; public Plug & Charge details specify ISO 15118-2/OCPP 2.0.1/mTLS/Hubject PKI, with €40 preauthorization and fleet invoice. API, CDR, settlement and dispute details are not public. Sources: [business](https://www.allego.eu/business/), [P&C](https://www.allego.eu/plugandcharge/), [app](https://www.allego.eu/app/), [pricing](https://www.allego.eu/pricing/), [user conditions](https://www.allego.eu/wp-content/uploads/2026/08/EN-November-2025-User-Condition.pdf).
- **IONAGE:** public Discovery API/OCPI 2.2.1 and Token A onboarding, Nexus/App/Flo capabilities, wallet and refund policy; SDK is closed beta and CDR/settlement implementation is not public. Sources: [Developer Tools](https://www.ionage.in/products/developer-tools), [Nexus](https://www.ionage.in/products/nexus), [App](https://www.ionage.in/products/app), [FLO](https://www.ionage.in/products/flo), [refund](https://www.ionage.in/refund-policy), [BPCL case](https://www.ionage.in/customer-stories/bpcl).

### Data brokers

- **Eco-Movement:** strong public station/EVSE/pricing API evidence with OCPI 2.2/2.1.1, PATCH push, GET backfill, credentials and quality/freshness controls. No sessions/CDRs/payment/settlement capability is publicly verified. Sources: [home](https://www.eco-movement.com/), [guide](https://developers.eco-movement.com/docs/data-api-user-guide), [FAQ](https://developers.eco-movement.com/v2.1.1/docs/data-api-faq), [locations](https://developers.eco-movement.com/reference/locations), [prices](https://developers.eco-movement.com/v2.1.1/reference/prices-new), [credentials](https://developers.eco-movement.com/reference/send-credentials), [compliance](https://www.eco-movement.com/services/compliance/).
- **CIRRANTIC:** publicly claims automated feeds, OCPI/structured inputs, Charging Wallet, MapAPI, session enablement and Charging Radar; public API/auth/CDR/settlement details are not verified. Sources: [company](https://actions.cirrantic.com/en/cirrantic), [integration](https://actions.cirrantic.com/integration-data), [location](https://actions.cirrantic.com/charging-location-listing), [service](https://actions.cirrantic.com/charging-service-listing), [wallet](https://actions.cirrantic.com/en/charging-wallet-poweredbycirrantic), [portfolio](https://actions.cirrantic.com/cirrantic-service-portfolio).

### Protocols, standards and regulatory controls

- **OCPI 2.3.0:** current Foundation-labelled protocol; credentials, tokens, sessions, CDRs, credit CDRs, optional Payments and Invoice Reconciliation. OCPI does not define general PSP rails, refunds, chargebacks or delivery SLAs. Sources: [Foundation](https://evroaming.org/ocpi/), [downloads](https://evroaming.org/ocpi-downloads/), [repo](https://github.com/ocpi/ocpi), [sessions](https://github.com/ocpi/ocpi/blob/2.3.0/release/core/mod_sessions.asciidoc), [CDRs](https://github.com/ocpi/ocpi/blob/2.3.0/release/core/mod_cdrs.asciidoc), [Payments](https://github.com/ocpi/ocpi/blob/2.3.0/release/payments/mod_payments.asciidoc), [Invoice Reconciliation](https://github.com/ocpi/ocpi/blob/2.3.0/release/core/mod_invoice_reconciliation.asciidoc).
- **OICP 2.3:** Hubject's latest public roaming REST specification, with mandatory authorization/EVSE data/status, optional reservation/dynamic pricing/notifications, SessionID, CDR push/pull and signed-metering fields; no payment/settlement rails. Sources: [repo](https://github.com/hubject/oicp), [releases](https://github.com/hubject/oicp/releases), [EMP API](https://hubject.github.io/oicp-emp-2.3-api-doc/), [CPO API](https://hubject.github.io/oicp-cpo-2.3-api-doc/), [release notes](https://github.com/hubject/oicp/blob/master/OICP-2.3/Realease_Notes.asciidoc).
- **OCPP/OCA:** OCPP 1.6, 2.0.1 and 2.1 are available; IEC 63584-201:2026 and 63584-210:2026 are current catalog entries at retrieval. OCA says TLS/security profiles belong in production, signed meter values are transport evidence, and CDR exchange/payment settlement are outside OCPP's complete scope. Sources: [OCA protocols](https://openchargealliance.org/protocols/ocpp-protocols/), [IEC 2.0.1](https://webstore.iec.ch/en/publication/111418), [IEC 2.1](https://webstore.iec.ch/en/publication/111422), [security guide](https://openchargealliance.org/wp-content/uploads/2026/01/ocpp_security_operations_guide-v2.pdf), [signed meters](https://openchargealliance.org/ocpp-info-whitepapers/signed-meter-values-eichrecht-paper/), [OCTT](https://openchargealliance.org/test-tool/), [certification](https://openchargealliance.org/certification-program/).
- **ISO 15118-20/-21 and Plug & Charge PKI:** ISO 15118-20:2022 and 2026 Amendment 1 define EV/EVSE communication; ISO 15118-21 is a conformance test plan and excludes reliability/performance. EU AFIR/Delegated Regulation 2025/656 impose scoped dates for EN ISO 15118 on public and private points. CharIN/OPNC and EU STF describe multi-root PKI/trust-list architecture. Sources: [ISO 15118-20](https://www.iso.org/standard/77845.html), [Amendment 1](https://www.iso.org/standard/87920.html), [ISO 15118-21](https://www.iso.org/standard/84170.html), [CharIN P&C](https://www.charin.global/technology/plug-charge), [CharIN PKI](https://www.charin.global/technology/plug-charge/pki/), [AFIR](https://eur-lex.europa.eu/eli/reg/2023/1804/oj/eng), [Delegated Regulation 2025/656](https://eur-lex.europa.eu/eli/reg_del/2025/656/oj/eng), [OPNC](https://github.com/charinev/opnc).
- **EU AFIR/CEAP:** AFIR requires public infrastructure data, NAP/common European access point architecture, one-minute dynamic freshness, quality controls, ad-hoc electronic payment and price transparency. CEAP is policy; ESPR creates conditional product/DPP obligations but does not automatically impose a charging DPP. Sources: [AFIR](https://eur-lex.europa.eu/eli/reg/2023/1804/oj/eng), [API act 2025/645](https://eur-lex.europa.eu/eli/reg_del/2025/645/oj/eng), [data act 2025/655](https://eur-lex.europa.eu/eli/reg_impl/2025/655/oj/eng), [CEAP](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:52020DC0098), [ESPR](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32024R1781).
- **India DPDP:** technology-neutral privacy/accountability law. At retrieval, most processing/consent/rights/breach provisions are staged for 13 Nov 2026 and 13 May 2027; future rules include notice, consent-manager, processor, logs, backup, breach and SDF controls. Sources: [Act](https://www.indiacode.nic.in/indiacode/handle/123456789/22037?view_type=browse), [Act PDF](https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf), [commencement](https://www.meity.gov.in/static/uploads/2025/11/c56ceae6c383460ca69577428d36828b.pdf), [Rules](https://www.meity.gov.in/static/uploads/2025/11/53450e6e5dc3bcb37b2b05bcc3b4e031f.pdf), [MeitY index](https://www.meity.gov.in/documents/act-and-policies/digital-personal-data-protection-rules-2025-gDOxUjMtQWa).
- **RBI PA/NETC:** RBI PA authorisation/escrow/merchant/dispute obligations are separate from NPCI NETC's issuer/acquirer/NRCS member network. NETC v2.1 and ICD v2.5 are member-facing/older public interfaces; public SDK/current technical spec is not verified. Sources: [RBI Directions](https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12896), [NETC v2.1](https://ihmcl.co.in/wp-content/uploads/2025/12/NETC_PG_V2.1.pdf), [NETC](https://www.netc.org.in/), [NHAI FAQ](https://nhai.gov.in/nhai/sites/default/files/mix_file/FAQ-FASTag.pdf), [statistics](https://www.npci.org.in/product/netc/product-statistics).
- **U.S. rules:** covered federal-aid projects require OCPP/OCPI/ISO capability, open-access payment, price disclosure, >97% port uptime, status/price API and network switching; California adds state open-access and privacy overlays. Sources: [23 CFR Part 680](https://www.ecfr.gov/current/title-23/chapter-I/subchapter-G/part-680), [§680.106](https://www.ecfr.gov/current/title-23/section-680.106), [§680.116](https://www.ecfr.gov/current/title-23/section-680.116), [DOE NEVI](https://afdc.energy.gov/laws/12744), [DOE open access](https://afdc.energy.gov/laws/11067), [CARB](https://ww2.arb.ca.gov/our-work/programs/electric-vehicle-supply-equipment-evse-standards), [CCPA](https://leginfo.legislature.ca.gov/faces/codes_displayText.xhtml?division=3.&part=4.&lawCode=CIV&title=1.81.5).
- **Payment/API security:** PCI DSS v4.0.1 is an industry compliance standard whose applicability/validation comes from payment brands/acquirers/contracts; NIST SP 800-228 update 1, OWASP API Top 10, RFC 9421 and RFC 8705 provide engineering controls for API inventory, auth, signatures and mTLS-bound tokens. Sources: [PCI DSS](https://www.pcisecuritystandards.org/standards/pci-dss/), [PCI library](https://www.pcisecuritystandards.org/document_library/?category=pcidss), [NIST](https://csrc.nist.gov/pubs/sp/800/228/upd1/final), [OWASP](https://owasp.org/API-Security/editions/2023/en/0x00-header/), [RFC 9421](https://www.rfc-editor.org/rfc/rfc9421.html), [RFC 8705](https://www.rfc-editor.org/rfc/rfc8705.html).
- **API/OAuth/OIDC/events:** OpenAPI 3.2.1, AsyncAPI 3.1.0, OAuth 2.0/RFC 9700, OIDC Discovery/Core and CloudEvents 1.0.2 provide interface, authorization, discovery and event-envelope standards. They do not define payment, CDR, refund, settlement or webhook delivery guarantees. Sources: [OpenAPI](https://spec.openapis.org/oas/v3.2.1.html), [AsyncAPI](https://www.asyncapi.com/docs/reference/specification/v3.1.0), [OAuth](https://www.rfc-editor.org/rfc/rfc6749), [OAuth BCP](https://www.rfc-editor.org/rfc/rfc9700), [OIDC Core](https://openid.net/specs/openid-connect-core-1_0.html), [OIDC Discovery](https://openid.net/specs/openid-connect-discovery-1_0.html), [CloudEvents](https://cloudevents.io/), [releases](https://github.com/cloudevents/spec/releases).

## 5. Direct incumbent and open-source substitutes

### 5.1 Substitute map by Enigma capability domain

| Enigma domain to benchmark | Direct incumbent substitutes | Open-source / standards substitutes | What is actually comparable |
|---|---|---|---|
| CPO↔EMP roaming | Hubject, GIREVE, e-clearing.net, ChargeHub, Plugsurfing, GreenFlux, Monta | OCPI 2.3, OICP 2.3, OCHP | Network reach, contract routing, token/session/CDR exchange; not necessarily funds settlement. |
| OCPP CSMS/control | Driivz, AMPECO, Last Mile, Road, Virta, chargecloud, GreenFlux, EV Connect | SteVe, CitrineOS, OpenCPO, EVtivity, gocpp | Charger control, auth, sessions, logs and meter data; payment ledger is separate. |
| Smart charging/local resilience | ChargePilot, Virta, GreenFlux, Driivz, ChargeLab | CitrineOS/OpenCPO plus OCPP profiles | Local fallback, load control, telemetry; not roaming finance. |
| eMSP/consumer access | Plugsurfing, Chargemap, Electroverse, Elli, Allego, IONAGE | OCPI Tokens/Commands, ISO 15118/PKI | Driver identity, start/stop and billing facade; CPO data remains authoritative for many fields. |
| Payment orchestration | E-Flux/Road, chargecloud, AMPECO, Virta, Noodoe, Monta, AmpUp | Stripe/Adyen/etc. connectors; PCI DSS control plane | PSP integration and preauth/capture/receipts; not automatically inter-operator settlement. |
| Financial clearing/reconciliation | Hubject Financial Services, GIREVE Clearing, chargecloud, selected managed-roaming products | OCPI CDR + Invoice Reconciliation; custom ledger | CDR rating, invoice and status handling; confirm funds custody, finality and disputes. |
| Station master data/status | Eco-Movement, CIRRANTIC, ChargeHub public API | OCPI Locations/EVSE/Prices, DATEX II | Availability/pricing distribution, not session or payment authority. |
| Payment/toll network | NPCI NETC/FASTag | NETC member integration; RBI PA controls | Regulated scheme boundary; must not be collapsed into generic EV roaming. |
| Security/event contracts | OAuth/OIDC, OpenAPI, AsyncAPI, CloudEvents, RFC 9421/8705, PCI/NIST | Implementations of these standards | Contract and trust controls; no domain settlement semantics. |

### 5.2 Strategic substitute conclusion

No single public substitute proves the complete Enigma target across **charger control + roaming + delegated authorization + evidence-grade metering + payment capture + inter-operator settlement + refunds/chargebacks + reconciliation + regulatory compliance**. The closest commercial breadth is distributed across chargecloud, Road/E-Flux, AMPECO, Virta, Driivz, GIREVE and Hubject-related services, but the public evidence still leaves contract and runtime gates. The strongest open-source starting points are EVtivity, OpenCPO, CitrineOS and SteVe/gocpp, but these require independent financial, operational and regulatory layers.

## 6. Material protocol and regulatory implications for Enigma

1. **Pin versions and profiles, not labels.** OCPI “2.3.0,” OICP “2.3,” OCPP “2.1,” and ISO 15118 “Plug & Charge” each contain editions, modules, profiles, optional features and implementation-specific deviations. Persist negotiated versions, module matrices, certificates, profile IDs and partner configuration.
2. **Treat CDR lineage as non-negotiable.** CPO-owned CDRs, eMSP-facing CDRs, OICP CDRs, credit CDRs, OCPP meter values, signed meter values and invoice lines are distinct objects. Store original payload, source, timestamps, signature/validation result, correction lineage and replay state.
3. **Separate transaction states.** At minimum: requested, authorized, charger-accepted, electricity-started, active, stop-requested, stopped, CDR-pending, CDR-validated, priced, preauth-captured, invoice-issued, settled, corrected, disputed, refunded, charged back, written off. Do not derive final money state from charger state.
4. **Support asynchronous and offline paths.** Public platforms document delayed/missing/reordered events, cached/offline auth, late CDRs, retry queues, pull recovery, failed captures and session correction. Require idempotency keys, deterministic deduplication, monotone state transitions where appropriate, dead-letter handling and operator-visible replay.
5. **Keep delegated authorization explicit.** OAuth/OIDC, OCPI credentials/tokens, OICP contracts, ISO 15118 contract certificates, RFID and API keys are not equivalent. Record principal, delegate, audience, scope, consent/contract reference, issuance/expiry/revocation and the policy decision.
6. **Do not confuse protocol compliance with legal compliance.** AFIR, 23 CFR Part 680, California rules, RBI/NETC, DPDP and PCI DSS apply according to role, geography, project funding and data/payment flow. Enigma needs a jurisdictional applicability register, not a generic “compliant” label.
7. **Design evidence separately from operational logs.** OCA signed-meter guidance, RFC 9421 signatures, HMAC webhooks, CDR fields and protocol logs help prove selected message properties; none alone establishes legally admissible meter evidence, immutable retention, or financial finality.
8. **Treat payment rails as external bounded contexts.** Merchant of record, acquirer/PSP, escrow, capture/reversal, chargeback, tax, reserves and payout timing must be contractually bound and reconciled to an internal double-entry ledger. “Automated settlement” is not enough.
9. **Implement public-data freshness and provenance.** EU AFIR requires dynamic updates within one minute and static changes within 24 hours for in-scope data; preserve source timestamps, freshness status, quality flags, IDRO/actor IDs and operator accountability.
10. **Plan Plug & Charge as a PKI program.** Certificate issuance, contract certificate renewal, revocation, trust-list updates, multiple roots/ecosystems, OEM/eMSP/CPO roles and ad-hoc fallback are separate from OCPI/OCPP. AFIR does not make Plug & Charge the sole payment route.

## 7. Falsifiable residual gap hypotheses

These are testable hypotheses, not conclusions. Each should be accepted or rejected with a contract, authenticated documentation, sandbox test, packet trace, replay test, ledger reconciliation or independent assurance artifact.

| ID | Hypothesis to test | Falsification evidence / acceptance test |
|---|---|---|
| H1 | Enigma can ingest and deduplicate every supported partner’s session/CDR flow without losing late, duplicate, reordered or corrected records. | Replay a corpus containing duplicate, out-of-order, credit-CDR, 90-day-late and missing-prior-session records; prove one canonical lineage and no silent loss. |
| H2 | Each incumbent’s public protocol claim corresponds to the tenant’s enabled production profile. | Obtain tenant-specific module/version matrix and run positive/negative conformance tests against sandbox and production-like credentials. |
| H3 | “Automated settlement” means a defined, reconcilable financial movement, not only rating/invoice status. | Obtain funds-flow diagram, merchant/acquirer role, settlement file/API, cutoff, finality/reversal rules and reconcile a complete period to bank/PSP evidence. |
| H4 | Refunds and chargebacks can be initiated, tracked, idempotently retried and reconciled for every payment mode. | Execute card, wallet, roaming, preauth, partial capture, failed capture and chargeback scenarios; require reason codes, evidence, status, SLA and ledger postings. |
| H5 | Enigma can prove which principal authorized a cross-domain start/stop. | Trace RFID/app/OAuth/OCPI/OICP/P&C paths with principal, delegate, audience, contract, consent, certificate and revocation evidence. |
| H6 | CPO meter data is sufficiently authoritative for regulated or contractual billing. | Obtain signed-meter/ Eichrecht evidence where claimed; compare raw meter, OCPP event, CDR, invoice and correction records; test clock drift and tampering. |
| H7 | Webhook/event delivery is recoverable and complete. | Induce timeouts, 429s, duplicate delivery, signature failure, endpoint outage and ordering inversion; prove retry, replay, dead-letter and operator reconciliation. |
| H8 | Public uptime/SLA claims cover the relevant end-to-end path. | Compare contract SLA denominator/exclusions with status history and synthetic tests across charger, CSMS, roaming, PSP and notification dependencies. |
| H9 | Enigma’s API contract can remain compatible through partner version drift. | Run schema-diff and contract tests against pinned OpenAPI/AsyncAPI/OCPI/OICP/OCPP artifacts; require deprecation notice and rollback path. |
| H10 | Public-data freshness obligations can be met while preserving operator provenance. | Measure static ≤24h and dynamic ≤1min AFIR feeds, including source outage, corrections, stale flags and NAP acknowledgements. |
| H11 | DPDP/CCPA/other privacy rights can propagate through all processors and roaming partners. | Execute access, correction, erasure, consent withdrawal and incident scenarios; prove processor/subprocessor propagation, exceptions and evidence. |
| H12 | PCI scope is minimized and correctly assigned. | Produce data-flow diagram, tokenization/PAN/SAD inventory, CDE boundaries, provider AOCs/ROCs and QSA/acquirer determination; verify no prohibited data enters logs/CDRs. |
| H13 | Plug & Charge trust-list/certificate lifecycle works across roots and roaming partners. | Test provisioning, renewal, revocation, trust-list update, expired cert, wrong root, offline and declined-auto-auth fallback across representative EV/EVSE/eMSP paths. |
| H14 | A self-hosted open-source substitute can meet Enigma’s operational goals without hidden proprietary services. | Deploy pinned SteVe/CitrineOS/OpenCPO/EVtivity/gocpp builds; run load, upgrade, recovery, security, licensing, data-retention and financial integration tests. |
| H15 | Regulatory claims are applicable to the actual Enigma role and deployment. | Obtain jurisdiction/funding/merchant/processor facts and legal review mapping each obligation to entity, product, date, evidence and control owner. |

## 8. Source limitations and explicit failed/unavailable items

### 8.1 Limitations

- All findings are based on the supplied structured primary-source results retrieved on **2026-09-30**; pages, repositories, versions, marketing claims and status dashboards can change.
- Vendor-controlled pages can establish a public claim, not independent implementation verification. Public source review cannot verify **private contract capabilities, legal compliance, certification scope, tenant configuration, commercial inclusion, or real integration behavior**.
- A product page that names a protocol does not prove every module/profile/version is enabled for every customer, geography, charger or partner.
- A service-level target or status page does not prove end-to-end availability across CPO, network, roaming hub, PSP, payment network and driver channels.
- A CDR or invoice endpoint does not prove meter truth, financial finality, legal metrology, settlement completion, refund execution or chargeback responsibility.
- Public source material often separates a base roaming/CPMS product from financial services; the report does not merge them by inference.
- Legal materials are not interchangeable: EU regulations, U.S. federal rules, California summaries, RBI directions, NPCI procedures, standards and vendor terms have different legal status and scope.
- Source retrieval date is fixed. “Current” means current in the supplied evidence at retrieval, not guaranteed current after retrieval.

### 8.2 Failed or unavailable items (transparent; no inference)

The structured input reports **`Failed items: []`**. No successful item was marked failed. The following items were nevertheless **unavailable or not publicly verified**, and were not filled by inference:

- Public maintained SDK/client-library package for Hubject intercharge/OICP, GIREVE, e-clearing.net, Plugsurfing, Virta, Driivz, Last Mile, Road/E-Flux, AMPECO, GreenFlux, ChargeLab, FLO, EV Connect, AmpUp, Noodoe, chargecloud, ChargePilot, ChargeHub Passport Hub, Chargemap, Electroverse, Elli, Allego, IONAGE, Eco-Movement, CIRRANTIC, EVlinq, Numocity, and most other commercial subjects.
- Public partner API endpoint/authentication catalog for Hubject Financial Services, ChargeHub Passport Hub, EVlinq, Allego, Electroverse, CIRRANTIC and several vendor-managed roaming products.
- Complete public API schemas, webhooks, idempotency, rate-limit, version/deprecation and compatibility guarantees for gated or feature-level APIs.
- Universal payment processor/acquirer, merchant-of-record, funds custody, escrow, reserve, tax, payout, chargeback and settlement-finality proof for commercial platforms.
- General refund, card-chargeback, dispute-case, representment and reconciliation workflow/API for most subjects.
- Protocol-wide CDR retention, exactly-once delivery, immutable audit, meter provenance, signature verification and legally admissible evidence guarantees.
- Independent uptime/SLA measurements, RPO/RTO, incident history and operational assurance for vendors that only published targets or marketing claims.
- Public current NETC member technical specifications, SDK, sandbox and complete API/error catalog; the procedural guidelines say detailed specifications are shared during certification/onboarding.
- Public EV-specific API/SDK/CDR/session contract in DPDP, AFIR, PCI DSS, NIST, OAuth/OIDC, OpenAPI, AsyncAPI or CloudEvents standards.
- Verification that any named vendor’s private contract, certification, regulatory authorization, tenant configuration or production integration behaves as described publicly.

## 9. Prioritized revalidation backlog

Priority uses **P0 = block architectural or legal assumption**, **P1 = before integration commitment**, **P2 = before scale/production pilot**, **P3 = ongoing evidence maintenance**.

| Priority | Work item | Why it matters | Required evidence / owner |
|---|---|---|---|
| P0 | Freeze Enigma domain model for auth, sessions, CDRs, ledger, settlement, refunds and disputes | Prevents protocol/session data being mistaken for financial finality | Architecture + finance/control owners; event/state model and ledger invariants |
| P0 | Create jurisdiction/role applicability register | AFIR, U.S. funding rules, California, DPDP, RBI/NETC and PCI are not universal | Legal/compliance; entity, geography, funding, processor, effective date, control mapping |
| P0 | Obtain payment data-flow and PCI scope determination | Card/payment claims are not enough; logs/CDRs can expand CDE scope | QSA/acquirer and security; PAN/SAD/token map, AOC/ROC, CDE boundary |
| P0 | Obtain contracts and product entitlements for every target incumbent | Public review cannot verify private capabilities | Procurement/partnerships; tenant matrix, enabled modules, SLA, data rights, liability |
| P0 | Pin protocol editions and profiles | Labels such as OCPI 2.3/OCPP 2.1 hide edition/module differences | Integration engineering; signed artifact hashes, profile matrix, compatibility tests |
| P1 | Run roaming authorization/session/CDR conformance matrix | CPO/EMP/hub behavior differs, including offline and late CDR paths | Integration QA; Hubject, GIREVE, OCPI, OICP, OCHP, Plugsurfing and partner tests |
| P1 | Build CDR replay/correction harness | CDRs can be late, duplicated, rejected, revised, credited or missing a Session | Data/platform; replay corpus, dedup, credit CDR lineage, correction ledger |
| P1 | Validate settlement and invoice reconciliation | “Automated settlement” is not proof of money movement/finality | Finance; end-to-end period reconciliation to PSP/bank/invoice/credit notes |
| P1 | Test refund/chargeback/dispute workflows by payment mode | Most public sources do not document a complete flow | Payments/support; card, wallet, roaming, preauth, partial, chargeback, reversal tests |
| P1 | Verify webhook/event guarantees | Public systems document retries but not always ordering/completeness/retention | SRE/integration; outage/429/signature/replay/DLQ and backfill tests |
| P1 | Verify auth/delegation and offboarding | OAuth, OCPI tokens, RFID, P&C certs and roaming contracts are distinct | IAM/security; scopes, audience, consent, expiry, revocation, partner offboarding |
| P1 | Establish meter/evidence policy | Signed meter values and OCPP logs are not automatically legal metrology | Compliance/data; source precedence, signatures, clock sync, retention, legal hold |
| P2 | Compare CPMS/CSMS substitutes in a controlled bake-off | Public breadth does not show operational fit | Platform team; SteVe/CitrineOS/OpenCPO/EVtivity vs 2 commercial candidates |
| P2 | Test local/offline resilience and recovery | Multiple platforms claim fallback/queues; behavior is deployment-specific | SRE; network loss, CPO outage, cloud outage, power loss, replay and reconciliation |

## 10. Exhaustive primary-source URL register

This appendix preserves the supplied source URLs, grouped by subject. It does not upgrade a source from vendor claim to independent evidence.

### Commercial roaming, CPMS, eMSP and data platforms

**Hubject intercharge**
- https://www.hubject.com/intercharge-overview
- https://www.hubject.com/products/intercharge-cpo
- https://www.hubject.com/products/intercharge-emp
- https://support.hubject.com/hc/en-us/articles/4409164946065-2-10-Web-services-to-be-implemented-as-CPO
- https://support.hubject.com/hc/en-us/articles/4403421095953-2-6-Implementation-of-web-services
- https://github.com/hubject/oicp
- https://hubject-fs.com/
- https://www.hubject.com/blog-posts/enelx-hubject-emobility-payment-solution
- https://www.hubject.com/pricing

**GIREVE**
- https://www.gireve.com/download/
- https://www.gireve.com/wp-content/uploads/2026/09/Gireve_Tech_OCPI-V2.2.1_ImplementationGuide_V1.6-_en.pdf
- https://www.gireve.com/wp-content/uploads/2025/02/Gireve_Tech_eMIP-V0.7.4_ProtocolDescription_1.0.17-en.pdf
- https://www.gireve.com/ev-roaming-services/
- https://www.gireve.com/clearing-services/
- https://www.gireve.com/wp-content/uploads/2024/10/GIREVE-%E2%80%93-BOOST-Services-description-%E2%80%93-092024.pdf
- https://www.gireve.com/wp-content/uploads/2024/10/GIREVE-BOOST-Licence-Content-%E2%80%93-092024.pdf
- https://www.gireve.com/wp-content/uploads/2022/09/GIREVE-Subscription-Agreement-1.5.2_Appendix-2-GIREVE-Service-Level-1.5.2.pdf
- https://gireve-apis.stoplight.io/
- https://www.gireve.com/plug-and-charge-services/
- https://www.gireve.com/wp-content/uploads/2022/09/Roaming-Agreement-Template-V2.9.pdf

**e-clearing.net**
- https://www.e-clearing.net/
- https://www.e-clearing.net/starter-package
- https://www.e-clearing.net/data-guardian
- https://www.e-clearing.net/extendedaccess
- https://www.e-clearing.net/customer-support
- https://github.com/e-clearing-net/OCHP
- https://github.com/e-clearing-net/OCHP/blob/master/OCHP.md
- https://github.com/e-clearing-net/OCHP/blob/master/OCHP-direct.md
- https://www.now-gmbh.de/en/news/pressreleases/e-clearing-net-and-now-gmbh-simplify-sharing-of-charging-infrastructure-data/
- https://smartlab.de/presse-e-clearing-verzeichnet-enormes-wachstum/

**Plugsurfing**
- https://developer.plugsurfing.com/docs/plugsurfings-apis
- https://developer.plugsurfing.com/docs/about-drive-api
- https://developer.plugsurfing.com/docs/about-roam-ocpi
- https://developer.plugsurfing.com/docs/authorization
- https://developer.plugsurfing.com/docs/sessions
- https://developer.plugsurfing.com/docs/cdr
- https://developer.plugsurfing.com/docs/payment-integrations
- https://developer.plugsurfing.com/docs/payments
- https://developer.plugsurfing.com/docs/cdrs-module
- https://developer.plugsurfing.com/docs/tokens-module
- https://developer.plugsurfing.com/docs/sla
- https://plugsurfing.com/api
- https://plugsurfing.com/network
- https://plugsurfing.com/legal/terms-of-use/
- https://status.plugsurfing.com/

**Virta**
- https://www.virta.global/virta-api
- https://docs.virta.global/
- https://docs.virta.global/docs/onboarding-guide/branches/main/enterprise/auth/intro
- https://docs.virta.global/docs/onboarding-guide/branches/main/enterprise/charging/intro
- https://docs.virta.global/docs/onboarding-guide/branches/main/enterprise/cdr-reports/intro
- https://docs.virta.global/docs/onboarding-guide/data-streaming/intro
- https://docs.virta.global/docs/onboarding-guide/branches/main/data-streaming/consuming
- https://docs.virta.global/docs/onboarding-guide/ptc/intro
- https://www.virta.global/charging-solution/roaming
- https://www.virta.global/charging-solution/payments-invoicing
- https://www.virta.global/charging-solution/virta-hub-cpms

**Driivz**
- https://driivz.com/platform/interoperability-and-extensibility/
- https://driivz.com/platform/operations-management/
- https://driivz.com/platform/ev-billing/
- https://driivz.com/solutions/e-mobility-service-providers/
- https://driivz.com/blog/ev-charging-guide/
- https://driivz.com/blog/ev-charging-management-api/
- https://driivz.com/platform/security-and-compliance/
- https://driivz.com/platform/reporting-and-analytics/
- https://docs.driivz.com/
- https://driivz.com/wp-content/uploads/2019/10/Driivz_web_pdf_Platform.pdf

**Last Mile Solutions**
- https://www.lastmilesolutions.com/developer-documentation/
- https://docs.evc-net.com/
- https://docs.evc-net.com/docs/overview-1.md
- https://docs.evc-net.com/docs/authentication.md
- https://docs.evc-net.com/docs/getting-started-ocpi.md
- https://docs.evc-net.com/docs/ocpi-authentication.md
- https://docs.evc-net.com/docs/ingesting-transactions.md
- https://docs.evc-net.com/docs/mining-invoice-data.md
- https://www.lastmilesolutions.com/payment-as-a-service/
- https://www.lastmilesolutions.com/billing-as-a-service/
- https://www.lastmilesolutions.com/hardware-integration/
- https://www.lastmilesolutions.com/it-data-management/
- https://status.evc-net.com/

**E-Flux by Road**
- https://www.e-flux.io/
- https://road.io/
- https://documentation.road.io/reference/introduction
- https://documentation.road.io/reference
- https://documentation.road.io/docs/charge-stations
- https://documentation.road.io/docs/charge-cards
- https://documentation.road.io/docs/roaming
- https://road.io/en/platform/charge-point-operations
- https://www.e-flux.io/products/payments
- https://www.e-flux.io/products/billing-settlement-engine
- https://road.io/services/managed-invoicing
- https://road.io/platform/payment-terminals
- https://road.io/platform/qr-code-payments
- https://www.e-flux.io/security
- https://documentation.road.io/reference/getv1eresessions.md
- https://documentation.road.io/reference/sessionupdatedwebhook.md
- https://documentation.road.io/reference/getv2invoicesbyinvoicebillableitemsexport.md
- https://help.e-flux.io/en/articles/9685320-api-access

**AMPECO**
- https://developers.ampeco.com/docs/overview
- https://developers.ampeco.com/docs/main-players
- https://developers.ampeco.com/reference/authorization-1
- https://developers.ampeco.com/llms.txt
- https://www.ampeco.com/ev-charging-platform/open-charge-point-interface-ocpi-protocol/
- https://www.ampeco.com/ev-charging-platform/payments-and-billing/
- https://developers.ampeco.com/reference/sessionslisting
- https://developers.ampeco.com/reference/cdrslisting
- https://developers.ampeco.com/reference/cdrread
- https://developers.ampeco.com/reference/partnersettlementreportslisting
- https://developers.ampeco.com/reference/transactionupdate
- https://developers.ampeco.com/reference/paymentmethodcreate
- https://developers.ampeco.com/reference/sessionretrypayment
- https://developers.ampeco.com/reference/sessionresumebilling
- https://developers.ampeco.com/reference/transactioncreatepreauthorization
- https://developers.ampeco.com/reference/communicationlogslisting
- https://developers.ampeco.com/reference/listocpilogs
- https://developers.ampeco.com/reference/notificationssubscribedeprecated
- https://www.ampeco.com/blog/platform-updates-may-2026/
- https://www.ampeco.com/ev-charging-solutions/scaling-charge-point-operator/

**Monta**
- https://monta.com/en-us/developer-hub/api-and-webhooks/
- https://developer.monta.com/
- https://docs.partner-api.monta.com/reference/ref-authentication
- https://developer.monta.com/reference/access-control
- https://developer.monta.com/reference/ref-webhooks
- https://developer.monta.com/reference/post-cdr-export
- https://monta.com/en/products/hub-charge-point-management-system/
- https://monta.com/help/en_US/monta-hub-roaming/emsp-self-managed-outbound-roaming
- https://monta.com/help/en_US/monta-hub-roaming/cpo-self-managed-inbound-roaming
- https://monta.com/help/en_US/monta-hub-payments-transactions-wallets-transactions/operator-wallet-transactions
- https://developer.monta.com/reference/post-operator-adjustment-transaction-1
- https://monta.com/en-us/partner-services/
- https://monta.com/en-us/legal-risk-compliance/terms-of-use/
- https://monta.com/help/en_US/monta-charge-account-settings/how-payment-works-for-ev-drivers
- https://monta.com/en/blog/ocpp/

**GreenFlux**
- https://www.greenflux.com/
- https://www.greenflux.com/platform/compliance/
- https://www.greenflux.com/roaming/
- https://www.greenflux.com/expertise/blogs/roaming-protocols-ocpi-oicp-ochp-and-emip/
- https://ca-api.chargeassist.app/
- https://ca-api.chargeassist.app/apis
- https://developer.greenflux.com/docs/intro-to-charge-assist
- https://www.greenflux.com/revenue-optimisation/
- https://www.greenflux.com/features/direct-pay-via-web/
- https://www.greenflux.com/management-at-scale/
- https://www.greenflux.com/platform/security/

**ChargeLab**
- https://chargelab.co/developer-program
- https://chargelab.co/software
- https://chargelab.co/integrations
- https://chargelab.co/blog/chargelab-announces-ev-charging-api-developer-program
- https://chargelab.zendesk.com/hc/en-us/articles/27582299405083-How-drivers-can-pay-for-charging-at-your-site
- https://chargelab.zendesk.com/hc/en-us/articles/25587384874651-How-to-receive-payments-for-your-chargers-usage
- https://chargelab.zendesk.com/hc/en-us/articles/26309429504155-How-to-view-reporting-and-payouts-for-Payter-terminals
- https://chargelab.zendesk.com/hc/en-us/articles/34181862209563-ChargeHub-Integration-What-EV-Drivers-Need-to-Know
- https://chargelab.zendesk.com/hc/en-us/articles/20391628214171-How-to-access-your-payment-history-receipts
- https://chargelab.zendesk.com/hc/en-us/articles/25587258749723-How-RFID-cards-can-be-used-at-your-chargers

**FLO**
- https://www.flo.com/products/hardware/smartdc/
- https://www.flo.com/wp-content/uploads/2023/02/FLO-Ultra-and-NEVI.pdf
- https://www.flo.com/business/utilities/
- https://www.flo.com/driver-terms-of-use/
- https://www.flo.com/products/software/owners-portal/
- https://www.flo.com/products/services/global-management-services/
- https://www.flo.com/company/partner-networks/
- https://www.flo.com/insights/plug-charge-and-go/
- https://www.flo.com/flo-charging-station-uptime/

**EV Connect**
- https://www.evconnect.com/software/
- https://www.evconnect.com/industries/cpos/
- https://www.evconnect.com/drivers/
- https://www.evconnect.com/news/ev-connect-continues-commitment-to-open-standards-with-ocpp-2-0-1-certification/
- https://www.evconnect.com/resources/glossary/
- https://www.evconnect.com/news/ev-connect-offers-gm-dealerships-charging-management-and-network-services-across-canada-u-s/
- https://www.evconnect.com/legal/software-license-agreement/
- https://www.evconnect.com/resources/faq/

**AmpUp**
- https://www.ampup.io/
- https://www.ampup.io/products/ev-charging-management-software
- https://www.ampup.io/terms-of-use
- https://support.ampup.io/hc/en-us/articles/27465149610779-AmpUp-Refund-Policy
- https://support.ampup.io/hc/en-us/articles/9875011283995-How-does-AmpUp-s-Driver-Payment-and-Wallet-work
- https://support.ampup.io/hc/en-us/articles/8725147089435-What-kind-of-data-do-EV-charging-stations-monitor-and-collect
- https://support.ampup.io/hc/en-us/articles/19839252709403-What-happens-if-a-car-if-the-charging-station-loses-connection-to-AmpUp-while-my-car-is-plugged-in
- https://support.ampup.io/hc/en-us/articles/12723526459291-What-is-included-in-the-CORE-plan
- https://support.ampup.io/hc/en-us/articles/23521776509339-Understanding-Network-and-Processing-Fees-on-AmpUp
- https://www.ampup.io/blog/ev-charging-white-labeled-software-considerations
- https://www.ampup.io/blog/what-is-ocpp-complete-standards-guide
- https://support.ampup.io/hc/en-us/articles/8558701366939-How-do-I-collect-my-revenue-from-charging-sessions

**Noodoe**
- https://www.noodoe.com/ev-os
- https://www.noodoe.com/press/noodoe-leads-the-future-of-ev-charging-with-ocpp-2-0-1-certification-and-integration-capabilities
- https://www.noodoe.com/blog/what-can-an-ev-charging-api-do-for-your-software
- https://help.noodoe.com/hc/en-us/articles/39130540019993-Understanding-Your-Charging-Session-Statement-Report
- https://help.noodoe.com/hc/en-us/articles/33569851429657-How-to-Set-Up-and-Activate-Noodoe-Cards-RFID-in-EV-OS
- https://help.noodoe.com/hc/en-us/articles/56258136816153-Charging-Access-Modes
- https://help.noodoe.com/hc/en-us/articles/36896422601113-How-to-Set-Up-Automatic-Revenue-Transfer-Stripe-for-your-CPO
- https://help.noodoe.com/hc/en-us/articles/4412209973017-Temporary-Pre-Authorization-Fee
- https://help.noodoe.com/hc/en-us/articles/56357640278553-Refund-Inquiry-Guide
- https://www.noodoe.com/data-security
- https://www.noodoe.com/blog/why-ev-charger-uptime-matters

**chargecloud**
- https://www.chargecloud.de/en-de/e-mobility-modules
- https://www.chargecloud.de/en-de
- https://www.chargecloud.de/en-de/e-mobility-modules/fleet-home-charging
- https://www.chargecloud.de/en-de/e-mobility-modules/crm-billing-payment
- https://www.chargecloud.de/en-de/e-mobility-modules/partner-solution-management-2
- https://chargecloud.dev/api/core-api
- https://chargecloud.dev/authentication
- https://chargecloud.dev/contract-management
- https://chargecloud.dev/asset-management
- https://chargecloud.dev/api/core-api/crmiapi.json
- https://support.chargecloud.de/hc/en-gb/articles/360012869457-Glossary
- https://status.chargecloud.de/
- https://trust.chargecloud.com/

**ChargePilot / The Mobility House**
- https://www.mobilityhouse.com/usa_en/solutions/chargepilot
- https://tmh-help.freshdesk.com/en/support/solutions/articles/203000040346-chargepilot-system-architecture
- https://tmh-help.freshdesk.com/en/support/solutions/articles/203000040345-chargepilot-integrations-through-standardized-interfaces
- https://tmh-help.freshdesk.com/en/support/solutions/articles/203000054911-chargepilot-ocpp-proxy
- https://chargepilot-api.tmh.energy/integration-guide/
- https://chargepilot-api.tmh.energy/docs-json
- https://chargepilot-api.tmhusa.energy/integration-guide/
- https://tmh-help.freshdesk.com/en/support/solutions/articles/203000046009-chargepilot-charging-data-push-api
- https://tmh-help.freshdesk.com/en/support/solutions/articles/203000061121-chargepilot-fallback-mechanism
- https://www.mobilityhouse.com/usa_en/partners
- https://tmh-help.freshdesk.com/en/support/solutions/articles/203000046016-chargepilot-modbus-interface

**ChargeHub / Passport Hub**
- https://chargehub.com/en/ev-business-solutions/passport-ev-roaming-hub
- https://chargehub.com/en/ev-business-solutions/plug-and-charge
- https://chargehub.com/en/ev-charging-news/plug-and-charge-raar-process
- https://chargehub.com/en/ev-business-solutions/emobility-service-provider-emsp
- https://developer.chargehub.com/
- https://developer.chargehub.com/apis
- https://developer.chargehub.com/products
- https://chargehub.com/en/ev-business-solutions/charging-lab
- https://chargehub.com/en/ev-charging-news/chargehub-soc2-type-ii-certification

**Chargemap**
- https://chargemap.com/en-gb/about/cgv
- https://chargemap.com/en-gb/pass
- https://chargemap.com/en-gb/price
- https://www.chargemap-partners.com/en/revenue-optimization
- https://www.chargemap-partners.com/en
- https://www.chargemap-business.com/en/charging-management-software
- https://chargemap.com/en-gb/blog/articles/charge-via-chargemap-mobile-app
- https://chargemap.com/en-gb/blog/articles/what-is-plug-and-charge
- https://chargemap.com/en-gb/blog/articles/autocharge-how-it-works
- https://support.chargemap.com/l/en/article/u7behxlm58-how-am-i-billed

**Electroverse**
- https://electroverse.octopus.energy/
- https://electroverse.octopus.energy/faqs
- https://electroverse.com/legal/terms
- https://electroverse.com/legal/business/terms
- https://electroverse.com/community/ev-blogs-and-guides/how-to-use-the-octopus-electroverse-app
- https://electroverse.com/legal/privacy

**Elli**
- https://developer.elli.eco/guides-get-started
- https://developer.elli.eco/guides-user-authorization
- https://developer.elli.eco/guides-public-charging
- https://developer.elli.eco/guides-remote-start-and-stop
- https://developer.elli.eco/guides-charge-and-pay
- https://developer.elli.eco/guides-subscriber-overview
- https://www.elli.eco/en/station-setup
- https://www.elli.eco/en/b2c/products/tariffs
- https://www.elli.eco/en/about-elli/news/newsroom/elli-engineering/parlez-vous-ocpp
- https://www.elli.eco/en/about-elli/news/newsroom/elli-engineering/catch-me-if-you-canmemory-leaks
- https://www.volkswagen-group.com/en/articles/elli-provides-access-to-more-than-one-million-charging-points-across-europe-20189
- https://www.elli.eco/en/tos
- https://shop.elli.eco/en-DE/right-of-withdrawal

**Allego**
- https://www.allego.eu/business/
- https://www.allego.eu/plugandcharge/
- https://www.allego.eu/app/
- https://www.allego.eu/pricing/
- https://www.allego.eu/wp-content/uploads/2026/08/EN-November-2025-User-Condition.pdf
- https://allegohelpcentercpoen.uccbpo.com/2025/09/18/how-can-i-receive-or-download-the-invoice-receipt-for-my-charging-session/
- https://allegohelpcentercpoen.uccbpo.com/2025/09/18/why-does-allego-preauthorize-or-charge-a-reservation-fee-for-a-charging-session/
- https://allegohelpcentercpoen.uccbpo.com/2025/09/18/how-will-i-be-billed-for-plug-and-charge-sessions/

**IONAGE**
- https://www.ionage.in/products/developer-tools
- https://www.ionage.in/products/nexus
- https://www.ionage.in/products/app
- https://play.google.com/store/apps/details?id=com.ionage.app&hl=en_US
- https://www.ionage.in/products/flo
- https://www.ionage.in/customer-stories/bpcl
- https://www.ionage.in/refund-policy
- https://www.ionage.in/terms-and-conditions
- https://www.ionage.in/privacy-policy
- https://www.ionage.in/about-us

**Eco-Movement**
- https://www.eco-movement.com/
- https://developers.eco-movement.com/docs/data-api-user-guide
- https://developers.eco-movement.com/v2.1.1/docs/data-api-faq
- https://www.eco-movement.com/services/station-visibility/
- https://www.eco-movement.com/services/navigation/
- https://developers.eco-movement.com/reference/locations
- https://developers.eco-movement.com/v2.1.1/reference/prices-new
- https://developers.eco-movement.com/reference/tariffs
- https://developers.eco-movement.com/reference/send-credentials
- https://www.eco-movement.com/services/compliance/
- https://developers.eco-movement.com/llms.txt

**CIRRANTIC**
- https://actions.cirrantic.com/en/cirrantic
- https://actions.cirrantic.com/integration-data
- https://actions.cirrantic.com/charging-location-listing
- https://actions.cirrantic.com/charging-service-listing
- https://actions.cirrantic.com/en/charging-wallet-poweredbycirrantic
- https://actions.cirrantic.com/cirrantic-service-portfolio
- https://actions.cirrantic.com/partners

### India, open source, protocols, standards and regulation

**Statiq EVlinq**
- https://www.statiq.in/ev-charging-software/evlinq
- https://www.statiq.in/about-us
- https://statiq.in/blog/2025/12/11/statiq-integrates-5100-hpcl-ev-chargers-into-evlinq-to-expand-indias-ev-charging-network/
- https://www.statiq.in/ev-charging-software/csms
- https://www.statiq.in/termsandconditions-page
- https://www.statiq.in/privacy-policy-page

**Numocity / Siemens**
- https://www.numocity.com/solutions
- https://www.numocity.com/
- https://www.siemens.com/en-us/products/numocity-technologies-charge-point-management-system/
- https://www.siemens.com/en-us/products/numocity-technologies-roaming-hub-interconnect/
- https://www.siemens.com/en-us/ecosystem/numocity-technologies/
- https://www.hubject.com/blog-posts/hubject-announces-strategic-partnership-with-numocity-to-enable-plug-charge-across-global-charging-networks
- https://www.numocity.com/blogs/the-guide-to-using-rfid-cards-for-easy-ev-charging

**NPCI NETC / FASTag**
- https://www.npci.org.in/product/netc
- https://ihmcl.co.in/wp-content/uploads/2025/12/NETC_PG_V2.1.pdf
- https://ihmcl.co.in/wp-content/uploads/2021/07/ICD-2-5-Document.pdf
- https://nhai.gov.in/nhai/sites/default/files/mix_file/FAQ-FASTag.pdf
- https://www.rbi.org.in/scripts/PublicationsView.aspx?Id=23127

**SteVe**
- https://github.com/steve-community/steve
- https://raw.githubusercontent.com/steve-community/steve/master/api-docs.json
- https://github.com/steve-community/steve/wiki/Configuration
- https://github.com/steve-community/steve/wiki/How-SteVe-Supports-OCPP-1.2%2C-1.5%2C-and-1.6
- https://github.com/steve-community/steve/wiki/OCPP-1.6J-Security-Configuration
- https://github.com/steve-community/steve/wiki/Incoming-OCPP-message-validation
- https://github.com/steve-community/steve/issues/1000
- https://openchargealliance.org/participants/powerfill-technologies-ltd/
- https://github.com/steve-community/steve/releases

**CitrineOS**
- https://github.com/citrineos/citrineos-core/releases/tag/v2.0.0
- https://github.com/citrineos/citrineos-core
- https://citrineos.github.io/latest/core-concepts/architecture/
- https://citrineos.github.io/latest/apis/core-api/
- https://github.com/citrineos/citrineos-core/blob/main/apps/ocpi-server/README.md
- https://github.com/citrineos/citrineos-core/blob/main/apps/ocpp-server/README.md
- https://citrineos.github.io/latest/guides/security-profiles/
- https://lfenergy.org/projects/citrineos/
- https://www.linuxfoundation.org/press/lf-energy-citrineos-expands-support-to-ocpp-1.6-enhancing-ev-charging-network-management
- https://citrineos.github.io/latest/roadmap/

**OpenCPO**
- https://opencpo.io/
- https://github.com/opencpo/opencpo
- https://github.com/opencpo/opencpo-core
- https://raw.githubusercontent.com/opencpo/opencpo-core/main/db/schema.sql
- https://raw.githubusercontent.com/opencpo/opencpo-core/main/api/public_sessions.py
- https://raw.githubusercontent.com/opencpo/opencpo-core/main/api/ocpi_management.py
- https://github.com/opencpo/opencpo-charge-app
- https://github.com/opencpo/opencpo-bastion

**EVtivity**
- https://www.evtivity.com/docs/getting-started/introduction/
- https://evtivity.com/api-reference
- https://www.evtivity.com/api-reference/payments
- https://www.evtivity.com/api-reference/sessions
- https://www.evtivity.com/api-reference/ocpi
- https://www.evtivity.com/api-reference/portal-auth
- https://www.evtivity.com/api-reference/portal-guest
- https://www.evtivity.com/api-reference/pnc
- https://www.evtivity.com/security
- https://www.evtivity.com/docs/getting-started/project-structure
- https://github.com/EVtivity/evtivity-csms
- https://github.com/EVtivity/evtivity-csms/blob/main/SECURITY.md

**gocpp**
- https://github.com/shiv3/gocpp
- https://raw.githubusercontent.com/shiv3/gocpp/main/README.md
- https://raw.githubusercontent.com/shiv3/gocpp/main/docs/usage.md
- https://raw.githubusercontent.com/shiv3/gocpp/main/docs/architecture.md
- https://raw.githubusercontent.com/shiv3/gocpp/main/core/storage/transaction.go
- https://raw.githubusercontent.com/shiv3/gocpp/main/core/auth/authenticator.go
- https://raw.githubusercontent.com/shiv3/gocpp/main/core/auth/basic.go
- https://raw.githubusercontent.com/shiv3/gocpp/main/core/auth/mtls.go
- https://raw.githubusercontent.com/shiv3/gocpp/main/addons/README.md
- https://raw.githubusercontent.com/shiv3/gocpp/main/v21/schemas/NotifySettlementRequest.json
- https://raw.githubusercontent.com/shiv3/gocpp/main/v21/schemas/NotifyWebPaymentStartedRequest.json
- https://raw.githubusercontent.com/shiv3/gocpp/main/v21/schemas/TransactionEventRequest.json
- https://raw.githubusercontent.com/shiv3/gocpp/main/SECURITY.md

**OCPI 2.3.0**
- https://evroaming.org/ocpi/
- https://evroaming.org/ocpi-downloads/
- https://github.com/ocpi/ocpi
- https://github.com/ocpi/ocpi/blob/2.3.0/release/core/introduction.asciidoc
- https://github.com/ocpi/ocpi/blob/2.3.0/release/core/credentials.asciidoc
- https://github.com/ocpi/ocpi/blob/2.3.0/release/core/transport_and_format.asciidoc
- https://github.com/ocpi/ocpi/blob/2.3.0/release/core/mod_tokens.asciidoc
- https://github.com/ocpi/ocpi/blob/2.3.0/release/core/mod_sessions.asciidoc
- https://github.com/ocpi/ocpi/blob/2.3.0/release/core/mod_cdrs.asciidoc
- https://github.com/ocpi/ocpi/blob/2.3.0/release/core/mod_invoice_reconciliation.asciidoc
- https://github.com/ocpi/ocpi/blob/2.3.0/release/payments/mod_payments.asciidoc
- https://github.com/ocpi/ocpi/blob/2.3.0/release/core/mod_commands.asciidoc

**OICP 2.3**
- https://github.com/hubject/oicp
- https://github.com/hubject/oicp/releases
- https://hubject.github.io/oicp-emp-2.3-api-doc/
- https://hubject.github.io/oicp-cpo-2.3-api-doc/
- https://github.com/hubject/oicp/blob/master/OICP-2.3/Realease_Notes.asciidoc
- https://support.hubject.com/hc/en-us/articles/9630390528925-Are-all-services-mandatory-for-OICP-2-3
- https://support.hubject.com/hc/en-us/articles/4403421095953-2-6-Implementation-of-web-services
- https://support.hubject.com/hc/en-us/articles/11683277706525-How-can-an-EMP-know-if-a-session-has-stopped
- https://support.hubject.com/hc/en-us/articles/16861952726813-eRoaming-Certificates-at-Hubject
- https://support.hubject.com/hc/en-us/articles/9860500572189-Home-page-Heartbeat-monitoring
- https://github.com/hubject/oicp/blob/master/Hubject%20Acceptable%20Use%20Policy%20v1-0.asciidoc
- https://support.hubject.com/hc/en-us/articles/13806366367517-What-are-the-different-EMP-roles-on-the-Hubject-Platform

**OCA/OCPP**
- https://openchargealliance.org/protocols/ocpp-protocols/
- https://openchargealliance.org/protocols/open-charge-point-protocol/
- https://webstore.iec.ch/en/publication/111418
- https://webstore.iec.ch/en/publication/111422
- https://openchargealliance.org/new-editions-of-the-ocpp-2-1-and-2-0-1-now-available/
- https://openchargealliance.org/ocpp-info-whitepapers/security-operations-guide/
- https://openchargealliance.org/wp-content/uploads/2026/01/ocpp_security_operations_guide-v2.pdf
- https://openchargealliance.org/ocpp-info-whitepapers/signed-meter-values-eichrecht-paper/
- https://openchargealliance.org/ocpp-info-whitepapers/ocpp-qr-code-payment-in-japan/
- https://openchargealliance.org/test-tool/
- https://openchargealliance.org/certification-program/
- https://openchargealliance.org/ocpp-info-whitepapers/
- https://openchargealliance.org/certificationocpp/certification-ocpp-2-0-1/

**ISO 15118 / Plug & Charge PKI**
- https://www.iso.org/standard/77845.html
- https://www.iso.org/standard/87920.html
- https://www.iso.org/standard/84170.html
- https://www.charin.global/technology/plug-charge
- https://www.charin.global/technology/plug-charge/pki/
- https://www.charin.global/media/pages/technology/knowledge-base/2c8d0e1dea-1721839255/charin_interoperability_guide-pki_use_cases_v2.pdf
- https://eur-lex.europa.eu/eli/reg/2023/1804/oj/eng
- https://eur-lex.europa.eu/eli/reg_del/2025/656/oj/eng
- https://transport.ec.europa.eu/system/files/2024-01/stf-tor-eu-emobility-pki-ecosystem-management.pdf
- https://transport.ec.europa.eu/transport-themes/clean-transport/alternative-fuels-sustainable-mobility-europe/alternative-fuels-infrastructure/questions-and-answers-regulation-deployment-alternative-fuels-infrastructure-eu-20231804_en.html
- https://github.com/charinev/opnc

**EU AFIR / CEAP / ESPR**
- https://eur-lex.europa.eu/eli/reg/2023/1804/oj/eng
- https://eur-lex.europa.eu/eli/reg_del/2025/645/oj/eng
- https://eur-lex.europa.eu/eli/reg_impl/2025/655/oj/eng
- https://transport.ec.europa.eu/transport-themes/clean-transport/alternative-fuels-sustainable-mobility-europe/alternative-fuels-infrastructure/questions-and-answers-regulation-deployment-alternative-fuels-infrastructure-eu-20231804_en.html
- https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:52020DC0098
- https://environment.ec.europa.eu/strategy/circular-economy_en
- https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32024R1781

**India DPDP**
- https://www.indiacode.nic.in/indiacode/handle/123456789/22037?view_type=browse
- https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf
- https://www.meity.gov.in/static/uploads/2025/11/c56ceae6c383460ca69577428d36828b.pdf
- https://www.meity.gov.in/static/uploads/2025/11/53450e6e5dc3bcb37b2b05bcc3b4e031f.pdf
- https://www.meity.gov.in/documents/act-and-policies/digital-personal-data-protection-rules-2025-gDOxUjMtQWa
- https://www.meity.gov.in/static/uploads/2025/12/3c7ebbae0e5456f493f486e6845df86b.pdf
- https://www.meity.gov.in/static/uploads/2025/11/cc217843dc3bcb37b2b05bcc3b4e031f.pdf
- https://www.meity.gov.in/static/uploads/2025/11/f6c0837972422cf79d890bfe84cc04d6.pdf

**RBI PA / NETC boundaries**
- https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12896
- https://ihmcl.co.in/wp-content/uploads/2025/12/NETC_PG_V2.1.pdf
- https://www.netc.org.in/
- https://nhai.gov.in/nhai/sites/default/files/mix_file/FAQ-FASTag.pdf
- https://www.npci.org.in/product/netc/product-statistics

**U.S. EV obligations**
- https://www.ecfr.gov/current/title-23/chapter-I/subchapter-G/part-680
- https://www.ecfr.gov/current/title-23/section-680.106
- https://www.ecfr.gov/current/title-23/section-680.116
- https://afdc.energy.gov/laws/12744
- https://afdc.energy.gov/laws/11067
- https://ww2.arb.ca.gov/our-work/programs/electric-vehicle-supply-equipment-evse-standards
- https://leginfo.legislature.ca.gov/faces/codes_displayText.xhtml?division=3.&part=4.&lawCode=CIV&title=1.81.5
- https://cppa.ca.gov/regulations/
- https://openchargealliance.org/protocols/open-charge-point-protocol/
- https://openchargealliance.org/certificationocpp/certification-ocpp-2-0-1/
- https://www.pcisecuritystandards.org/standards/pci-dss/

**PCI / NIST / OWASP / HTTP signatures / mTLS**
- https://www.pcisecuritystandards.org/standards/pci-dss/
- https://www.pcisecuritystandards.org/document_library/?category=pcidss
- https://blog.pcisecuritystandards.org/just-published-pci-dss-v4-0-1
- https://csrc.nist.gov/pubs/sp/800/228/upd1/final
- https://owasp.org/API-Security/editions/2023/en/0x00-header/
- https://www.rfc-editor.org/rfc/rfc9421.html
- https://www.rfc-editor.org/rfc/rfc8705.html

**HTTP / OpenAPI / AsyncAPI / OAuth / OIDC / CloudEvents**
- https://www.rfc-editor.org/rfc/rfc9110
- https://www.rfc-editor.org/rfc/rfc6749
- https://www.rfc-editor.org/rfc/rfc9700
- https://www.rfc-editor.org/rfc/rfc8414
- https://openid.net/specs/openid-connect-core-1_0.html
- https://openid.net/specs/openid-connect-discovery-1_0.html
- https://openid.net/developers/specs/
- https://spec.openapis.org/oas/v3.2.1.html
- https://spec.openapis.org/oas/
- https://www.asyncapi.com/docs/reference/specification/v3.1.0
- https://cloudevents.io/
- https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md
- https://github.com/cloudevents/spec/releases
