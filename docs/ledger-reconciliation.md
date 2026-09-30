# Enigma Money Ledger and Reconciliation

## Principle

Operational state and money state must not be conflated.

## Ledger

Financial amounts should be represented as immutable ledger entries or compensating entries.

Do not silently edit historical monetary facts.

## Required concepts

- currency
- amount
- tax
- fee
- discount
- authorization
- capture
- refund
- dispute
- payable
- receivable
- settlement
- exchange rate
- provider reference
- invoice reference

## Double-entry direction

A future implementation should use a proper double-entry or equivalently auditable accounting model for financial postings. The exact chart of accounts must be designed with accounting and regulatory professionals.

## Reconciliation layers

### Operational

Did the provider perform the requested service?

### Commercial

Does the provider's CDR/invoice agree with the contracted commercial terms?

### Payment

Does the payment processor report agree with Enigma's expected money state?

### Settlement

Does the provider payable/receivable agree with actual settlement?

## Reconciliation record

Each exception should include:

- reconciliation_id
- source systems
- expected value
- observed value
- difference
- currency
- evidence references
- severity
- owner
- status
- resolution
- resolved_at

## Never assume

A successful payment does not prove a successful charging session.

A successful charging session does not prove correct billing.

A correct invoice does not prove successful settlement.

These are separate evidence chains.
