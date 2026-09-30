# Residual Gap Hypotheses

## Falsification-first method

For every proposed Enigma capability:

1. State the exact user/operator problem.
2. Enumerate existing systems that can already solve it.
3. Test whether those systems can be composed.
4. Measure the remaining friction.
5. Identify the party that pays for removing it.
6. Verify permission, liability and regulatory perimeter.
7. Build only if a persistent residual gap remains.

## Candidate residual gaps

### A. Cross-hub transaction assurance

Hypothesis: A customer using multiple roaming hubs/direct providers needs one neutral evidence model for conflicting session, tariff, authorization, CDR and settlement outcomes.

Potential value:
- reduce disputed sessions
- shorten incident resolution
- identify provider-side contradictions
- preserve evidence for audit

Falsifier:
If a customer's existing hub/CPMS/eMSP stack already provides equivalent evidence, reconciliation and dispute workflow at acceptable cost, this is not a product gap.

### B. Capability truth rather than directory truth

Hypothesis: A directory says a charger exists; a capability graph says what can actually be done now, for this user, vehicle, contract, provider, protocol and geography.

Required dimensions:
- operation
- actor
- protocol
- geography
- contract
- payment
- time
- freshness
- reliability
- evidence level

Falsifier:
If provider APIs plus existing data vendors can produce equivalent capability decisions with no material gap, do not build a separate layer.

### C. Cross-domain transaction orchestration

Hypothesis: A journey can require charging + parking + toll + reservation + service recovery, but each domain has different providers and transaction semantics.

Value:
- one policy engine
- one correlation ID
- one journey state
- compensating actions
- unified evidence

Falsifier:
If a single existing MaaS/enterprise platform can coordinate the exact workflow without material integration duplication, Enigma should integrate with it rather than replace it.

### D. Provider-neutral reliability evidence

Hypothesis: “available” is not equivalent to “likely to complete a transaction.”

Potential model:
`availability -> capability -> authorization success rate -> start success rate -> energy delivery -> completion -> billing correctness`

Falsifier:
If high-quality commercial data providers already expose sufficiently granular reliability and transaction-success evidence, Enigma needs a different differentiator.

### E. Portable constrained authorization

Hypothesis: Users, fleets, OEMs and applications need delegated rights that survive movement between providers while remaining bounded by geography, time, spend, operation and policy.

Falsifier:
If existing identity, payment and roaming credentials already support this without fragmentation, no new authorization layer is justified.

### F. Neutral transaction graph

Hypothesis: The market lacks a neutral graph joining person/vehicle/organization, provider, capability, authorization, session, money movement, evidence and recovery across multiple networks.

Falsifier:
If enterprise mobility platforms already expose equivalent graph semantics and APIs, Enigma should consume rather than recreate them.

## Most important strategic rule

Do not choose a hypothesis because it sounds technically advanced.

Choose it only after:

`documented pain + existing-stack failure + permission + payer + measurable outcome`

## Required experiment matrix

For each hypothesis measure:

- integration hours saved
- transactions covered
- failure detection latency
- dispute rate
- recovery rate
- false availability rate
- reconciliation exception rate
- provider onboarding time
- marginal transaction cost
- support contacts per 1,000 transactions
- regulatory/legal overhead

No hypothesis becomes a product decision before these are measured.
