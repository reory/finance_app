import pytest
from django.urls import reverse

# Instructs pytest to safely allow database transactions across this entire test module
pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestAuthenticationViews:
    def test_homepage_index(self, client):
        """Verifies core root URL loads index cleanly."""

        url = reverse("home")
        response = client.get(url)
        assert response.status_code == 200
        assert "index.html" in [t.name for t in response.templates]

    def test_login_page_renders(self, client):
        """Checks authentication view interface availability."""

        url = reverse("login")
        response = client.get(url)
        assert response.status_code == 200
        assert "login.html" in [t.name for t in response.templates]

    def test_successful_login_redirect(self, client, create_user):
        """
        Verifies correct credentials grant entry and
        switch path to analytics dashboard.
        """

        create_user(username="validuser", password="SafePassword7")

        url = reverse("login")
        response = client.post(
            url, {"username": "validuser", "password": "SafePassword7"}
        )

        assert response.status_code == 302
        assert response.url == reverse("analytics:dashboard")

    def test_failed_login_keeps_user_on_page(self, client, create_user):
        """Invalid details trigger an error prompt instead of a session swap."""

        create_user(username="validuser", password="SafePassword7")

        url = reverse("login")
        response = client.post(
            url, {"username": "validuser", "password": "IncorrectPassword"}
        )

        assert response.status_code == 200
        messages = list(response.context["messages"])
        assert len(messages) == 1
        assert str(messages[0]) == "Invalid username or password."

    def test_unauthenticated_user_profile_redirect(self, client):
        """Verifies security decorator prevents access to user profiles without login."""

        url = reverse("profile")
        response = client.get(url)
        assert response.status_code == 302

    def test_authenticated_user_profile_access(self, auth_client):
        """Confirms authorized accounts can fetch profile templates successfully."""

        url = reverse("profile")
        response = auth_client.get(url)
        assert response.status_code == 200
        assert "profile.html" in [t.name for t in response.templates]
