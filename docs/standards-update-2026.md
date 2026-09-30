# Standards and Regulatory Update — 2026-09-30

## OCPI
OCPI 2.3.0 is the latest public release. It includes optional Payments and Bookings and Invoice Reconciliation in edition 2. EVRoaming Foundation materials describe OCPI 3.0 as draft development with a target around mid-2027.

Sources:
- https://github.com/ocpi/ocpi
- https://evroaming.org/ocpi/

## OCPP
OCPP 2.1 is IEC 63584-210:2025. Current OCA downloads include OCPP 2.1 Edition 2 and OCPP 2.0.1 Edition 4 with 2026 errata. Edition 2 of OCPP 2.1 includes certification profiles and test cases.

Sources:
- https://openchargealliance.org/download-ocpp/
- https://openchargealliance.org/ocpp-2-1-edition-1-is-now-officially-published-by-iec-as-iec-63584-210-2025/
- https://openchargealliance.org/new-editions-of-the-ocpp-2-1-and-2-0-1-now-available/

## ISO 15118
ISO 15118-20:2022 Amendment 1:2026 adds AC DER service, MCS service and an improved security concept. ISO 15118-21:2025 provides a second-generation conformance test plan. ISO/PAS 15118-23:2026 addresses DC charging conformance testing. ISO/CD 15118-202 is under development.

Sources:
- https://www.iso.org/cms/%20render/live/en/sites/isoorg/contents/data/standard/08/79/87920.html?browse=ics
- https://www.iso.org/standard/94023.html
- https://www.iso.org/ics/43.120/x/

## EU AFIR data
AFIR Article 20 requires APIs and public data access. Implementing Regulation 2025/655 requires static data updates within 24 hours and dynamic updates within one minute after changes. CEAP is mandated by 31 December 2026.

Sources:
- https://eur-lex.europa.eu/eli/reg/2023/1804/2025-04-14/eng
- https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202500655
- https://op.europa.eu/en/publication-detail/-/publication/132a219e-f3f5-11ef-b7db-01aa75ed71a1/language-en

## Architectural consequence
Enigma must support protocol version negotiation, adapter versioning, schema evolution, capability discovery, unknown-field tolerance, conformance fixtures, backward compatibility and standards-change monitoring.