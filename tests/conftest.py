import pytest
from sharedmodels.db import Session, get_engine
from tests.factories import set_session
from api.app import app as _app
from sharedmodels.models import Base


@pytest.fixture
def db_session(db):
    """Creates SQLAlchemy session for use in a test.
    Session will be rolled back at the end to undo changes.
    """
    session = Session()
    set_session(session)
    yield session
    session.rollback()
    session.close()


@pytest.fixture
def app():
    _app.config["TESTING"] = True
    _app.config["SERVER_NAME"] = "localhost"
    with _app.app_context():
        yield _app


@pytest.fixture(scope="session")
def db(engine):
    """Creates all database tables and drops them after
    tests have finished"""
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="session")
def engine():
    eng = get_engine()
    # Sanity check to avoid dropping real database
    assert eng.url.database == "test_iss"
    return eng


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client