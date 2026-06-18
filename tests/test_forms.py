import pytest
from hypothesis import given, strategies as st, settings, HealthCheck
from accounts.views import RegisterForm

# Instructs pytest to safely allow database transactions across this entire test module
pytestmark = pytest.mark.django_db


def test_register_form_valid_data():
    """Confirms form registers valid combinations correctly."""

    payload = {
        "username": "tester",
        "email": "test@domain.com",
        "password": "secure_pass_123",
        "confirm_password": "secure_pass_123",
    }
    form = RegisterForm(data=payload)
    assert form.is_valid() is True


def test_register_form_mismatched_passwords():
    """Validates explicit user validation error output when passwords diverge."""

    payload = {
        "username": "tester",
        "email": "test@domain.com",
        "password": "PasswordOne",
        "confirm_password": "PasswordTwo",
    }
    form = RegisterForm(data=payload)
    assert form.is_valid() is False
    assert "Passwords do not match." in form.errors["__all__"]


# --- Hypothesis Property Test ---
# We use settings to tell Hypothesis that reusing the database across iterations is intended
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(pwd1=st.text(min_size=1, max_size=40), pwd2=st.text(min_size=1, max_size=40))
def test_register_form_password_matching_invariant(db, pwd1, pwd2):
    """
    Property Test: Evaluates that form validation errors always flag
    divergent text fields, irrespective of unique characters or input sizes.
    """

    payload = {
        "username": "hypo_user",
        "email": "hypo@example.com",
        "password": pwd1,
        "confirm_password": pwd2,
    }
    form = RegisterForm(data=payload)

    # Invariant Rule: If inputs do not completely match, registration must fail validation
    if pwd1 != pwd2:
        assert form.is_valid() is False
        # If both passwords were provided but they don't match, verify the error message
        if pwd1 and pwd2:
            assert "Passwords do not match." in form.non_field_errors()
