# Enigma Experimental Protocols — 2026-09-30

## Purpose

Convert strategy into falsifiable measurements.

### 1. Existing-stack reconstruction
Rebuild the target workflow using one roaming hub, one CPMS, one eMSP, one data provider and existing payment infrastructure. Measure integration effort, credentials, latency, failure visibility, reconciliation visibility and support handoffs.

### 2. Capability truth
Compare static existence, dynamic availability, connector compatibility, tariff, authorization eligibility, reservation, payment, contract scope and observed transaction success. Produce one evidence-backed capability decision.

### 3. Failure injection
Inject duplicate commands, delayed webhooks, missing/contradictory CDRs, stale availability, tariff mutation, timeout, partial/duplicate refunds and provider outage. Verify no duplicate transaction effects and explicit recovery states.

### 4. Cross-provider reconciliation
Generate authorization, session, CDR, invoice, settlement and refund records with deliberate mismatches. Measure detection, false matches, unresolved cases and diagnosis time.

### 5. Hub-versus-Enigma composition
Run the same workflow directly against a simulated provider and through a simulated roaming hub. Compare integration complexity, failure information, provider identity, evidence completeness and recovery control.

### 6. Multi-domain orchestration
Simulate charging + parking + toll as independent transactions. Test shared correlation, partial success, cancellation, compensation and provider outage.

### 7. Authorization portability
Model person, vehicle, fleet, provider, time, geography, spend limit, service and credential. Test delegated rights across providers.

### 8. Reliability intelligence
Compare reported availability against observed authorization success, start success, session continuity, completion and billing correctness. Test whether observed transaction history predicts outcome better than availability alone.

### 9. Economics
Measure API cost, infrastructure, support, disputes, payment fees, settlement, data licensing and integration amortization per transaction.

### 10. Incumbent response
For every proposed differentiator ask whether a hub, CPMS, eMSP, data provider, OEM, customer or open-source project can reproduce it.

### 11. Regulatory boundary
Map data roles, payment flow, merchant-of-record, authorization, settlement, consumer protection, tax and cross-border processing.

### 12. Zero-network launch
Assume zero CPOs, zero eMSPs, zero drivers and zero transaction history. Identify a first integration that creates standalone buyer value.

## Survival rule

A hypothesis survives only when problem, residual gap, permission, payer, economics and measurable outcome are all supported by evidence.