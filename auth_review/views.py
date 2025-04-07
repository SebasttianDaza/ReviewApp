import sys

import requests, logging
from django.contrib.auth import authenticate, login

from django.contrib.auth.views import LoginView as DjangoLoginView
from django.core.signing import BadSignature
from django.http import HttpRequest, HttpResponse, QueryDict
from django.shortcuts import redirect

from ReviewApp.settings import env
from auth_review.decorators import oauth_twitter_token, oauth_twitter_access_token
from auth_review.forms import AuthenticationForm
from django.utils.decorators import method_decorator
from auth_review.http.request import get_signature_twitter
from .models import AuthUser

logger = logging.getLogger("review_app.middleware")

class LoginView(DjangoLoginView):
    form_class = AuthenticationForm
    template_name = "admin/login.html"

    @method_decorator(oauth_twitter_token)
    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""

        try:
            auth_token_twitter = self.request.get_signed_cookie(
                key="OAUTH_TOKEN_TWITTER",
                salt=env("API_KEY_TWITTER")
            )
            token, *rest = auth_token_twitter.split("&")
            kwargs["sign_in_twitter"] = f"{env('API_TWITTER')}/oauth/authenticate?{token}"
        except KeyError or BadSignature:
            kwargs["sign_in_twitter"] = None
            logger.info("Sign in failed twitter")
            pass

        return self.render_to_response(
            self.get_context_data(**kwargs),
        )

@oauth_twitter_access_token
def oauth_twitter_login(request: HttpRequest, *args):
    params = args[0] if args else {}
    url = f"{env('API_TWITTER_1_0')}/account/verify_credentials.json?include_email=true"
    auth = [
        f'oauth_consumer_key={env("API_KEY_TWITTER")}',
        'oauth_nonce=ea9ec8429b68d6b77cd5600adbbb0456',
        'oauth_signature_method=HMAC-SHA1',
        f'oauth_timestamp={params.get("time_signature")}',
        f'oauth_token={params.get("oauth_token")}',
        'oauth_version=1.0'
    ]
    auth.insert(
        3,
        f'oauth_signature="{get_signature_twitter(url, auth, "GET", params.get("oauth_token_secret"))}"'
    )

    user_data = requests.get(
        url,
        headers={
            "Authorization": "{0} {1}".format("OAuth", ", ".join(auth)),
            "Content-Type": "application/json"
        }
    )

    if user_data.status_code == 200:
        user_data = QueryDict(user_data.text)
        username = user_data.get(key="screen_name")
        first_name, last_name, *rest = user_data.get(key="name").split(" ")
        user = AuthUser.objects.get(username=username)
        if user is None:
            AuthUser.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=user_data.get(key="email"),
                password="admin"
            )

        user = authenticate(username=username, password="admin")
        return login(request, user)

    logger.warn(
        f"Exception raised while requesting twitter verify credentials {user_data.text}"
    )
    return redirect("/admin/login")


def terms_of_service():
    return HttpResponse()

def privacy_police():
    return HttpResponse()