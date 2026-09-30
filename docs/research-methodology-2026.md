# Research Methodology — 2026-09-30

## Evidence hierarchy

- E0: internal hypothesis
- E1: secondary market discovery
- E2: primary public documentation
- E3: provider-confirmed/private evidence
- E4: reproducible integration/sandbox observation
- E5: production observation

Never upgrade E0-E2 to E4/E5 by inference.

## Research passes

### Pass 1 — system decomposition

Map:

`physical asset -> control system -> network -> roaming -> eMSP -> data -> payment -> settlement -> regulatory layer`

### Pass 2 — competitor discovery

Search by function, protocol, geography and customer segment:

- roaming hub
- clearing house
- OCPI provider
- OICP provider
- eMSP
- CPMS/CSMS
- EV API
- charging data
- payment
- Plug & Charge
- fleet
- energy flexibility
- parking
- tolling
- MaaS
- roadside
- maintenance

### Pass 3 — primary verification

Prefer:
- official product documentation
- official standards bodies
- government/regulatory publications
- official API documentation
- official press releases for partnerships

### Pass 4 — capability decomposition

Do not record “supports roaming.” Record:
- protocol/version
- direction
- authorization
- start/stop
- sessions
- CDR
- tariff
- booking
- payment
- settlement
- reconciliation
- dispute support
- API/SDK
- geography
- commercial availability

### Pass 5 — strategic decomposition

For each competitor record:
- customer
- buyer
- user
- distribution
- integration strategy
- network strategy
- pricing/monetization if public
- lock-in mechanism
- switching cost
- partnerships
- standards strategy
- adjacent expansion
- trust/security model

### Pass 6 — adversarial falsification

Ask:
- Could an incumbent add this?
- Could a customer compose existing products?
- Is the problem caused by missing permissions rather than missing software?
- Is the payer obvious?
- Is the value large enough?
- Does the product increase regulatory exposure?
- Does Enigma become a regulated intermediary?
- Does the proposed moat depend on network effects that cannot start at zero?
- Is the feature merely a protocol wrapper?

### Pass 7 — implementation proof

No strategic claim is considered validated until an executable test, sandbox or production observation supports it.

## Search completeness protocol

“Worldwide exhaustive” is not technically provable because:
- private integrations are invisible
- commercial contracts are private
- products change continuously
- regional companies may not index in English
- public websites can be stale
- capabilities may be tenant-specific

Therefore the repository uses a rolling evidence register with:
- source
- URL
- retrieval date
- claim
- evidence level
- geography
- product/version
- contradiction status
- next verification date

## Research output rule

Every source-derived claim committed to the repository must have a source URL nearby. Every strategic conclusion must distinguish observation from hypothesis.

## Revalidation triggers

Re-audit when:
- OCPI/OCPP/ISO versions change
- major roaming hub adds a new domain
- regulatory rules change
- a new real provider integration begins
- payment/settlement flow changes
- Enigma changes customer segment
- a production incident reveals a missing state
