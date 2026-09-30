# Standards Evidence Matrix — 2026-09-30

| Standard / regulation | Current evidence | Enigma implication |
|---|---|---|
| OCPI | Official repository identifies 2.3.0 as latest official release; core and optional modules are separately packaged | Model version, module and edition independently |
| OCPP | OCA lists 1.6, 2.0.1 and 2.1; 2.1 adds V2X, DER, battery swapping and ad-hoc payment capabilities | Keep charger/CSMS integration boundary explicit |
| ISO 15118-20 | 2026 amendment published July 2026 | Track amendment and security/DER/MCS implications |
| EU AFIR | Article 20 requires infrastructure data and APIs; delegated regulation 2025/645 specifies common API requirements | Treat regulatory data as a first-class ingestion channel |
| India DPDP | MeitY lists 2025 Rules and enforcement timeline | Update India privacy implementation plan |

## Primary sources

- OCPI: https://github.com/ocpi/ocpi
- OCPP: https://openchargealliance.org/protocols/open-charge-point-protocol/
- ISO 15118-20 amendment: https://www.iso.org/cms/%20render/live/en/sites/isoorg/contents/data/standard/08/79/87920.html?browse=tc
- AFIR: https://eur-lex.europa.eu/legal-content/en/ALL/?uri=CELEX%3A02023R1804-20260108
- AFIR API delegated regulation: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32025R0645
- India DPDP Rules: https://www.meity.gov.in/documents/act-and-policies/digital-personal-data-protection-rules-2025-gDOxUjMtQWa

## Evidence rule

A standard's existence does not mean a provider implements it.

For every adapter, record:
standard version -> provider implementation -> tested subset -> production evidence.
