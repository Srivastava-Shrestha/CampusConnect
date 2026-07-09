"""
Shared pytest fixtures.

Force the LLM client into mock mode for the entire test suite, regardless of
whether an ANTHROPIC_API_KEY happens to be set in backend/.env. Tests must be
deterministic, offline, and free - they exercise the mock fallback contract,
not the real Anthropic API. The real key is still used by the running dev
server; only tests are pinned to the mock.
"""
import pytest

from app.services import llm_client


@pytest.fixture(autouse=True)
def force_llm_mock_mode(monkeypatch):
    monkeypatch.setattr(llm_client, "_API_KEY", "")
    # Clear the response cache so a value cached by a real call in a prior
    # run cannot leak into a mock-mode assertion.
    llm_client._cache.clear()
    yield
    llm_client._cache.clear()
