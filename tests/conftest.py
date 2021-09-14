import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope='module')
def test_client():
    """
    Client fixture.

    Yields
    ------
    test client
    """
    client = TestClient(app)
    yield client
