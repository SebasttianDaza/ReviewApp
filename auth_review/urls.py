from django.urls import path

from . import views

urlpatterns = [
    path("admin/login/", views.LoginView.as_view(), name="login"),
]
