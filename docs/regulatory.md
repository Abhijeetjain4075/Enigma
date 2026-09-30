# Regulatory and Market-Access Framework

## Principle

Regulatory analysis must follow the actual role Enigma performs, not merely the technology it uses.

For every target market determine whether Enigma is only a software/data intermediary, initiates or receives regulated payments, holds customer funds, is merchant of record, issues invoices, determines taxes, controls infrastructure, processes precise location data, enters consumer contracts, or operates cross-border.

## European Union

Regulation (EU) 2023/1804 (AFIR) establishes requirements around alternative-fuels infrastructure, user information, payment, and data access. It also provides for machine-readable infrastructure data and APIs/national access points.

Enigma must model ad-hoc versus contract charging, transparent price presentation, roaming fees, static and dynamic data, API provenance, national access point ingestion, and operator obligations versus intermediary obligations.

Official source:
https://eur-lex.europa.eu/eli/reg/2023/1804/oj/eng

## India

India-specific analysis must be maintained separately because payment, data protection, EV charging, consumer protection, taxation, and energy regulation can attach to different parties and transactions.

Do not infer that an Indian payment rail makes Enigma itself a licensed payment entity. The exact payment flow and regulated intermediary role must be determined with qualified legal/compliance review.

## Privacy

For India, map the Digital Personal Data Protection Act, 2023 and applicable rules to controller/processor roles, notices, lawful basis as applicable, purpose limitation, retention, security safeguards, breach response, rights workflows, cross-border processing, and children's data where relevant.

Official source:
https://www.meity.gov.in/

## Financial regulation

Before launching money movement, document acquiring relationship, payment aggregator/payment gateway role, merchant-of-record role, settlement account ownership, safeguarding/customer-funds handling, KYC/AML responsibility, chargeback responsibility, refunds, tax invoices, cross-border FX, and sanctions screening where applicable.

## Certification

Protocol conformance and regulatory authorization are different concepts. A protocol certificate does not automatically authorize a commercial payment or mobility service.

## Compliance matrix

| Area | Question | Owner | Evidence | Status |
|---|---|---|---|---|
| Payments | Who legally receives customer money? | Compliance | Contract/licence opinion | TBD |
| Privacy | Who controls personal data? | Privacy | Data-flow map | TBD |
| Charging | Who operates the EVSE? | Partner | Contract | TBD |
| Tax | Who invoices whom? | Finance | Tax analysis | TBD |
| Consumer | Who contracts with end user? | Legal | Terms | TBD |
| Security | Which controls are mandatory? | Security | Control matrix | TBD |

## Rule

No country should be marked launch-ready merely because technical APIs are available.
