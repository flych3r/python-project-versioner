from fastapi.testclient import TestClient


def test_get_root(test_client: TestClient):
    """Test '/' endpoint get response."""
    response = test_client.get('/')
    assert response.status_code == 200, 'Get not successfull'
    assert response.json() == {'status': 'ok'}, 'Json response unexpected'
