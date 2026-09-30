# Enigma Authorization and Delegation Model

## Principle

Authentication answers "who are you?" Authorization answers "what are you permitted to do?"

Enigma must model authorization as a policy decision, not as possession of an API token.

## Authorization tuple

A decision should consider:

- principal
- acting application
- tenant/organization
- resource
- operation
- geographic scope
- time window
- provider contract
- user consent/delegation
- risk level
- transaction state
- policy version

## Delegation

A fleet, OEM, enterprise or user may delegate limited authority.

A delegation should define:

- issuer
- delegate
- allowed resources
- allowed operations
- constraints
- issued_at
- expires_at
- revocation state
- evidence

## High-risk operations

Remote start/stop, reservation mutation, financial capture/refund and credential changes require stronger controls than discovery.

Use step-up authorization where risk warrants it.

## Deny by default

Unknown capability, expired delegation, missing provider contract, geographic restriction, policy mismatch or ambiguous identity should produce an explicit denial.

## Audit

Every authorization decision should be attributable to:

- policy version
- subject
- actor
- resource
- operation
- decision
- reason code
- timestamp
- correlation ID

Do not expose internal policy details to untrusted callers beyond what is necessary.

## Provider permissions

A user's Enigma authorization does not create permission at the provider.

Provider commercial/API authorization remains a separate gate.
