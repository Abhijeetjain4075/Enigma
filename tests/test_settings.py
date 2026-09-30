import pytest

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
