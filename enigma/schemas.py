"""Typed, bounded API request/response schemas."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

Scenario = Literal[
    "normal",
    "delayed_webhook",
    "duplicate_event",
    "cdr_mismatch",
    "refund_failure",
    "provider_outage",
    "stale_availability",
]


class TransactionCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    provider_id: Literal["simulator-a", "simulator-b"]
    scenario: Scenario = "normal"
    expected_amount_minor: int = Field(gt=0, le=100_000_000)
    currency: str = Field(min_length=3, max_length=3, pattern=r"^[A-Z]{3}$")


class RefundCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    amount_minor: int | None = Field(default=None, gt=0, le=100_000_000)
    reason: str = Field(min_length=3, max_length=200)

    @field_validator("reason")
    @classmethod
    def strip_reason(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 3:
            raise ValueError("reason must contain at least 3 non-whitespace characters")
        return value


class ErrorBody(BaseModel):
    error_code: str
    message: str
    retryable: bool = False
    correlation_id: str
    remediation_hint: str | None = None
    transaction_id: str | None = None


class TransactionView(BaseModel):
    transaction_id: str
    tenant_id: str
    provider_id: str
    scenario: str
    status: str
    reconciliation_status: str
    currency: str
    expected_amount_minor: int
    billed_amount_minor: int | None
    refunded_amount_minor: int
    correlation_id: str
    version: int
    created_at: datetime
    updated_at: datetime
    started_at: datetime | None
    completed_at: datetime | None
    safety_classification: str


class ReconciliationView(BaseModel):
    reconciliation_id: str
    transaction_id: str
    status: str
    expected_amount_minor: int
    observed_amount_minor: int | None
    currency: str
    difference_minor: int | None
    reason_codes: list[str]
    evidence_ids: list[str]
    owner: str
    resolution: str | None


class TransactionEnvelope(BaseModel):
    transaction: TransactionView


class TransactionList(BaseModel):
    items: list[TransactionView]
    limit: int
    offset: int
    count: int


class StartEnvelope(BaseModel):
    transaction: TransactionView
    error_code: str | None = None
    message: str | None = None
    retryable: bool | None = None


class LifecycleEnvelope(BaseModel):
    transaction: TransactionView
    reconciliation: ReconciliationView | None = None
    action_required: str | None = None
    automatically_resolved: bool | None = None


class RefundEnvelope(BaseModel):
    transaction: TransactionView
    refund: dict[str, Any]
