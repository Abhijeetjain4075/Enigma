"""Backendless Enigma protocol primitives.

This module is deliberately independent of the SQL/FastAPI transaction lab.
It models the minimum protocol state that participants can carry and verify
without an Enigma-operated database.

Security boundary:
- Ed25519 signatures authenticate an issuer key; they do not establish that
  the issuer is authorized to operate a provider.
- The provider remains authoritative for physical-world service state.
- A local Enigma state is never promoted to provider-authoritative state merely
  because it is signed.
- This module performs no network I/O and never moves money or controls
  physical equipment.
"""

from __future__ import annotations

import base64
import hashlib
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)

PROTOCOL = "enigma-protocol"
PROTOCOL_VERSION = "0.1"
ALGORITHM = "Ed25519"


class ProtocolError(ValueError):
    """Raised when a protocol object is malformed or unverifiable."""


def _canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def content_hash(value: Any) -> str:
    """Return a stable SHA-256 content identifier for a JSON value."""
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
    private_key: Ed25519PrivateKey
    public_key: Ed25519PublicKey

    @classmethod
    def generate(cls) -> "KeyPair":
        private = Ed25519PrivateKey.generate()
        return cls(private, private.public_key())

    @property
    def key_id(self) -> str:
        raw = self.public_key.public_bytes_raw()
        return "ed25519:" + hashlib.sha256(raw).hexdigest()[:32]

    @property
    def public_key_b64(self) -> str:
        return _b64(self.public_key.public_bytes_raw())


def _signed_payload(payload: dict[str, Any], key: KeyPair) -> dict[str, Any]:
    unsigned = dict(payload)
    unsigned.pop("signature", None)
    signature = key.private_key.sign(_canonical(unsigned))
    return {
        **unsigned,
        "signature": {
            "algorithm": ALGORITHM,
            "key_id": key.key_id,
            "public_key": key.public_key_b64,
            "value": _b64(signature),
        },
    }


def verify_signed(payload: dict[str, Any]) -> bool:
    signature = payload.get("signature")
    if not isinstance(signature, dict):
        raise ProtocolError("missing signature")
    if signature.get("algorithm") != ALGORITHM:
        raise ProtocolError("unsupported signature algorithm")
    try:
        public = Ed25519PublicKey.from_public_bytes(_unb64(str(signature["public_key"])))
        public.verify(
            _unb64(str(signature["value"])),
            _canonical({k: v for k, v in payload.items() if k != "signature"}),
        )
    except (KeyError, ValueError, TypeError, InvalidSignature) as exc:
        raise ProtocolError("invalid signature") from exc
    expected_key_id = "ed25519:" + hashlib.sha256(
        public.public_bytes_raw()
    ).hexdigest()[:32]
    if expected_key_id != signature.get("key_id"):
        raise ProtocolError("signature key identifier mismatch")
    return True


def deterministic_transaction_id(
    *,
    issuer_key_id: str,
    nonce: str,
    intent_body: dict[str, Any],
) -> str:
    """Derive a stable transaction identifier from issuer + nonce + intent."""
    if not issuer_key_id or not nonce:
        raise ProtocolError("issuer_key_id and nonce are required")
    material = {
        "protocol": PROTOCOL,
        "version": PROTOCOL_VERSION,
        "issuer_key_id": issuer_key_id,
        "nonce": nonce,
        "intent": intent_body,
    }
    return "txn_" + content_hash(material)


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
    """Create a signed, portable intent. No provider is contacted."""
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
    transaction_id = deterministic_transaction_id(
        issuer_key_id=key.key_id,
        nonce=nonce,
        intent_body=body,
    )
    body["transaction_id"] = transaction_id
    return _signed_payload(body, key)


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
    """Create one signed event linked to the previous event hash."""
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
    return _signed_payload(body, key)


def verify_event_chain(events: list[dict[str, Any]]) -> bool:
    """Verify signatures, hashes, sequence and predecessor links."""
    expected_previous: str | None = None
    expected_sequence = 0
    for event in events:
        verify_signed(event)
        if event.get("sequence") != expected_sequence:
            raise ProtocolError("event sequence gap or duplicate")
        if event.get("previous_event_hash") != expected_previous:
            raise ProtocolError("event predecessor mismatch")
        unsigned_without_signature = {
            k: v for k, v in event.items() if k not in {"signature", "event_hash"}
        }
        if content_hash(unsigned_without_signature) != event.get("event_hash"):
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
    """Create a signed evidence object with a content identifier."""
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
    return _signed_payload(body, key)


def detect_replay(
    seen_event_hashes: set[str],
    events: list[dict[str, Any]],
) -> tuple[set[str], list[str]]:
    """Return the updated seen set and hashes that were already observed."""
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
) -> dict[str, Any]:
    """Compare independently held signed histories without a central store."""
    verify_event_chain(local_events)
    verify_event_chain(external_events)
    local_by_hash = {content_hash(e): e for e in local_events}
    external_by_hash = {content_hash(e): e for e in external_events}
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
    status = "matched" if not local_only and not external_only and not conflicts else "reconciliation_required"
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
) -> dict[str, Any]:
    """Create a portable transaction bundle that can be stored anywhere."""
    verify_signed(intent)
    verify_event_chain(events)
    for item in evidence:
        verify_signed(item)
    return {
        "protocol": PROTOCOL,
        "protocol_version": PROTOCOL_VERSION,
        "type": "transaction_bundle",
        "bundle_id": content_hash({"intent": intent, "events": events, "evidence": evidence}),
        "intent": intent,
        "events": events,
        "evidence": evidence,
    }


def import_bundle(bundle: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    """Verify and unpack a portable bundle after process/device recovery."""
    if bundle.get("type") != "transaction_bundle":
        raise ProtocolError("unsupported bundle type")
    intent = bundle.get("intent")
    events = bundle.get("events")
    evidence = bundle.get("evidence")
    if not isinstance(intent, dict) or not isinstance(events, list) or not isinstance(evidence, list):
        raise ProtocolError("malformed transaction bundle")
    expected_id = content_hash({"intent": intent, "events": events, "evidence": evidence})
    if bundle.get("bundle_id") != expected_id:
        raise ProtocolError("bundle content identifier mismatch")
    verify_signed(intent)
    verify_event_chain(events)
    for item in evidence:
        if not isinstance(item, dict):
            raise ProtocolError("malformed evidence object")
        verify_signed(item)
    return intent, events, evidence
