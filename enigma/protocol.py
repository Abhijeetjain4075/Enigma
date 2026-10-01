"""Backendless Enigma protocol primitives.

The prototype is independent of the SQL/FastAPI simulator. It proves that
transaction intent, local event history, evidence, replay detection,
reconciliation, and recovery bundles do not inherently require an Enigma
database.

The prototype uses a standard-library keyed MAC so the repository's locked
dependency graph remains unchanged. Production identity should replace the
keyed authenticator with an asymmetric scheme such as Ed25519 plus an explicit
trust/key-discovery mechanism. A valid MAC/signature never grants provider
authorization.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import secrets
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, Mapping

PROTOCOL = "enigma-protocol"
PROTOCOL_VERSION = "0.1"
ALGORITHM = "HMAC-SHA256"


class ProtocolError(ValueError):
    """Raised when a protocol object is malformed or unverifiable."""


def _canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def content_hash(value: Any) -> str:
    return hashlib.sha256(_canonical(value)).hexdigest()


def _b64(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode("ascii")


def _unb64(value: str) -> bytes:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))


def _utc(value: datetime) -> str:
    if value.tzinfo is None:
        value = value.replace(tzinfo=UTC)
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True, slots=True)
class KeyPair:
    """Local issuer/verifier key material for the prototype MAC scheme."""

    secret: bytes

    @classmethod
    def generate(cls) -> "KeyPair":
        return cls(secrets.token_bytes(32))

    @property
    def key_id(self) -> str:
        return "hmac:" + hashlib.sha256(self.secret).hexdigest()[:32]


KeyLookup = Mapping[str, bytes]


def _authenticate(payload: dict[str, Any], key: KeyPair) -> dict[str, Any]:
    unsigned = {k: v for k, v in payload.items() if k != "signature"}
    mac = hmac.new(key.secret, _canonical(unsigned), hashlib.sha256).digest()
    return {
        **unsigned,
        "signature": {
            "algorithm": ALGORITHM,
            "key_id": key.key_id,
            "value": _b64(mac),
        },
    }


def verify_signed(payload: dict[str, Any], key_lookup: KeyLookup) -> bool:
    signature = payload.get("signature")
    if not isinstance(signature, dict):
        raise ProtocolError("missing signature")
    if signature.get("algorithm") != ALGORITHM:
        raise ProtocolError("unsupported authentication algorithm")
    key_id = signature.get("key_id")
    if not isinstance(key_id, str):
        raise ProtocolError("missing key identifier")
    try:
        secret = key_lookup[key_id]
    except KeyError as exc:
        raise ProtocolError("unknown signing key") from exc
    unsigned = {k: v for k, v in payload.items() if k != "signature"}
    expected = hmac.new(secret, _canonical(unsigned), hashlib.sha256).digest()
    try:
        actual = _unb64(str(signature["value"]))
    except (ValueError, TypeError) as exc:
        raise ProtocolError("invalid authentication value") from exc
    if not hmac.compare_digest(actual, expected):
        raise ProtocolError("invalid signature")
    return True


def deterministic_transaction_id(
    *, issuer_key_id: str, nonce: str, intent_body: dict[str, Any]
) -> str:
    if not issuer_key_id or not nonce:
        raise ProtocolError("issuer_key_id and nonce are required")
    return "txn_" + content_hash(
        {
            "protocol": PROTOCOL,
            "version": PROTOCOL_VERSION,
            "issuer_key_id": issuer_key_id,
            "nonce": nonce,
            "intent": intent_body,
        }
    )


def create_intent(
    *,
    key: KeyPair,
    nonce: str,
    principal: str,
    operation: str,
    provider_id: str,
    resource_id: str,
    requested_at: datetime,
    authorization_ref: str | None = None,
    parameters: dict[str, Any] | None = None,
) -> dict[str, Any]:
    body = {
        "protocol": PROTOCOL,
        "protocol_version": PROTOCOL_VERSION,
        "type": "transaction_intent",
        "issuer": key.key_id,
        "nonce": nonce,
        "principal": principal,
        "operation": operation,
        "provider_id": provider_id,
        "resource_id": resource_id,
        "requested_at": _utc(requested_at),
        "authorization_ref": authorization_ref,
        "parameters": parameters or {},
    }
    body["transaction_id"] = deterministic_transaction_id(
        issuer_key_id=key.key_id, nonce=nonce, intent_body=body
    )
    return _authenticate(body, key)


def create_event(
    *,
    key: KeyPair,
    transaction_id: str,
    sequence: int,
    event_type: str,
    previous_event_hash: str | None,
    state: str,
    occurred_at: datetime,
    authority: str,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if sequence < 0:
        raise ProtocolError("sequence must be non-negative")
    body = {
        "protocol": PROTOCOL,
        "protocol_version": PROTOCOL_VERSION,
        "type": "transaction_event",
        "transaction_id": transaction_id,
        "sequence": sequence,
        "event_type": event_type,
        "previous_event_hash": previous_event_hash,
        "state": state,
        "occurred_at": _utc(occurred_at),
        "authority": authority,
        "producer": key.key_id,
        "payload": payload or {},
    }
    body["event_hash"] = content_hash(body)
    return _authenticate(body, key)


def verify_event_chain(events: list[dict[str, Any]], key_lookup: KeyLookup) -> bool:
    expected_previous: str | None = None
    expected_sequence = 0
    for event in events:
        verify_signed(event, key_lookup)
        if event.get("sequence") != expected_sequence:
            raise ProtocolError("event sequence gap or duplicate")
        if event.get("previous_event_hash") != expected_previous:
            raise ProtocolError("event predecessor mismatch")
        unsigned = {k: v for k, v in event.items() if k not in {"signature", "event_hash"}}
        if content_hash(unsigned) != event.get("event_hash"):
            raise ProtocolError("event hash mismatch")
        expected_previous = event["event_hash"]
        expected_sequence += 1
    return True


def create_evidence(
    *,
    key: KeyPair,
    transaction_id: str,
    source: str,
    evidence_type: str,
    observed_at: datetime,
    payload: dict[str, Any],
    authority: str,
) -> dict[str, Any]:
    body = {
        "protocol": PROTOCOL,
        "protocol_version": PROTOCOL_VERSION,
        "type": "evidence",
        "transaction_id": transaction_id,
        "source": source,
        "evidence_type": evidence_type,
        "observed_at": _utc(observed_at),
        "authority": authority,
        "payload": payload,
    }
    body["content_id"] = content_hash(body)
    return _authenticate(body, key)


def detect_replay(
    seen_event_hashes: set[str], events: list[dict[str, Any]]
) -> tuple[set[str], list[str]]:
    duplicates: list[str] = []
    updated = set(seen_event_hashes)
    for event in events:
        event_hash = content_hash(event)
        if event_hash in updated:
            duplicates.append(event_hash)
        else:
            updated.add(event_hash)
    return updated, duplicates


def reconcile_histories(
    local_events: list[dict[str, Any]],
    external_events: list[dict[str, Any]],
    key_lookup: KeyLookup,
) -> dict[str, Any]:
    verify_event_chain(local_events, key_lookup)
    verify_event_chain(external_events, key_lookup)
    local_by_hash = {e["event_hash"]: e for e in local_events}
    external_by_hash = {e["event_hash"]: e for e in external_events}
    common = sorted(set(local_by_hash) & set(external_by_hash))
    local_only = sorted(set(local_by_hash) - set(external_by_hash))
    external_only = sorted(set(external_by_hash) - set(local_by_hash))
    conflicts: list[dict[str, Any]] = []
    if local_events and external_events:
        local_tail = local_events[-1]
        external_tail = external_events[-1]
        if (
            local_tail["sequence"] == external_tail["sequence"]
            and local_tail["event_hash"] != external_tail["event_hash"]
        ):
            conflicts.append(
                {
                    "type": "same_sequence_different_event",
                    "sequence": local_tail["sequence"],
                    "local_hash": local_tail["event_hash"],
                    "external_hash": external_tail["event_hash"],
                }
            )
    status = (
        "matched"
        if not local_only and not external_only and not conflicts
        else "reconciliation_required"
    )
    return {
        "status": status,
        "common_event_hashes": common,
        "local_only_event_hashes": local_only,
        "external_only_event_hashes": external_only,
        "conflicts": conflicts,
    }


def export_bundle(
    *,
    intent: dict[str, Any],
    events: list[dict[str, Any]],
    evidence: list[dict[str, Any]],
    key_lookup: KeyLookup,
) -> dict[str, Any]:
    verify_signed(intent, key_lookup)
    verify_event_chain(events, key_lookup)
    for item in evidence:
        verify_signed(item, key_lookup)
    contents = {"intent": intent, "events": events, "evidence": evidence}
    return {
        "protocol": PROTOCOL,
        "protocol_version": PROTOCOL_VERSION,
        "type": "transaction_bundle",
        "bundle_id": content_hash(contents),
        **contents,
    }


def import_bundle(
    bundle: dict[str, Any], key_lookup: KeyLookup
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    if bundle.get("type") != "transaction_bundle":
        raise ProtocolError("unsupported bundle type")
    intent = bundle.get("intent")
    events = bundle.get("events")
    evidence = bundle.get("evidence")
    if not isinstance(intent, dict) or not isinstance(events, list) or not isinstance(evidence, list):
        raise ProtocolError("malformed transaction bundle")
    contents = {"intent": intent, "events": events, "evidence": evidence}
    if bundle.get("bundle_id") != content_hash(contents):
        raise ProtocolError("bundle content identifier mismatch")
    verify_signed(intent, key_lookup)
    verify_event_chain(events, key_lookup)
    for item in evidence:
        if not isinstance(item, dict):
            raise ProtocolError("malformed evidence object")
        verify_signed(item, key_lookup)
    return intent, events, evidence
