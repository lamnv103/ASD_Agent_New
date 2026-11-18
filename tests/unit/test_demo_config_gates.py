"""The T2.6 authorization gates: defaults must be safe, and enabling one must fail loudly, not silently."""

import importlib

import pytest

import app.config as config_module


def reload_with_env(monkeypatch, **env):
    for key in ("ASD_DEMO_MODE", "ASD_ENABLE_LIVE_QUERY_EMBEDDING", "ASD_ENABLE_LIVE_RERANKING",
                "ASD_ENABLE_LIVE_LLM"):
        monkeypatch.delenv(key, raising=False)
    for key, value in env.items():
        monkeypatch.setenv(key, value)
    return importlib.reload(config_module)


def test_defaults_are_demo_on_and_every_live_provider_off(monkeypatch):
    mod = reload_with_env(monkeypatch)
    assert mod.DEMO_MODE is True
    assert mod.ENABLE_LIVE_QUERY_EMBEDDING is False
    assert mod.ENABLE_LIVE_RERANKING is False
    assert mod.ENABLE_LIVE_LLM is False


@pytest.mark.parametrize("flag", [
    "ASD_ENABLE_LIVE_QUERY_EMBEDDING", "ASD_ENABLE_LIVE_RERANKING", "ASD_ENABLE_LIVE_LLM",
])
def test_enabling_a_live_provider_flag_fails_loudly_instead_of_silently_enabling(monkeypatch, flag):
    # Caught as RuntimeError, not config_module.ConfigError: importlib.reload re-executes the class
    # statement, so a class reference captured before reload would be a stale, distinct class object.
    with pytest.raises(RuntimeError, match=r"APPROVAL_REQUIRED|not been approved"):
        reload_with_env(monkeypatch, **{flag: "true"})


def test_demo_mode_can_be_turned_off_without_affecting_the_disabled_providers(monkeypatch):
    mod = reload_with_env(monkeypatch, ASD_DEMO_MODE="false")
    assert mod.DEMO_MODE is False
    assert mod.ENABLE_LIVE_QUERY_EMBEDDING is False


@pytest.fixture(autouse=True)
def _restore_module():
    yield
    importlib.reload(config_module)
