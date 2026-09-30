# Enigma Metrics and SLO Framework

## North-star metric

The primary product metric should be **successful end-to-end transactions**, not provider count or station count.

## Funnel

1. eligible request
2. provider/capability match
3. authorization accepted
4. operation initiated
5. service successfully completed
6. correct billing
7. successful settlement/reconciliation

## Core metrics

### Coverage

- providers connected
- assets discovered
- capability coverage
- geographic coverage
- transaction-capable coverage

### Reliability

- authorization success rate
- start success rate
- stop success rate
- session completion rate
- timeout rate
- stale-data rate
- provider error rate
- reconciliation exception rate

### Financial

- gross transaction value
- net revenue
- provider payable
- payment success rate
- refund rate
- chargeback rate
- reconciliation ageing
- integration cost per successful transaction

### Platform

- API latency
- webhook processing latency
- adapter error rate
- retry volume
- dead-letter volume
- uptime
- incident frequency

### Customer

- successful trip/session rate
- repeat usage
- support contacts per transaction
- failed-session recovery rate

## SLO principle

Do not publish a platform-wide reliability number without separating Enigma-controlled failures, provider-controlled failures, network failures, user/device failures, and unknown failures.

## Economic test

For every integration calculate integration_cost + support_cost + payment_cost + compliance_cost + infrastructure_cost versus gross-margin contribution from transactions and contracts.

## Experiment discipline

Every major feature must specify hypothesis, measurable outcome, baseline, target, observation window, failure threshold, and decision after experiment.
