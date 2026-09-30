# Enigma Security Threat Model

## Assets

- user identity
- delegated credentials
- provider credentials
- vehicle identity
- physical-world control authority
- payment tokens
- financial ledger
- location/journey history
- provider operational data
- audit evidence
- signing keys

## Trust boundaries

1. user/device -> Enigma
2. partner application -> Enigma
3. Enigma -> provider
4. provider -> Enigma webhook
5. payment provider -> Enigma
6. internal service -> internal service
7. operator -> production control plane

## Threats

### Spoofing
Fake user, provider or webhook identity.

### Tampering
Modified transaction, CDR, tariff, webhook or ledger event.

### Repudiation
Participant disputes whether an operation occurred.

### Information disclosure
Leakage of identity, location, payment or provider data.

### Denial of service
Provider/API flooding, webhook storms, credential abuse.

### Elevation of privilege
A discovery credential gains transaction-control authority.

### Replay
A captured start/stop/refund request is executed again.

### Confused deputy
Enigma performs an action for an application outside the principal's intended authority.

## Highest-risk scenarios

1. unauthorized physical-world operation;
2. duplicate financial capture;
3. forged provider event;
4. credential compromise;
5. incorrect settlement;
6. mass location-data exposure.

## Required controls

- strong authentication
- scoped authorization
- short-lived credentials where possible
- signing verification
- replay protection
- idempotency
- immutable audit events
- secrets management
- key rotation
- rate limiting
- circuit breakers
- anomaly detection
- tenant isolation
- incident response
- recovery testing

## Security testing

Test both expected and adversarial flows.

A successful happy-path integration is not security evidence.
