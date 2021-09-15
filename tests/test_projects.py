from dataclasses import dataclass


def test_get_projects(test_client):
    response = test_client.get(
        '/projects/',
    )
    assert response.status_code == 200, 'Response not ok'
    assert len(response.json()) == 2, 'Wrong number of projects returned'
    assert 'PyMove' in [p['name'] for p in response.json()], 'Project not in response'
    assert 'pandas' not in [p['name'] for p in response.json()], 'Wrong project in response'


def test_get_project_name(test_client):
    response = test_client.get(
        '/projects/PyMove/',
    )
    assert response.status_code == 200, 'Response not ok'
    assert response.json() == {
        'name': 'PyMove',
        'packages': [
            {
            'name': 'folium',
            'version': '0.12.1'
            },
            {
            'name': 'pandas',
            'version': '1.2.1'
            }
        ]
    }, 'Wrong project returned'

    response = test_client.get(
        '/projects/pymove/',
    )
    assert response.status_code == 200, 'Response not ok'
    assert response.json().get('name') == 'PyMove' , 'Wrong project returned'

    response = test_client.get(
        '/projects/missing/',
    )
    assert response.status_code == 400, 'Wrong error code'
    assert response.json() == {
        'error': 'Project not found'
    } , 'Wrong error message for non existing project'


def test_create_project(test_client, mocker):
    @dataclass
    class ResponseMock:
        ok: bool
        _json: dict

        def json(self) -> dict:
            return self._json

    def mock_pypi(url):
        if url == 'https://pypi.org/pypi/django-rest-swagger/json':
            return ResponseMock(True, {'info': {'version': '2.2.0'}})
        if url == 'https://pypi.org/pypi/Django/2.2.24/json':
            return ResponseMock(True, {'info': {'version': '2.2.24'}})
        if url == 'https://pypi.org/pypi/psycopg2-binary/2.9.1/json':
            return ResponseMock(True, {'info': {'version': '2.9.1'}})
        if url == 'https://pypi.org/pypi/keras/json':
            return ResponseMock(True, {'info': {'version': '2.6.0'}})
        if url == 'https://pypi.org/pypi/keras/3.0/json':
            return ResponseMock(False, None)
        if url == 'https://pypi.org/pypi/pypypypypypypypypypypypypy/json':
            return ResponseMock(False, None)

    mocker.patch('app.utils.pypi.requests.get', mock_pypi)

    response = test_client.post(
        '/projects/',
        json={
            'name': 'titan',
            'packages': [
                {'name': 'django-rest-swagger'},
                {'name': 'Django', 'version': '2.2.24'},
                {'name': 'psycopg2-binary', 'version': '2.9.1'}
            ]
        }
    )
    assert response.status_code == 201, 'Response not ok'
    resp = response.json()
    assert resp.get('name') == 'titan', 'Wrong project name'
    django_pkg = [*filter(
        lambda x: x['name'] == 'Django', resp.get('packages')
    )][0]
    drs_version_pkg = [*filter(
        lambda x: x['name'] == 'django-rest-swagger', resp.get('packages')
    )][0]
    assert django_pkg['version'] == '2.2.24', 'Wrong package version for provided'
    assert drs_version_pkg['version'] == '2.2.0', 'Wrong package version for missing'

    response = test_client.post(
        '/projects/',
        json={
            'name': 'titan',
            'packages': [
                {'name': 'django-rest-swagger'},
                {'name': 'Django', 'version': '2.2.24'},
                {'name': 'psycopg2-binary', 'version': '2.9.1'}
            ]
        }
    )
    assert response.status_code == 400, 'Wrong error code'
    assert response.json() == {
        'error': 'Project already exists'
    } , 'Wrong error message for duplicate project'

    response = test_client.post(
        '/projects/',
        json={
            'name': 'titan2',
            'packages': [
                {'name': 'Django', 'version': '2.2.24'},
                {'name': 'psycopg2-binary', 'version': '2.9.1'},
                {'name': 'django', 'version': '2.2.23'}
            ]
        }
    )
    assert response.status_code == 400, 'Wrong error code'
    assert response.json() == {
        'error': 'One or more packages are duplicated'
    } , 'Wrong error message for project with duplicate packages'

    response = test_client.post(
        '/projects/',
        json={
            'name': 'machine-head',
            'packages': [
                {'name': 'keras'},
                {'name': 'pypypypypypypypypypypypypy'}
            ]
        }
    )
    assert response.status_code == 400, 'Wrong error code'
    assert response.json() == {
        'error': "One or more packages doesn't exist"
    } , 'Wrong error message for non existing package'

    response = test_client.post(
        '/projects/',
        json={
            'name': 'machine-head',
            'packages': [
                {'name': 'keras', 'version': '3.0'}
            ]
        }
    )
    assert response.status_code == 400, 'Wrong error code'
    assert response.json() == {
        'error': "One or more packages doesn't exist"
    } , 'Wrong error message for package with wrong version'


def test_delete_project(test_client):
    response = test_client.delete(
        '/projects/PyMove/',
    )
    print(response.url)
    assert response.status_code == 200, 'Response not ok'
    assert response.json() == {'message': 'Project deleted'}, 'Wrong delete message'

    response = test_client.delete(
        '/projects/PyMoved/',
    )
    assert response.status_code == 400, 'Wrong error code'
    assert response.json() == {
        'error': 'Project not found'
    } , 'Wrong error message for non existing project'
