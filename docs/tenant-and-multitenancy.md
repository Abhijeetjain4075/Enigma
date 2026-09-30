# Enigma Tenant and Multi-Party Isolation

## Principle

Enigma may serve users, fleets, OEMs, eMSPs, CPOs, developers and enterprises simultaneously. Their data and permissions must not leak across tenant boundaries.

## Tenant dimensions

Potential tenant types:

- consumer application
- fleet
- OEM
- CPO
- eMSP
- enterprise
- developer
- internal operations

## Isolation

Enforce isolation at:

- API authorization
- database query
- object storage
- event delivery
- logs
- analytics
- support tooling
- secrets
- webhooks

## Cross-tenant relationships

A transaction may legitimately reference multiple parties. That does not mean every party can read the whole transaction.

Use explicit field/resource-level visibility rules.

## Operational access

Support staff should receive time-bound, audited access.

Production break-glass access must be:

- justified
- approved
- time limited
- logged
- reviewable

## No implicit trust

A provider credential must never grant access to another provider's data.

A developer API key must never inherit internal operator privileges.
