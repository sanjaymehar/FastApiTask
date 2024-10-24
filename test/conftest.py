import pytest
from app.main import app as main


@pytest.fixture
def app():
    yield main
