import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_connection_uri():
    """Gets a connection URI for postgres from environment variables.
    """
    user = os.environ["POSTGRES_USER"]
    password = os.environ["POSTGRES_PASSWORD"]
    host = os.environ["POSTGRES_HOST"]
    port = os.environ["POSTGRES_PORT"]
    dbname = os.environ["POSTGRES_DB"]

    return f"postgres+pg8000://{user}:{password}@{host}:{port}/{dbname}"


def get_engine():
    return create_engine(get_connection_uri(), echo=False)


Session = sessionmaker(bind=get_engine())


@contextmanager
def get_session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
