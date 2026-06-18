from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django import forms

from apps.logs.pipeline_logger import log_pipeline_step
from apps.logs.security_logger import log_suspicious_activity


# Forms -----------------------------------------------
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def clean(self):
        # Run the parent class validation first
        cleaned = super().clean()
        # Extract both password fields from the cleaned data.
        p1 = self.data.get("password")
        p2 = self.data.get("confirm_password")
        # Ensure both fields exist and match
        if p1 != p2:
            raise forms.ValidationError("Passwords do not match.")

        # Return the validated from data
        return cleaned


# Views ---------------------------------------------------
def login_view(request):
    """The view the user sees once logged into a session."""

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            # Logs succesful login
            log_pipeline_step(f"User logged in: {username}")
            login(request, user)
            return redirect("analytics:dashboard")
        else:
            # Log failed attempts to login
            log_suspicious_activity(f"Failed login attempt for username={username}")
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")


def logout_view(request):
    """The view the user sees once logged out of a session."""

    log_pipeline_step(f"User logged out: {request.user.username}")
    logout(request)
    return redirect("login")


def register_view(request):
    """Registration view when a user lands on the registration page."""

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            # Log new registered user
            log_pipeline_step(f"New user registered: {user.username}")

            messages.success(request, "Account created successfully.")
            return redirect("login")
        else:
            log_suspicious_activity("Registration form validation failed.")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


def index(request):
    return render(request, "index.html")


@login_required
def profile_view(request):
    """Profile view for the user."""

    log_pipeline_step(f"Profile viewed: {request.user.username}")
    return render(request, "profile.html")
