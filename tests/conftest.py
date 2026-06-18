import pytest
from django.contrib.auth.models import User
from unittest.mock import MagicMock


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
    return {
        "username": "testdeveloper",
        "email": "dev@example.com",
        "password": "SuperSecurePassword99!",
    }


@pytest.fixture
def create_user(db, base_user_data):
    def make_user(**kwargs):
        data = base_user_data.copy()
        data.update(kwargs)
        return User.objects.create_user(
            username=data["username"], email=data["email"], password=data["password"]
        )

    return make_user


@pytest.fixture
def standard_user(create_user):
    return create_user()


@pytest.fixture
def auth_client(client, standard_user):
    """A client pre-authenticated for view checking."""

    client.force_login(standard_user)
    return client
