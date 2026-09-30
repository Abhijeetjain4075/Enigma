"""Versioned simulator adapters. These never call real providers or control physical equipment."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Protocol

from enigma.domain import utc_now

ADAPTER_VERSION = "simulator-adapter/0.1.0"
TRANSFORMATION_VERSION = "canonical/0.1.0"
PROTOCOL = "enigma-simulator"
PROTOCOL_VERSION = "1.0"


class ProviderFailure(RuntimeError):
    def __init__(self, code: str, message: str, *, retryable: bool = False) -> None:
        super().__init__(message)
        self.code = code
        self.retryable = retryable


@dataclass(frozen=True, slots=True)
class Capability:
    operation: str
    state: str
    evidence_level: str
    observed_at: datetime
    expires_at: datetime | None
    source: str
    protocol: str = PROTOCOL
    protocol_version: str = PROTOCOL_VERSION


@dataclass(frozen=True, slots=True)
class ProviderResult:
    operation: str
    external_id: str
    observed_at: datetime
    payload: dict[str, object]


class ProviderAdapter(Protocol):
    provider_id: str
    adapter_version: str

    def get_capabilities(self, scenario: str) -> list[Capability]: ...

    def health_check(self) -> dict[str, object]: ...

    def authorize(self, transaction_id: str, scenario: str) -> ProviderResult: ...

    def start(self, transaction_id: str, scenario: str) -> ProviderResult: ...

    def stop(self, transaction_id: str, scenario: str, amount_minor: int) -> ProviderResult: ...

    def get_cdr(
        self, transaction_id: str, scenario: str, amount_minor: int, currency: str
    ) -> ProviderResult: ...

    def refund(self, transaction_id: str, scenario: str, amount_minor: int) -> ProviderResult: ...


class SimulatedProvider:
    adapter_version = ADAPTER_VERSION

    def __init__(self, provider_id: str, *, stress_provider: bool) -> None:
        self.provider_id = provider_id
        self.stress_provider = stress_provider

    def get_capabilities(self, scenario: str) -> list[Capability]:
        now = utc_now()
        is_stale = self.stress_provider and scenario == "stale_availability"
        expiry = now - timedelta(minutes=10) if is_stale else now + timedelta(minutes=5)
        freshness = "stale" if is_stale else "recently_observed"
        return [
            Capability("discover", "supported", "E4-simulated", now, expiry, self.provider_id),
            Capability("authorize", "supported", "E4-simulated", now, expiry, self.provider_id),
            Capability("start", "supported", "E4-simulated", now, expiry, self.provider_id),
            Capability("stop", "supported", "E4-simulated", now, expiry, self.provider_id),
            Capability("cdr", "supported", "E4-simulated", now, expiry, self.provider_id),
            Capability("refund", "simulated_only", "E4-simulated", now, expiry, self.provider_id),
            Capability("availability", freshness, "E4-simulated", now, expiry, self.provider_id),
        ]

    def health_check(self) -> dict[str, object]:
        return {
            "provider_id": self.provider_id,
            "mode": "simulated",
            "healthy": True,
            "real_provider_connected": False,
        }

    def authorize(self, transaction_id: str, scenario: str) -> ProviderResult:
        self._raise_outage(scenario)
        return self._result(
            "authorization.accepted", f"{transaction_id}:authorization:1", {"decision": "accepted"}
        )

    def start(self, transaction_id: str, scenario: str) -> ProviderResult:
        self._raise_outage(scenario)
        return self._result("session.started", f"{transaction_id}:session:1", {"state": "active"})

    def stop(self, transaction_id: str, scenario: str, amount_minor: int) -> ProviderResult:
        self._raise_outage(scenario)
        return self._result(
            "session.stopped", transaction_id, {"state": "completed", "amount_minor": amount_minor}
        )

    def get_cdr(
        self, transaction_id: str, scenario: str, amount_minor: int, currency: str
    ) -> ProviderResult:
        self._raise_outage(scenario)
        observed_at = utc_now()
        if self.stress_provider and scenario == "delayed_webhook":
            raise ProviderFailure(
                "provider_event_delayed", "CDR event has not arrived yet", retryable=True
            )
        observed_amount = amount_minor
        if self.stress_provider and scenario == "cdr_mismatch":
            observed_amount = amount_minor + max(1, int(Decimal(amount_minor) * Decimal("0.07")))
        return ProviderResult(
            operation="cdr.received",
            external_id=f"{transaction_id}:cdr:1",
            observed_at=observed_at,
            payload={
                "amount_minor": observed_amount,
                "currency": currency,
                "source_status": "final",
            },
        )

    def refund(self, transaction_id: str, scenario: str, amount_minor: int) -> ProviderResult:
        if self.stress_provider and scenario == "refund_failure":
            raise ProviderFailure("refund_failed", "Simulator B injected a refund failure")
        return self._result(
            "refund.accepted", f"{transaction_id}:refund:1", {"amount_minor": amount_minor}
        )

    @staticmethod
    def _raise_outage(scenario: str) -> None:
        if scenario == "provider_outage":
            raise ProviderFailure(
                "provider_unavailable", "Simulator injected a provider outage", retryable=True
            )

    def _result(
        self, operation: str, external_id: str, payload: dict[str, object]
    ) -> ProviderResult:
        return ProviderResult(operation, external_id, utc_now(), payload)


def provider_registry() -> dict[str, SimulatedProvider]:
    return {
        "simulator-a": SimulatedProvider("simulator-a", stress_provider=False),
        "simulator-b": SimulatedProvider("simulator-b", stress_provider=True),
    }


def scenario_supported(provider_id: str, scenario: str) -> bool:
    allowed = {
        "simulator-a": {"normal"},
        "simulator-b": {
            "normal",
            "delayed_webhook",
            "duplicate_event",
            "cdr_mismatch",
            "refund_failure",
            "provider_outage",
            "stale_availability",
        },
    }
    return scenario in allowed.get(provider_id, set())
