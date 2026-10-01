from datetime import UTC, datetime

import pytest

from enigma.protocol import (
    KeyPair,
    ProtocolError,
    content_hash,
    create_evidence,
    create_event,
    create_intent,
    detect_replay,
    export_bundle,
    import_bundle,
    reconcile_histories,
    verify_event_chain,
    verify_signed,
)

NOW = datetime(2026, 10, 1, 12, 0, tzinfo=UTC)


def _fixture():
    key = KeyPair.generate()
    lookup = {key.key_id: key.secret}
    intent = create_intent(
        key=key,
        nonce="nonce-001",
        principal="did:enigma:customer-1",
        operation="charge.start",
        provider_id="provider-fixture",
        resource_id="charger-1",
        requested_at=NOW,
        authorization_ref="delegation-001",
        parameters={"connector": 1},
    )
    first = create_event(
        key=key,
        transaction_id=intent["transaction_id"],
        sequence=0,
        event_type="intent.created",
        previous_event_hash=None,
        state="created",
        occurred_at=NOW,
        authority="client",
    )
    second = create_event(
        key=key,
        transaction_id=intent["transaction_id"],
        sequence=1,
        event_type="provider.observed",
        previous_event_hash=first["event_hash"],
        state="active",
        occurred_at=NOW,
        authority="provider-fixture",
        payload={"provider_state": "active"},
    )
    evidence = create_evidence(
        key=key,
        transaction_id=intent["transaction_id"],
        source="provider-fixture",
        evidence_type="session",
        observed_at=NOW,
        payload={"external_id": "session-1", "state": "active"},
        authority="provider-fixture",
    )
    return key, lookup, intent, [first, second], [evidence]


def test_authenticated_intent_verifies_without_database() -> None:
    _, lookup, intent, _, _ = _fixture()
    assert verify_signed(intent, lookup)
    assert intent["transaction_id"].startswith("txn_")
    assert len(intent["transaction_id"]) == 68


def test_event_chain_and_content_ids_verify() -> None:
    _, lookup, _, events, _ = _fixture()
    assert verify_event_chain(events, lookup)
    assert all(content_hash(e) for e in events)


def test_tampering_is_detected() -> None:
    _, lookup, intent, events, _ = _fixture()
    intent["operation"] = "charge.stop"
    with pytest.raises(ProtocolError, match="invalid signature"):
        verify_signed(intent, lookup)
    events[1]["state"] = "completed"
    with pytest.raises(ProtocolError):
        verify_event_chain(events, lookup)


def test_replay_is_detected_without_central_store() -> None:
    _, _, _, events, _ = _fixture()
    seen, duplicates = detect_replay(set(), events)
    assert duplicates == []
    _, duplicates = detect_replay(seen, events)
    assert len(duplicates) == 2


def test_independent_histories_reconcile() -> None:
    _, lookup, _, local, _ = _fixture()
    external = [dict(event) for event in local]
    result = reconcile_histories(local, external, lookup)
    assert result["status"] == "matched"


def test_conflicting_histories_become_uncertain() -> None:
    _, lookup, _, local, _ = _fixture()
    external = [dict(event) for event in local]
    external[1] = dict(external[1])
    external[1]["state"] = "completed"
    with pytest.raises(ProtocolError):
        reconcile_histories(local, external, lookup)


def test_bundle_survives_export_import() -> None:
    _, lookup, intent, events, evidence = _fixture()
    bundle = export_bundle(
        intent=intent, events=events, evidence=evidence, key_lookup=lookup
    )
    recovered = import_bundle(bundle, lookup)
    assert recovered == (intent, events, evidence)


def test_bundle_detects_tampering() -> None:
    _, lookup, intent, events, evidence = _fixture()
    bundle = export_bundle(
        intent=intent, events=events, evidence=evidence, key_lookup=lookup
    )
    bundle["bundle_id"] = "bad"
    with pytest.raises(ProtocolError, match="bundle content identifier"):
        import_bundle(bundle, lookup)
