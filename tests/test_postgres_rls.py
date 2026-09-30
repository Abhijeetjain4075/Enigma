from __future__ import annotations

import os
import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError

from enigma.api import create_app
from enigma.settings import Settings


@pytest.mark.skipif(
    not os.getenv("ENIGMA_TEST_POSTGRES_URL"), reason="requires PostgreSQL NOBYPASSRLS test role"
)
def test_postgres_rls_isolation_and_missing_context_denial() -> None:
    url = os.environ["ENIGMA_TEST_POSTGRES_URL"]
    settings = Settings(
        environment="test",
        database_url=url,
        api_keys={"tenant-one-" + "a" * 40: "tenant-one", "tenant-two-" + "b" * 40: "tenant-two"},
    )
    app = create_app(settings)
    client = TestClient(app)
    create_key = f"rls-test-create-{uuid.uuid4()}"
    tenant_one_key = "tenant-one-" + "a" * 40
    created = client.post(
        "/v1/transactions",
        headers={"X-API-Key": tenant_one_key, "Idempotency-Key": create_key},
        json={"provider_id": "simulator-a", "expected_amount_minor": 100, "currency": "USD"},
    )
    assert created.status_code == 201, created.text
    transaction_id = created.json()["transaction"]["transaction_id"]
    active = created.json()["transaction"]
    stopped = client.post(
        f"/v1/transactions/{transaction_id}/stop",
        headers={
            "X-API-Key": tenant_one_key,
            "Idempotency-Key": f"rls-test-stop-{uuid.uuid4()}",
            "If-Match": str(active["version"]),
        },
    )
    assert stopped.status_code == 200, stopped.text
    assert stopped.json()["transaction"]["status"] == "billed"
    assert stopped.json()["reconciliation"]["status"] == "matched"
    ledger = client.get(
        f"/v1/transactions/{transaction_id}/ledger", headers={"X-API-Key": tenant_one_key}
    ).json()
    assert ledger["balanced"] is True
    assert len(ledger["items"]) == 2
    hidden = client.get(
        f"/v1/transactions/{transaction_id}",
        headers={"X-API-Key": "tenant-two-" + "b" * 40},
    )
    assert hidden.status_code == 404

    with app.state.engine.connect() as connection:
        count = connection.execute(text("SELECT count(*) FROM transactions")).scalar_one()
    assert count == 0, "a database session without tenant context must see no tenant rows"
    with app.state.engine.begin() as connection:
        connection.execute(
            text("SELECT set_config('app.tenant_id', :tenant_id, true)"),
            {"tenant_id": "tenant-one"},
        )
        event_id = connection.execute(
            text(
                "SELECT event_id FROM transaction_events "
                "WHERE aggregate_id = :transaction_id LIMIT 1"
            ),
            {"transaction_id": transaction_id},
        ).scalar_one()
    with pytest.raises(DBAPIError, match="append-only"):
        with app.state.engine.begin() as connection:
            connection.execute(
                text("SELECT set_config('app.tenant_id', :tenant_id, true)"),
                {"tenant_id": "tenant-one"},
            )
            connection.execute(
                text(
                    "UPDATE transaction_events SET payload = '{}'::jsonb WHERE event_id = :event_id"
                ),
                {"event_id": event_id},
            )
    app.state.engine.dispose()
