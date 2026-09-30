"""Environment configuration. Secrets are supplied out-of-band, never committed."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field


class ConfigurationError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class Settings:
    environment: str = "development"
    database_url: str = "sqlite:///./enigma-dev.db"
    api_keys: dict[str, str] = field(default_factory=dict)
    max_request_bytes: int = 1_048_576

    @classmethod
    def from_env(cls) -> Settings:
        environment = os.getenv("ENIGMA_ENV", "development").lower()
        database_url = os.getenv("DATABASE_URL", "sqlite:///./enigma-dev.db")
        serialized = os.getenv("ENIGMA_API_KEYS", "")
        api_keys: dict[str, str]
        if serialized:
            try:
                parsed = json.loads(serialized)
            except json.JSONDecodeError as exc:
                raise ConfigurationError("ENIGMA_API_KEYS must be a JSON object") from exc
            if not isinstance(parsed, dict) or not all(
                isinstance(key, str) and isinstance(tenant, str) and tenant.strip()
                for key, tenant in parsed.items()
            ):
                raise ConfigurationError(
                    "ENIGMA_API_KEYS must map non-empty API keys to tenant IDs"
                )
            api_keys = parsed
        elif environment == "development":
            # Intentionally local-only convenience; production refuses this fallback.
            api_keys = {os.getenv("ENIGMA_DEV_API_KEY", "local-dev-key-change-me"): "tenant-demo"}
        else:
            raise ConfigurationError("ENIGMA_API_KEYS is required outside development")
        settings = cls(
            environment=environment,
            database_url=database_url,
            api_keys=api_keys,
            max_request_bytes=int(os.getenv("ENIGMA_MAX_REQUEST_BYTES", "1048576")),
        )
        settings.validate()
        return settings

    def validate(self) -> None:
        if self.environment not in {"development", "test", "staging", "production"}:
            raise ConfigurationError("ENIGMA_ENV must be development, test, staging, or production")
        if self.max_request_bytes < 1024 or self.max_request_bytes > 10_485_760:
            raise ConfigurationError("ENIGMA_MAX_REQUEST_BYTES must be between 1 KiB and 10 MiB")
        if not self.api_keys:
            raise ConfigurationError("At least one tenant-scoped API key must be configured")
        if self.environment in {"staging", "production"}:
            if self.database_url.startswith("sqlite"):
                raise ConfigurationError(
                    "Staging/production requires PostgreSQL; SQLite is local/test only"
                )
            if any(len(key) < 32 for key in self.api_keys):
                raise ConfigurationError(
                    "Staging/production API keys must contain at least 32 characters"
                )
            if "local-dev-key-change-me" in self.api_keys:
                raise ConfigurationError(
                    "The development API key cannot be used outside development"
                )
