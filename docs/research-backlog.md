# Enigma Research Backlog

This backlog is intentionally explicit so "everything" means a controlled research program rather than an unbounded list.

## Market structure

- Build a verified global CPO/eMSP/roaming/provider dataset.
- Map provider coverage by country.
- Map direct versus hub connectivity.
- Compare commercial integration requirements.
- Estimate integration cost per provider.
- Interview CPOs, eMSPs, OEMs, fleets, navigation providers and payment providers.

## Transaction economics

- Model CPO -> eMSP -> hub -> payment-provider money flows.
- Identify where Enigma could create incremental value without duplicating existing hub economics.
- Quantify gross margin per transaction.
- Model refunds, disputes, taxes and FX.

## Technical

- Build canonical charging schema.
- Build OCPI adapter prototype.
- Evaluate OICP integration requirements.
- Evaluate OCPP only where direct CSMS connectivity is strategically necessary.
- Evaluate ISO 15118 data/control boundaries.
- Build event replay and reconciliation prototype.

## Reliability

- Define session-success ground truth.
- Build freshness scoring.
- Build provider health scoring.
- Define confidence and evidence models.
- Develop failure taxonomy from real sessions.

## Security/privacy

- Produce full data-flow diagrams.
- Perform threat modeling.
- Define tenant isolation.
- Define secret lifecycle.
- Define location-data retention.
- Map privacy obligations by launch market.

## Regulatory

- EU AFIR implementation details by Member State.
- India payment role analysis.
- India EV charging rules and state-level differences.
- Data protection implementation requirements.
- Cross-border data transfer requirements.
- Consumer-contract obligations.
- Tax/invoicing requirements.

## Competitive

- Verify every named competitor in competitive-landscape.md.
- Record primary evidence and last-verified date.
- Compare APIs, protocols, transaction depth and commercial models.
- Track new entrants and product changes continuously.

## Product validation

- Recruit design partners.
- Run transaction-level pilots.
- Measure completed sessions rather than app installs.
- Test embedded API distribution before building a large consumer app.

## Decision gate

The next implementation should begin only when one concrete workflow has:

- a paying or committed customer;
- at least one permitted provider integration;
- measurable transaction value;
- defined regulatory responsibility;
- a reliable failure/reconciliation strategy.
