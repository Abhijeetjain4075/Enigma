# Enigma Security and Privacy Model

## Threat model

Enigma sits between users, applications, providers, physical-world services, and money movement. The highest-impact threats include:

- account takeover
- credential theft
- unauthorized charging/session control
- replayed start/stop requests
- payment fraud
- provider impersonation
- webhook forgery
- API abuse
- privilege escalation
- data exfiltration
- location surveillance
- malicious or compromised provider integrations
- supply-chain compromise
- incorrect reconciliation
- denial of service
- insider misuse

## Security boundaries

Separate:

1. public discovery data
2. partner integration credentials
3. user identity
4. vehicle identifiers
5. location/telemetry
6. authorization tokens
7. payment tokens
8. financial ledger
9. operational control plane
10. analytics/derived data

No component should receive broader privileges than its operation requires.

## Authentication

Use strong authentication for users and partners.

For delegated access, distinguish:

- who the principal is
- what application is acting
- what provider granted access
- what operation is authorized
- for how long
- on which resource

## Webhook security

Provider callbacks should use, where available:

- signature verification
- timestamp/replay protection
- endpoint authentication
- event IDs
- schema validation
- idempotent processing

## Physical-world action policy

Remote start/stop and similar actions are high-impact operations.

Require:

- explicit authorization
- resource binding
- anti-replay protection
- idempotency
- policy checks
- audit event
- provider response correlation

## Financial security

Never store raw card credentials unless a properly scoped compliant architecture requires it. Prefer tokenized payment-provider integrations.

Financial records should be immutable through compensating entries rather than silent mutation.

## Privacy

Location, journey, vehicle, and charging data can reveal sensitive behavioral patterns.

Apply:

- data minimization
- purpose limitation
- retention limits
- access controls
- tenant isolation
- encryption in transit and at rest
- deletion/erasure workflows where applicable
- audit logging
- privacy-preserving analytics where possible

## India

If operating in India, the Digital Personal Data Protection Act, 2023 and associated rules/regulatory requirements must be mapped to the actual role Enigma takes in processing personal data. The repository must not assume that being a software platform eliminates data-protection obligations.

## Security engineering requirements

Before production:

- dependency scanning
- secret scanning
- SAST
- DAST
- API abuse testing
- threat-model review
- penetration testing
- incident-response plan
- backup/restore tests
- key rotation
- access review
- disaster recovery exercise

## Security principle

The most dangerous Enigma failure is not a broken map. It is an incorrect physical-world or financial action. Security controls should therefore be strongest around authorization, transaction execution, and money.
