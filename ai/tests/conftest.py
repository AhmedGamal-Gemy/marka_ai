import pytest
from app.config import get_settings, Settings

@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_settings()
