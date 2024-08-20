from django.urls import path

from . import views

urlpatterns = [
    path("admin/login/", views.LoginView.as_view(), name="login"),
    path("redirect", views.oauth_twitter_login, name="oauth_twitter_login"),
]
