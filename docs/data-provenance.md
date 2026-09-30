# Enigma Data Provenance and Freshness

## Principle

Data is only useful when Enigma can explain where it came from and how fresh it is.

## Observation record

Every externally sourced fact should be associated with:

- source_id
- provider
- namespace
- external_identifier
- observed_at
- received_at
- expires_at where known
- protocol/version
- retrieval method
- transformation version
- confidence
- conflict status

## Freshness classes

Suggested classes:

- real_time
- near_real_time
- periodic
- static
- historical
- unknown

A freshness class is metadata, not a guarantee.

## Conflict handling

If two sources disagree:

1. retain both observations;
2. compare timestamps;
3. compare source authority;
4. apply domain-specific precedence;
5. expose uncertainty where material;
6. record the resolution decision.

Never silently overwrite contradictory evidence.

## Derived intelligence

Reliability scores, predicted availability, price estimates, and routing recommendations are derived data.

Store:

- input evidence references
- model/rule version
- generated_at
- confidence
- expiry
- explanation fields where feasible

## Regulatory data

Regulatory open-data feeds must remain distinguishable from commercial provider feeds because rights, freshness, update cadence, and legal responsibilities differ.
