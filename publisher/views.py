from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse


# Create your views.py here.

def index(request: WSGIRequest) -> HttpResponse:
    return HttpResponse("Hello, world. You're at the Review Index page.")

def terms_of_service():
    return HttpResponse()

def privacy_police():
    return HttpResponse()