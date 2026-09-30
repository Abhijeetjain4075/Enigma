# Enigma Competitive Comparison Framework

## Purpose

Avoid comparing fundamentally different businesses using a single "competitor" label.

## Capability matrix

| Capability | Roaming hub | eMSP | Aggregator | CSMS | OEM platform | Enigma hypothesis |
|---|---:|---:|---:|---:|---:|---:|
| Static discovery | yes | yes | yes | often | yes | yes |
| Live availability | often | often | often | yes | often | yes |
| Tariff normalization | often | often | often | provider-specific | often | yes |
| Cross-network authorization | core capability | core capability | varies | usually provider-facing | varies | target |
| Session control | often | often | varies | core/provider-facing | varies | target |
| CDR/billing | often | often | varies | provider-facing | often | target |
| Settlement | often | often | varies | provider-specific | varies | target |
| Cross-domain orchestration | limited/varies | limited | limited | limited | varies | strategic hypothesis |
| Independent reliability evidence | varies | varies | varies | provider-local | varies | strategic hypothesis |
| Universal developer abstraction | varies | varies | varies | provider APIs | varies | strategic hypothesis |

This table is a hypothesis framework, not a claim that every company in a category has identical capabilities.

## Competitor evidence

### Hubject/intercharge

Hubject describes intercharge as a shared eRoaming network connecting CPOs and eMSPs, including automated authorization and settlement.

Source:
https://www.hubject.com/intercharge-overview

### OCPI ecosystem

OCPI itself demonstrates that interoperability is already standardized at multiple levels of the charging transaction lifecycle.

Source:
https://github.com/ocpi/ocpi

## Strategic implication

The competitive question is not "Can Enigma show many chargers?" It is "Can Enigma create a materially better, more neutral, more reliable, more programmable transaction abstraction than the combination of existing roaming, eMSP, OEM and provider APIs?"

That proposition requires empirical validation.

## Required competitor record

Every competitor entry should eventually contain company, product, role, geography, protocols, data coverage, transaction capabilities, payment role, settlement role, API/SDK, commercial model, customer segment, certifications, public evidence, and last verified date.

Do not treat an unverified feature as a fact.
