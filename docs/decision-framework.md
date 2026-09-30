# Enigma Decision Framework

## Purpose

Prevent scope expansion from becoming uncontrolled feature accumulation.

## New capability gate

A new capability must answer:

### A. Fragmentation
What independent systems currently do not interoperate?

### B. Canonical primitive
Which Enigma primitive solves the mismatch?

Provider, Asset, Capability, Identity, Authorization, Service, Session, Transaction, MoneyMovement, Evidence, Contract, Journey.

### C. Adapter feasibility
Can Enigma observe or execute the required operation through a permitted integration?

### D. Commercial permission
Does the provider permit the proposed use?

### E. Regulatory boundary
Which entity legally performs the activity?

### F. Reliability
What evidence will establish whether the operation succeeded?

### G. Economics
Who pays and what is the gross-margin contribution?

### H. Distribution
Which application, OEM, fleet, provider or user brings demand?

### I. Moat
What becomes harder to replicate if the capability succeeds?

## Domain expansion test

A new domain should be added only if it reuses several core primitives and creates meaningful transaction value.

Examples:

Parking can reuse Provider, Asset, Availability, Reservation, Authorization, Transaction and MoneyMovement.

Random unrelated consumer content cannot.

## Kill criteria

Pause a capability when integration permissions are unavailable, required data cannot be obtained reliably, economics are negative without strategic justification, legal responsibility is unresolved, reliability cannot be measured, or the feature is easily replicated and has no distribution advantage.

## Evidence ladder

1. hypothesis
2. desk research
3. provider documentation
4. provider conversation
5. sandbox test
6. controlled production transaction
7. repeated production evidence
8. scalable unit economics

Do not use level 1-3 evidence to claim level 6-8 capability.
