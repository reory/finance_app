from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="home"),  # homepage
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("profile/", views.profile_view, name="profile"),
    path("uploads/", include("apps.uploads.urls", namespace="main_uploads")),
]
