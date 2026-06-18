import pytest
from accounts.models import UserProfile

# Instructs pytest to safely allow database transactions across this entire test module
pytestmark = pytest.mark.django_db


@pytest.mark.django_db
def test_user_profile_creation_and_defaults(standard_user):
    """
    Validates model instantiation constraints,
    default properties, and metadata strings.
    """

    profile = UserProfile.objects.create(
        user=standard_user, organisation="Open Source Analytics"
    )

    assert profile.user == standard_user
    assert profile.organisation == "Open Source Analytics"
    assert profile.timezone == "UTC"  # Confirms model default string assignment
    assert (
        profile.onboarding_complete is False
    )  # Checks onboarding state starts cleanly
    assert (
        str(profile) == "testdeveloper"
    )  # Tests __str__ design for Admin Panel clarity
