# Strategy

## Starting point

The visible problem is fragmented charging applications.

The strategic opportunity is interoperability software, but generic EV roaming is already a mature category.

## What not to build as the core thesis

Do not compete primarily on:

- another charger map
- another generic charging wallet
- another social EV app
- a large static database
- a hardware network
- basic OCPI connectivity
- basic managed roaming
- basic CPO/eMSP authorization
- basic CDR/tariff normalization

These can be implementation components, but they are not sufficient differentiation.

## Competitive reality

Current products from Hubject, Plugsurfing, ChargeHub, GIREVE, Last Mile Solutions, IONAGE, Numocity and others demonstrate that roaming, multi-network access, CPO/eMSP connectivity, payment/settlement workflows, APIs and charging-management software already exist in substantial combinations.

See docs/competitive-pressure-2026.md.

## Potential differentiation hypotheses

### 1. Cross-provider transaction assurance

Represent and verify the complete lifecycle of a transaction across independent systems, including uncertain outcomes, evidence, recovery and reconciliation.

### 2. Provider-neutral capability graph

Model what each provider can actually do, in which geography, under which contract, through which protocol and with what freshness/reliability.

### 3. Cross-domain orchestration

Coordinate charging with parking, tolls, maintenance, roadside assistance and other mobility services as one journey-level workflow.

### 4. Multi-network-of-networks abstraction

Enigma may consume multiple existing roaming hubs and direct provider connections instead of attempting to replace every network. The abstraction would be above the individual roaming hub.

### 5. Evidence-based reliability intelligence

Treat observed transaction outcomes, provider evidence and data freshness as first-class evidence. Do not equate an API status field with ground truth.

### 6. Portable authorization and delegation

Research whether user, fleet, OEM and application authorization can be represented as portable, policy-constrained delegation across independent providers.

### 7. Neutral transaction graph

Represent relationships among parties, capabilities, services, sessions, money movements and evidence in a graph that can span providers and domains.

## Potential moat

The strongest moat hypotheses are:

- provider network
- transaction history
- normalized data
- reliability intelligence
- integration infrastructure
- settlement workflows
- developer ecosystem
- enterprise contracts
- cross-domain transaction graph

None is a moat merely because it exists. Each requires scale, proprietary evidence, distribution, switching costs, or contractual/network effects.

## Strategic analogy

UPI is useful as an architectural analogy because it separated interoperability from ownership of underlying bank accounts and merchant businesses.

Enigma can explore a similar separation between mobility transactions and ownership of physical infrastructure.

The analogy does not imply that Enigma should copy UPI's governance, licensing, settlement model, or technical architecture.

## Critical constraint

The platform cannot declare itself a universal network before it has real provider participation.

Network claims must always distinguish:

- listed
- data-connected
- authorization-connected
- session-connected
- payment-connected
- fully reconciled.

## Wedge principle

Start narrow enough to achieve transaction reliability, but design the core abstractions so adjacent domains can be added without rewriting the platform.

## Falsification rule

If existing roaming hubs, eMSPs, OEM platforms and direct APIs solve the selected workflow at acceptable economics, Enigma should not build a duplicate layer merely because the architecture is interesting.

The first product must therefore be selected only after a documented "existing-stack residual gap" is demonstrated.
