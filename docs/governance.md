# Enigma Governance and Change Control

## Purpose

Enigma spans protocols, providers, money, personal data and physical-world operations. Governance must therefore be explicit.

## Change classes

### Documentation
Research, strategy, glossary and explanatory material.

### Architecture
Canonical models, state machines, API contracts and security boundaries.

### External dependency
Protocol, provider API, regulation or commercial dependency changes.

### Production-risk
Changes capable of affecting authorization, physical-world operations, money, identity or personal data.

## Required evidence

Production-risk changes require:

- owner
- rationale
- threat/security review
- test evidence
- rollback plan
- monitoring plan
- regulatory/commercial review where applicable

## Architecture Decision Records

Material architectural decisions should be recorded as ADRs with:

- context
- alternatives
- decision
- consequences
- reversal conditions

## External change monitoring

Monitor:

- protocol releases
- regulatory changes
- provider API changes
- provider commercial terms
- security advisories
- dependency vulnerabilities

## No silent breaking changes

Breaking changes to canonical APIs, events, adapters or financial semantics require explicit versioning and migration documentation.

## Research integrity

Do not remove contradictory evidence merely because it weakens the Enigma thesis.

A strong research system preserves disconfirming evidence.
