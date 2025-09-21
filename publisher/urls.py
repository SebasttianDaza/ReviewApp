from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path("terms-of-service", views.terms_of_service, name="terms_of_service"),
    path("privacy-police", views.privacy_police, name="privacy_police"),
]
