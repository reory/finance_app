from unittest.mock import MagicMock

import pytest
from django.contrib.auth.models import User


@pytest.fixture(autouse=True)
def mock_loggers(monkeypatch):
    """
    Globally patches and mocks system logging tasks to
    isolate execution path testing.
    """

    mock_pipeline = MagicMock()
    mock_security = MagicMock()
    monkeypatch.setattr("accounts.views.log_pipeline_step", mock_pipeline)
    monkeypatch.setattr("accounts.views.log_suspicious_activity", mock_security)
    return mock_pipeline, mock_security


@pytest.fixture
def base_user_data():
    """
    Returns a dictionary containing a set of 
    user fields used throughout the application.
    """

    return {
        "username": "testdeveloper",
        "email": "dev@example.com",
        "password": "SuperSecurePassword99!",
    }


@pytest.fixture
def create_user(db, base_user_data):
    """Create a new user and save it to the database."""

    def make_user(**kwargs):
        """Create a user with sensible defaults for tests."""

        data = base_user_data.copy()
        data.update(kwargs)
        return User.objects.create_user(
            username=data["username"], email=data["email"], password=data["password"]
        )

    return make_user


@pytest.fixture
def standard_user(create_user):
    """Return a default test user instance."""

    return create_user()


@pytest.fixture
def auth_client(client, standard_user):
    """A client pre-authenticated for view checking."""

    client.force_login(standard_user)
    return client
