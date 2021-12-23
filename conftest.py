"""Global configuration."""
import pytest
import vroom


@pytest.fixture(autouse=True)
def global_setup(doctest_namespace, monkeypatch):
    """Global configuration setup."""
    doctest_namespace["vroom"] = vroom
