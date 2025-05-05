from django.urls import path

from . import views

urlpatterns = [
    path("admin/login/", views.LoginView.as_view(), name="login"),
    path("auth-twitter", views.oauth_twitter_login, name="oauth_twitter_login"),
    path("auth-google", views.oauth_google_login, name="oauth_google_login"),
]
