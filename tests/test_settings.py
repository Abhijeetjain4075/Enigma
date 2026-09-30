import json

import pytest

from enigma.api import create_app
from enigma.settings import ConfigurationError, Settings


def test_production_rejects_sqlite_and_weak_api_keys() -> None:
    with pytest.raises(ConfigurationError, match="requires PostgreSQL"):
        Settings(
            environment="production",
            database_url="sqlite:///prod.db",
            api_keys={"x" * 40: "tenant"},
        ).validate()
    with pytest.raises(ConfigurationError, match="32 characters"):
        Settings(
            environment="production",
            database_url="postgresql+psycopg://db",
            api_keys={"short": "tenant"},
        ).validate()


def test_api_rejects_invalid_environment_configuration() -> None:
    with pytest.raises(ConfigurationError, match="At least one tenant-scoped API key"):
        Settings(environment="test", database_url="sqlite:///test.db", api_keys={}).validate()


@pytest.mark.parametrize("environment", ["staging", "production"])
def test_app_refuses_simulator_only_environment(environment: str) -> None:
    settings = Settings(
        environment=environment,
        database_url="postgresql+psycopg://enigma:secret@localhost:5432/enigma",
        api_keys={"k" * 40: "tenant-live"},
    )

    with pytest.raises(ConfigurationError, match="simulator-only providers"):
        create_app(settings)


def test_unspecified_environment_defaults_to_production(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in (
        "ENIGMA_ENV",
        "DATABASE_URL",
        "ENIGMA_API_KEYS",
    ):
        monkeypatch.delenv(name, raising=False)

    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://enigma:secret@localhost:5432/enigma")
    monkeypatch.setenv("ENIGMA_API_KEYS", json.dumps({"k" * 40: "tenant-production"}))
    assert Settings.from_env().environment == "production"

    monkeypatch.delenv("ENIGMA_API_KEYS")
    with pytest.raises(ConfigurationError, match="ENIGMA_API_KEYS is required"):
        Settings.from_env()

    monkeypatch.setenv("ENIGMA_ENV", "development")
    with pytest.raises(ConfigurationError, match="ENIGMA_API_KEYS is required"):
        Settings.from_env()
