"""Canonical transaction states and deterministic transition validation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum


class TransactionStatus(StrEnum):
    CREATED = "created"
    VALIDATED = "validated"
    AUTHORIZED = "authorized"
    INITIATED = "initiated"
    ACTIVE = "active"
    COMPLETED = "completed"
    BILLED = "billed"
    SETTLED = "settled"
    REJECTED = "rejected"
    EXPIRED = "expired"
    FAILED = "failed"
    CANCELLED = "cancelled"
    DISPUTED = "disputed"
    REFUNDED = "refunded"
    PARTIALLY_REFUNDED = "partially_refunded"
    RECONCILIATION_REQUIRED = "reconciliation_required"


TRANSITIONS: dict[TransactionStatus, frozenset[TransactionStatus]] = {
    TransactionStatus.CREATED: frozenset(
        {
            TransactionStatus.VALIDATED,
            TransactionStatus.REJECTED,
            TransactionStatus.FAILED,
            TransactionStatus.EXPIRED,
            TransactionStatus.CANCELLED,
        }
    ),
    TransactionStatus.VALIDATED: frozenset(
        {
            TransactionStatus.AUTHORIZED,
            TransactionStatus.REJECTED,
            TransactionStatus.FAILED,
            TransactionStatus.EXPIRED,
            TransactionStatus.CANCELLED,
        }
    ),
    TransactionStatus.AUTHORIZED: frozenset(
        {
            TransactionStatus.INITIATED,
            TransactionStatus.FAILED,
            TransactionStatus.CANCELLED,
            TransactionStatus.EXPIRED,
        }
    ),
    TransactionStatus.INITIATED: frozenset(
        {
            TransactionStatus.ACTIVE,
            TransactionStatus.FAILED,
            TransactionStatus.RECONCILIATION_REQUIRED,
            TransactionStatus.CANCELLED,
        }
    ),
    TransactionStatus.ACTIVE: frozenset(
        {
            TransactionStatus.COMPLETED,
            TransactionStatus.FAILED,
            TransactionStatus.RECONCILIATION_REQUIRED,
        }
    ),
    TransactionStatus.COMPLETED: frozenset(
        {TransactionStatus.BILLED, TransactionStatus.RECONCILIATION_REQUIRED}
    ),
    TransactionStatus.BILLED: frozenset(
        {
            TransactionStatus.SETTLED,
            TransactionStatus.DISPUTED,
            TransactionStatus.PARTIALLY_REFUNDED,
            TransactionStatus.REFUNDED,
            TransactionStatus.RECONCILIATION_REQUIRED,
        }
    ),
    TransactionStatus.SETTLED: frozenset(
        {
            TransactionStatus.DISPUTED,
            TransactionStatus.PARTIALLY_REFUNDED,
            TransactionStatus.REFUNDED,
            TransactionStatus.RECONCILIATION_REQUIRED,
        }
    ),
    TransactionStatus.RECONCILIATION_REQUIRED: frozenset(
        {
            TransactionStatus.BILLED,
            TransactionStatus.SETTLED,
            TransactionStatus.DISPUTED,
            TransactionStatus.PARTIALLY_REFUNDED,
            TransactionStatus.REFUNDED,
            TransactionStatus.FAILED,
        }
    ),
    TransactionStatus.PARTIALLY_REFUNDED: frozenset(
        {
            TransactionStatus.PARTIALLY_REFUNDED,
            TransactionStatus.REFUNDED,
            TransactionStatus.DISPUTED,
            TransactionStatus.RECONCILIATION_REQUIRED,
        }
    ),
    TransactionStatus.REJECTED: frozenset(),
    TransactionStatus.EXPIRED: frozenset(),
    TransactionStatus.FAILED: frozenset(),
    TransactionStatus.CANCELLED: frozenset(),
    TransactionStatus.DISPUTED: frozenset(
        {
            TransactionStatus.PARTIALLY_REFUNDED,
            TransactionStatus.REFUNDED,
            TransactionStatus.RECONCILIATION_REQUIRED,
        }
    ),
    TransactionStatus.REFUNDED: frozenset(),
}


class InvalidTransition(ValueError):
    """Raised when a requested state transition is not in the canonical graph."""


def validate_transition(current: str | TransactionStatus, target: str | TransactionStatus) -> None:
    source = TransactionStatus(current)
    destination = TransactionStatus(target)
    if destination not in TRANSITIONS[source]:
        raise InvalidTransition(
            f"Transition {source.value} -> {destination.value} is not permitted"
        )


def utc_now() -> datetime:
    return datetime.now(UTC)


@dataclass(frozen=True, slots=True)
class Provenance:
    source: str
    provider_id: str
    namespace: str
    external_id: str
    observed_at: datetime
    received_at: datetime
    protocol: str
    protocol_version: str
    adapter_version: str
    transformation_version: str
    confidence: float
    conflict_status: str = "none"


@dataclass(frozen=True, slots=True)
class CanonicalEvent:
    event_id: str
    event_type: str
    aggregate_id: str
    event_version: int
    occurred_at: datetime
    received_at: datetime
    producer: str
    correlation_id: str
    causation_id: str | None
    payload_schema_version: str
    payload: dict[str, object]
