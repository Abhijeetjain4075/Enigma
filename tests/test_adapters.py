from enigma.adapters import provider_registry, scenario_supported


def test_two_simulators_advertise_only_simulated_capabilities() -> None:
    registry = provider_registry()
    assert set(registry) == {"simulator-a", "simulator-b"}
    for provider in registry.values():
        assert provider.health_check()["real_provider_connected"] is False
        assert all(
            cap.evidence_level == "E4-simulated" for cap in provider.get_capabilities("normal")
        )


def test_failure_scenarios_are_explicit_and_provider_scoped() -> None:
    assert scenario_supported("simulator-a", "normal")
    assert not scenario_supported("simulator-a", "cdr_mismatch")
    assert scenario_supported("simulator-b", "cdr_mismatch")
    assert not scenario_supported("unknown", "normal")


def test_provider_b_marks_stale_availability_as_stale() -> None:
    availability = next(
        cap
        for cap in provider_registry()["simulator-b"].get_capabilities("stale_availability")
        if cap.operation == "availability"
    )
    assert availability.state == "stale"
    assert availability.expires_at < availability.observed_at
