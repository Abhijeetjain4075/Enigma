# Enigma Consent, Privacy and Data Governance

## Data classes

Classify data into:

1. public infrastructure data
2. partner operational data
3. account/identity data
4. vehicle data
5. location/journey data
6. payment/financial data
7. telemetry
8. derived intelligence
9. security/audit data

## Purpose binding

Every non-public data element should have:

- purpose
- legal basis where applicable
- source
- controller/processor role
- retention rule
- access policy
- sharing policy
- deletion/archival rule

## Location

Location and journey information should be treated as high-sensitivity operational data because longitudinal traces can reveal behavior even when names are removed.

Use coarse location when exact location is not required.

## Consent

Consent, where used, must be distinguishable from:

- contract necessity
- legal obligation
- legitimate/other applicable basis
- security necessity

Do not treat every processing activity as consent-based.

## Data subject workflows

The production design must support applicable:

- access
- correction
- deletion/erasure
- withdrawal
- grievance
- restriction/objection where applicable
- portability where applicable

Exact rights and exceptions depend on the jurisdiction and role.

## Retention

Retention must be purpose-specific.

Financial and legal records may require longer retention than operational telemetry. The retention schedule must be documented rather than using one global TTL.

## Governance

Data lineage should be reviewable from source -> transformation -> derived output -> consumer.

## India

The Digital Personal Data Protection Act, 2023 and Digital Personal Data Protection Rules, 2025 must be incorporated into the India launch compliance workstream, including their phased enforcement timeline.

Primary source:
https://www.meity.gov.in/documents/act-and-policies/digital-personal-data-protection-rules-2025-gDOxUjMtQWa
