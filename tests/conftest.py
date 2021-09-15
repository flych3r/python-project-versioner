from collections import namedtuple

import pytest
from fastapi.testclient import TestClient

from app import models
from app.dependencies.database import Base, SessionLocal, engine
from app.main import app
from app.utils.pypi import normalize

Proj = namedtuple('Proj', ['name', 'packages'])
Pkg = namedtuple('Pkg', ['name', 'version'])

projects = [
    models.Project(
        name=proj.name,
        normalized_name=normalize(proj.name),
        packages_releases=[
            models.PackageRelease(name=pkg.name, version=pkg.version)
            for pkg in proj.packages
        ]
    ) for proj in [
        Proj('PyMove', [Pkg('folium', '0.12.1'), Pkg('pandas', '1.2.1')]),
        Proj('magpy', [Pkg('fastapi', '0.68.1'), Pkg('uvicorn', '0.15.0')])
    ]
]


def setup():
    """Setup db for tests."""
    Base.metadata.create_all(engine)
    with SessionLocal() as session:
        for p in projects:
            session.add(p)
            session.commit()


def teardown():
    """Teardown db from tests."""
    Base.metadata.drop_all(engine)


@pytest.fixture(scope='session', autouse=True)
def tests_setup_and_teardown():
    """
    Fixture to be executed before and after tests.

    Creates and populates sqlite db.
    """
    setup()
    yield
    teardown()


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
