# Problem Definition

## Observed problem

EV users can encounter multiple charging operators with different applications, accounts, authentication methods, wallets, tariffs, availability data, and payment flows.

## Deeper problem

The real fragmentation is across:

1. Identity
2. Discovery
3. Availability
4. Compatibility
5. Authorization
6. Pricing
7. Session control
8. Payment
9. Billing
10. Settlement
11. Receipts
12. Reliability
13. Data semantics
14. Provider integration

## Why aggregation alone is insufficient

A map can aggregate locations without being able to authorize a session.

An app can display a tariff without controlling the transaction.

A roaming connection can authorize charging without providing a unified experience across every network.

Therefore Enigma must treat interoperability as a transaction lifecycle, not a directory.

## Generalized problem

The same structural pattern can appear outside charging:

Provider A owns a service.
Provider B owns another service.
The user needs both.
Each provider has a separate identity, authorization, data model, and payment flow.

Enigma explores whether a common software layer can normalize that complexity.

## Hypothesis

The most valuable product is not the largest directory. It is the layer that reliably converts fragmented provider capabilities into one coherent transaction or journey.

## Validation questions

- How many providers can be connected without bespoke integrations?
- Which standards can be reused?
- What percentage of real-world transactions can be completed end to end?
- Where do failures occur?
- Who pays for interoperability?
- Which data becomes proprietary through network usage?
- Which workflows remain impossible without direct provider agreements?