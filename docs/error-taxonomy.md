# Enigma Error and Failure Taxonomy

## Principle

Distributed mobility systems fail in ways that ordinary CRUD applications do not. Errors must distinguish user, provider, network, protocol, authorization, money, and reconciliation causes.

## Categories

### Identity
invalid_identity, expired_credential, unknown_vehicle, revoked_delegation

### Authorization
unauthorized, provider_denied, capability_not_supported, contract_missing, geographic_restriction

### Discovery/data
stale_data, malformed_data, conflicting_data, missing_data, unsupported_version

### Network
timeout, connection_failure, dns_failure, rate_limited, provider_unavailable

### Protocol
schema_error, signature_invalid, unsupported_operation, invalid_state_transition

### Service operation
start_rejected, stop_rejected, reservation_failed, session_unknown, provider_operation_uncertain

### Money
payment_declined, capture_failed, refund_failed, chargeback_open, currency_mismatch, tax_mismatch

### Reconciliation
cdr_missing, cdr_mismatch, duplicate_transaction, settlement_mismatch, unknown_external_transaction

## Error contract

Every externally visible error should contain stable error_code, human-readable message, retryable flag, retry_after where applicable, correlation_id, provider_reference where safe, remediation hint, and canonical state impact.

Do not expose provider secrets or internal security details.

## Retry policy

Retries must be operation-specific. Read operations may often be retried. Physical-world commands and financial mutations require idempotency and state confirmation before retry.
