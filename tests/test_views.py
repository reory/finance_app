from datetime import date
from decimal import Decimal

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from apps.analytics.models import Transaction

# Instructs pytest to safely allow database transactions across this entire test module
pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestAuthenticationViews:
    def test_upload_view_renders(self, client, django_user_model):
        """Authenticated users can access the upload page."""

        django_user_model.objects.create_user(
            username="testuser",
            password="secret123",
        )

        client.login(
            username="testuser",
            password="secret123",
        )

        response = client.get(reverse("uploads:upload"))

        assert response.status_code == 200

    def test_upload_view_requires_file(self, client, django_user_model):
        """Posting without a file returns a validation error."""

        django_user_model.objects.create_user(
            username="testuser",
            password="secret123",
        )

        client.login(
            username="testuser",
            password="secret123",
        )

        response = client.post(reverse("uploads:upload"))

        assert response.status_code == 400

    def test_upload_view_rejects_non_csv(self, client, django_user_model):
        """Test to make sure only CSV files are accepted."""

        django_user_model.objects.create_user(
            username="testuser",
            password="secret123",
        )

        client.login(
            username="testuser",
            password="secret123",
        )

        file = SimpleUploadedFile(
            "notes.txt",
            b"not a csv",
            content_type="text/plain",
        )

        response = client.post(
            reverse("uploads:upload"),
            {"csv_file": file},
        )

        assert response.status_code == 400

    def test_upload_view_imports_transactions(self, client, django_user_model):
        """Valid CSV uploads create transactions records."""

        user = django_user_model.objects.create_user(
            username="testuser",
            password="secret123",
        )

        client.login(
            username="testuser",
            password="secret123",
        )

        csv_content = (
            b"Date,Description,Category,Amount\n" 
            b"2026-01-15,Coffee,Food,-4.50\n"
        )

        file = SimpleUploadedFile(
            "transactions.csv",
            csv_content,
            content_type="text/csv",
        )

        response = client.post(
            reverse("uploads:upload"),
            {"csv_file": file},
        )

        assert response.status_code == 302

        transaction = Transaction.objects.get()

        assert transaction.user == user
        assert transaction.description == "Coffee"
        assert transaction.category == "Food"
        assert transaction.amount == Decimal("-4.50")
        assert transaction.type == "Debit"


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



    def test_dashboard_view_shows_transaction_count(self, client, django_user_model):
        """Dashboard displays the count of transactions belonging to the user."""

        user = django_user_model.objects.create_user(
            username="testuser",
            password="secret123",
        )

        client.login(username="testuser", password="secret123")

        Transaction.objects.create(
        user=user,
        date=date(2024, 1, 15),
        description="Coffee",
        category="Food",
        amount=Decimal("4.50"),
        type="Debit",
        )

        Transaction.objects.create(
        user=user,
        date=date(2024, 1, 16),
        description="Lunch",
        category="Food",
        amount=Decimal("8.50"),
        type="Debit",
    )

        response = client.get(reverse("analytics:dashboard"))

        assert response.status_code == 200
        assert response.context["transaction_count"] == 2



    def test_status_view_renders(self, client, django_user_model):
        """Status page loads successfully for authenticated users."""

        django_user_model.objects.create_user(
            username="testuser",
            password="secret123",
        )

        client.login(
            username="testuser", 
            password="secret123"
        )
        
        response = client.get(reverse("analytics:status"))

        assert response.status_code == 200



    def test_transactions_view_returns_user_transactions(
        self,
        client,
        django_user_model,
    ):
        """Transactions view only returns transactions belonging to the user."""

        user = django_user_model.objects.create_user(
            username="testuser",
            password="secret123",
        )

        client.login(username="testuser", password="secret123")

        tx = Transaction.objects.create(
            user=user,
            date=date(2024, 1, 15),
            description="Coffee",
            category="Food",
            amount=Decimal("4.50"),
            type="Debit",
        )

        response = client.get(reverse("analytics:transactions"))

        assert response.status_code == 200
        assert tx in response.context["transactions"]



    def test_clear_transactions_deletes_user_transactions(
        self,
        client,
        django_user_model,
    ):
        """Posting to clear transactions removes all user transactions."""

        user = django_user_model.objects.create_user(
            username="testuser",
            password="secret123",
        )

        client.login(username="testuser", password="secret123")

        Transaction.objects.create(
        user=user,
        date=date(2024, 1, 15),
        description="Coffee",
        category="Food",
        amount=Decimal("4.50"),
        type="Debit",
        )

        Transaction.objects.create(
            user=user,
            date=date(2024, 1, 16),
            description="Lunch",
            category="Food",
            amount=Decimal("8.50"),
            type="Debit",
        )

        assert Transaction.objects.count() == 2

        response = client.post(reverse("analytics:clear_transactions"))

        assert response.status_code == 302
        assert Transaction.objects.count() == 0
