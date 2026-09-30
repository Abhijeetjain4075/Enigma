#!/usr/bin/env python3
"""Bounded local API smoke-load probe; never run against live providers."""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import statistics
import time
import uuid
from urllib.parse import urlsplit

import httpx


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--requests", type=int, default=40)
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()
    if not 1 <= args.requests <= 100 or not 1 <= args.workers <= 16:
        parser.error("requests must be 1-100 and workers must be 1-16")
    parsed_url = urlsplit(args.base_url)
    if (
        parsed_url.scheme != "http"
        or parsed_url.hostname not in {"localhost", "127.0.0.1", "::1"}
        or parsed_url.username
        or parsed_url.password
        or parsed_url.query
        or parsed_url.fragment
    ):
        parser.error("the smoke probe is intentionally restricted to a local HTTP loopback URL")
    api_key = os.environ.get("ENIGMA_LOAD_API_KEY")
    if not api_key:
        parser.error("set ENIGMA_LOAD_API_KEY to a disposable test tenant API key")

    def one_request(client: httpx.Client, index: int) -> tuple[float, int]:
        payload = {
            "provider_id": "simulator-a",
            "scenario": "normal",
            "expected_amount_minor": 100 + index,
            "currency": "USD",
        }
        started = time.perf_counter()
        try:
            response = client.post(
                "/v1/transactions",
                json=payload,
                headers={"X-API-Key": api_key, "Idempotency-Key": f"load-{uuid.uuid4()}"},
            )
            return (time.perf_counter() - started) * 1000, response.status_code
        except httpx.HTTPError:
            return (time.perf_counter() - started) * 1000, 0

    started = time.perf_counter()
    with httpx.Client(base_url=args.base_url.rstrip("/"), timeout=10, trust_env=False) as client:
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
            results = list(
                executor.map(lambda index: one_request(client, index), range(args.requests))
            )
    elapsed = time.perf_counter() - started
    latencies = sorted(milliseconds for milliseconds, _ in results)
    status_counts = {
        str(code): sum(status == code for _, status in results)
        for code in sorted({status for _, status in results})
    }

    def percentile(value: float) -> float:
        index = min(len(latencies) - 1, int((len(latencies) - 1) * value))
        return latencies[index]

    print(
        json.dumps(
            {
                "scope": "local simulator-only smoke test; not a capacity certification",
                "requests": args.requests,
                "workers": args.workers,
                "elapsed_seconds": round(elapsed, 3),
                "requests_per_second": round(args.requests / elapsed, 2),
                "latency_ms_p50": round(statistics.median(latencies), 2),
                "latency_ms_p95": round(percentile(0.95), 2),
                "status_counts": status_counts,
            },
            indent=2,
        )
    )
    return 0 if all(status == 201 for _, status in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
