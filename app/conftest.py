"""
Module to configure the tests for Mutant Detection API.
This file contains the fixtures and configurations needed to run the tests.
"""

import atexit
import os
import subprocess

import pytest
from adapters.api.dependencies import get_db
from config import settings
from fast_api.fast_api_app import create_app
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database

app: FastAPI = create_app()
# Define a database URL for tests
TEST_DB_NAME: str = "test_db_" + os.urandom(8).hex()
TEST_DATABASE_URL: str = (
    f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{TEST_DB_NAME}"
)

# Build a sessionmaker factory for the test database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=None)

# Define the Base model
Base = declarative_base()


def cleanup_database():
    """
    Drops the test database if it exists.

    This function is registered to be called upon program exit to ensure
    that the test database is removed after the tests have completed.
    """
    if database_exists(TEST_DATABASE_URL):
        drop_database(TEST_DATABASE_URL)
        print(f"Test database {TEST_DB_NAME} dropped.")


atexit.register(cleanup_database)


def execute_alembic_migrations() -> None:
    """
    Executes the Alembic migrations.
    """
    print("Executing Alembic migrations...")
    # Change the current working directory to the project root
    project_root: str = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)

    # Put the test database URL in the environment variables
    os.environ["DATABASE_URL"] = TEST_DATABASE_URL

    command: list[str] = ["alembic", "-c", "alembic.ini", "upgrade", "heads"]
    try:
        # Execute the Alembic migrations
        output: str = subprocess.check_output(
            command, stderr=subprocess.STDOUT, text=True
        )
        print("Alembic migrations executed successfully.")
        print(output)
    except subprocess.CalledProcessError as e:
        print("Error executing Alembic migrations.")
        print(e.output)


@pytest.fixture(scope="session", autouse=True)
def db_engine():
    """
    Creates a new database engine for tests.
    The database engine is created only once before the tests are run.
    The scope of this fixture is at the session level.
    This means that the database engine is created only once for all the tests.

    Returns:
        Engine: The database engine.
    """
    # Create the test database
    if not database_exists(TEST_DATABASE_URL):
        create_database(TEST_DATABASE_URL)

    # Create a new database engine for tests
    engine = create_engine(TEST_DATABASE_URL)

    # Configure the SessionLocal to use the engine
    SessionLocal.configure(bind=engine)

    # Execute Alembic migrations
    execute_alembic_migrations()

    yield engine

    # Clean up after tests
    Base.metadata.drop_all(bind=engine)
    engine.dispose()
    drop_database(TEST_DATABASE_URL)


@pytest.fixture(scope="function")
def db_session(db_engine: Engine):
    """
    Creates a new database session for a test.
    This fixture is executed before each test function is run.

    Args:
        db_engine (Engine): The database engine.

    Returns:
        Session: The database session.
    """
    connection = db_engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function", autouse=True)
def setup_override_get_db(db_session: Session):
    """
    Overrides the `get_db` FastAPI dependency to use the test database session.

    Replaces the application's `get_db` dependency with a version that yields
    the session provided by the `db_session` fixture.
    """

    app.dependency_overrides[get_db] = override_get_db(db_session=db_session)


def override_get_db(db_session: Session):
    """
    Overrides the get_db function to provide a custom database session.

    Args:
        db_session (Session): The database session to be used.

    Returns:
        Generator[Session]: A generator that yields the database
    """

    def _override_get_db():
        """
        Overrides the get_db function to return the db_session.

        Yields:
            db_session: The database session.
        """
        yield db_session

    return _override_get_db


@pytest.fixture(scope="module")
def client():
    """
    Creates a test client for the FastAPI application.

    This fixture provides a `TestClient` instance for simulating HTTP requests
    to the API endpoints during testing.
    """
    return TestClient(app)
