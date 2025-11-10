from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse


# Create your views.py here.

def index(request: WSGIRequest) -> HttpResponse:
    return JsonResponse({
        "is_secure()": request.is_secure(),
        "scheme": request.scheme,
        "HTTP_X_FORWARDED_PROTO": request.META.get("HTTP_X_FORWARDED_PROTO"),
        "HTTP_X_FORWARDED_SSL": request.META.get("HTTP_X_FORWARDED_SSL"),
        "HTTP_X_FORWARDED_HOST": request.META.get("HTTP_X_FORWARDED_HOST"),
        "Host": request.META.get("HTTP_HOST"),
    })

def terms_of_service():
    return HttpResponse()

def privacy_police():
    return HttpResponse()