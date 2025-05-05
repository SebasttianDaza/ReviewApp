from django.urls import path

from . import views

urlpatterns = [
    path("admin/login/", views.LoginView.as_view(), name="login"),
    path("auth-twitter", views.oauth_twitter_login, name="oauth_twitter_login"),
    path("terms-of-service", views.terms_of_service, name="terms_of_service"),
    path("privacy-police", views.privacy_police, name="privacy_police"),
    path("auth-google", views.auth_google, name="auth_google"),
]
