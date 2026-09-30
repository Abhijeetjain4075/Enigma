from __future__ import annotations

from typing import Any

import pytest
from fastapi.testclient import TestClient

from enigma.api import create_app
from enigma.settings import Settings


@pytest.fixture
def client(tmp_path: Any) -> TestClient:
    settings = Settings(
        environment="test",
        database_url=f"sqlite:///{tmp_path}/test.db",
        api_keys={"tenant-one-secret": "tenant-one", "tenant-two-secret": "tenant-two"},
    )
    return TestClient(create_app(settings))


def headers(key: str = "tenant-one-secret", **extra: str) -> dict[str, str]:
    return {"X-API-Key": key, **extra}


def create_tx(
    client: TestClient,
    *,
    provider: str = "simulator-a",
    scenario: str = "normal",
    idem: str = "create-1",
) -> dict[str, Any]:
    response = client.post(
        "/v1/transactions",
        headers=headers(**{"Idempotency-Key": idem}),
        json={
            "provider_id": provider,
            "scenario": scenario,
            "expected_amount_minor": 1250,
            "currency": "INR",
        },
    )
    assert response.status_code == 201, response.text
    return response.json()["transaction"]


def stop_tx(client: TestClient, tx: dict[str, Any], idem: str = "stop-1") -> Any:
    return client.post(
        f"/v1/transactions/{tx['transaction_id']}/stop",
        headers=headers(**{"Idempotency-Key": idem, "If-Match": str(tx["version"])}),
    )


def test_auth_and_openapi_security(client: TestClient) -> None:
    assert client.get("/health/live").status_code == 200
    assert client.get("/v1/providers").status_code == 401
    schema = client.get("/openapi.json").json()
    assert "APIKeyHeader" in schema["components"]["securitySchemes"]
    assert schema["paths"]["/v1/transactions"]["post"]["security"]


def test_complete_lifecycle_is_idempotent_and_auditable(client: TestClient) -> None:
    tx = create_tx(client)
    assert tx["status"] == "active"
    duplicate = client.post(
        "/v1/transactions",
        headers=headers(**{"Idempotency-Key": "create-1"}),
        json={
            "provider_id": "simulator-a",
            "scenario": "normal",
            "expected_amount_minor": 1250,
            "currency": "INR",
        },
    )
    assert duplicate.status_code == 201
    assert duplicate.headers["Idempotency-Replayed"] == "true"
    assert duplicate.json()["transaction"]["transaction_id"] == tx["transaction_id"]

    stopped = stop_tx(client, tx)
    assert stopped.status_code == 200, stopped.text
    result = stopped.json()
    assert result["transaction"]["status"] == "billed"
    assert result["reconciliation"]["status"] == "matched"
    ledger = client.get(f"/v1/transactions/{tx['transaction_id']}/ledger", headers=headers()).json()
    assert ledger["balanced"] is True
    assert ledger["simulation_only"] is True
    events = client.get(
        f"/v1/transactions/{tx['transaction_id']}/events", headers=headers()
    ).json()["items"]
    assert [item["event_version"] for item in events] == sorted(
        item["event_version"] for item in events
    )
    assert len(events) >= 7
    evidence = client.get(
        f"/v1/transactions/{tx['transaction_id']}/evidence", headers=headers()
    ).json()["items"]
    assert evidence and all(item["evidence_level"] == "E4-simulated" for item in evidence)


def test_idempotency_key_cannot_be_reused_for_different_payload(client: TestClient) -> None:
    create_tx(client, idem="same-key")
    response = client.post(
        "/v1/transactions",
        headers=headers(**{"Idempotency-Key": "same-key"}),
        json={
            "provider_id": "simulator-a",
            "scenario": "normal",
            "expected_amount_minor": 1251,
            "currency": "INR",
        },
    )
    assert response.status_code == 409
    assert response.json()["error_code"] == "idempotency_key_reused"


def test_tenant_isolation_returns_not_found(client: TestClient) -> None:
    tx = create_tx(client)
    response = client.get(
        f"/v1/transactions/{tx['transaction_id']}", headers=headers("tenant-two-secret")
    )
    assert response.status_code == 404
    assert response.json()["error_code"] == "transaction_not_found"


def test_duplicate_provider_cdr_event_is_suppressed(client: TestClient) -> None:
    tx = create_tx(client, provider="simulator-b", scenario="duplicate_event")
    response = stop_tx(client, tx)
    assert response.status_code == 200
    events = client.get(
        f"/v1/transactions/{tx['transaction_id']}/events", headers=headers()
    ).json()["items"]
    cdr_events = [
        item for item in events if item["external_event_id"] == f"{tx['transaction_id']}:cdr:1"
    ]
    assert len(cdr_events) == 1


def test_cdr_mismatch_is_preserved_for_manual_review(client: TestClient) -> None:
    tx = create_tx(client, provider="simulator-b", scenario="cdr_mismatch")
    response = stop_tx(client, tx)
    assert response.status_code == 202
    result = response.json()
    assert result["transaction"]["status"] == "reconciliation_required"
    assert result["reconciliation"]["status"] == "unresolved"
    assert result["reconciliation"]["reason_codes"] == ["amount_mismatch"]
    ledger = client.get(f"/v1/transactions/{tx['transaction_id']}/ledger", headers=headers()).json()
    assert ledger["items"] == []


def test_delayed_cdr_can_be_explicitly_reconciled(client: TestClient) -> None:
    tx = create_tx(client, provider="simulator-b", scenario="delayed_webhook")
    stopped = stop_tx(client, tx)
    assert stopped.status_code == 202
    pending = stopped.json()["transaction"]
    assert pending["status"] == "reconciliation_required"
    recovered = client.post(
        f"/v1/transactions/{tx['transaction_id']}/reconcile",
        headers=headers(**{"Idempotency-Key": "reconcile-1", "If-Match": str(pending["version"])}),
    )
    assert recovered.status_code == 200, recovered.text
    assert recovered.json()["transaction"]["status"] == "billed"
    assert recovered.json()["reconciliation"]["status"] == "matched"


def test_stale_availability_is_not_reported_as_available(client: TestClient) -> None:
    response = client.post(
        "/v1/transactions",
        headers=headers(**{"Idempotency-Key": "stale-1"}),
        json={
            "provider_id": "simulator-b",
            "scenario": "stale_availability",
            "expected_amount_minor": 100,
            "currency": "INR",
        },
    )
    assert response.status_code == 409
    assert response.json()["transaction"]["status"] == "rejected"


def test_temporary_provider_outage_is_visible_and_idempotent(client: TestClient) -> None:
    response = client.post(
        "/v1/transactions",
        headers=headers(**{"Idempotency-Key": "outage-1"}),
        json={
            "provider_id": "simulator-b",
            "scenario": "provider_outage",
            "expected_amount_minor": 100,
            "currency": "INR",
        },
    )
    assert response.status_code == 502
    assert response.json()["transaction"]["status"] == "failed"
    replay = client.post(
        "/v1/transactions",
        headers=headers(**{"Idempotency-Key": "outage-1"}),
        json={
            "provider_id": "simulator-b",
            "scenario": "provider_outage",
            "expected_amount_minor": 100,
            "currency": "INR",
        },
    )
    assert replay.status_code == 502
    assert replay.headers["Idempotency-Replayed"] == "true"
    assert (
        replay.json()["transaction"]["transaction_id"]
        == response.json()["transaction"]["transaction_id"]
    )


def test_refund_is_bounded_and_entries_remain_balanced(client: TestClient) -> None:
    tx = create_tx(client)
    billed = stop_tx(client, tx).json()["transaction"]
    refund = client.post(
        f"/v1/transactions/{tx['transaction_id']}/refunds",
        headers=headers(**{"Idempotency-Key": "refund-1", "If-Match": str(billed["version"])}),
        json={"amount_minor": 500, "reason": "partial correction"},
    )
    assert refund.status_code == 200, refund.text
    assert refund.json()["transaction"]["status"] == "partially_refunded"
    current = refund.json()["transaction"]
    over = client.post(
        f"/v1/transactions/{tx['transaction_id']}/refunds",
        headers=headers(**{"Idempotency-Key": "refund-2", "If-Match": str(current["version"])}),
        json={"amount_minor": 800, "reason": "too much"},
    )
    assert over.status_code == 422
    ledger = client.get(f"/v1/transactions/{tx['transaction_id']}/ledger", headers=headers()).json()
    assert ledger["balanced"] is True
    assert len(ledger["items"]) == 4


def test_refund_provider_failure_does_not_post_refund_ledger(client: TestClient) -> None:
    tx = create_tx(client, provider="simulator-b", scenario="refund_failure")
    billed = stop_tx(client, tx).json()["transaction"]
    response = client.post(
        f"/v1/transactions/{tx['transaction_id']}/refunds",
        headers=headers(**{"Idempotency-Key": "refund-fail", "If-Match": str(billed["version"])}),
        json={"amount_minor": 100, "reason": "test failure"},
    )
    assert response.status_code == 502
    ledger = client.get(f"/v1/transactions/{tx['transaction_id']}/ledger", headers=headers()).json()
    assert len(ledger["items"]) == 2
    assert ledger["balanced"] is True


def test_api_timestamps_are_explicit_utc_and_validation_does_not_echo_input(
    client: TestClient,
) -> None:
    tx = create_tx(client, idem="utc-check")
    assert tx["created_at"].endswith("+00:00")
    assert tx["updated_at"].endswith("+00:00")
    invalid = client.post(
        "/v1/transactions",
        headers=headers(**{"Idempotency-Key": "bad-contract"}),
        json={
            "provider_id": "not-a-provider",
            "expected_amount_minor": 100,
            "currency": "USD",
            "customer_secret": "do-not-echo",
        },
    )
    assert invalid.status_code == 422
    assert invalid.json()["error_code"] == "request_validation_failed"
    assert "do-not-echo" not in invalid.text


def test_mutation_requires_idempotency_key(client: TestClient) -> None:
    response = client.post(
        "/v1/transactions",
        headers=headers(),
        json={"provider_id": "simulator-a", "expected_amount_minor": 10, "currency": "USD"},
    )
    assert response.status_code == 400
    assert response.json()["error_code"] == "idempotency_key_required"
