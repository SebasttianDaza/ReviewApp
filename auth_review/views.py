import sys

import requests, logging
from django.contrib.auth import authenticate, login

from django.contrib.auth.views import LoginView as DjangoLoginView, redirect_to_login
from django.core.signing import BadSignature
from django.http import HttpRequest, HttpResponse, QueryDict, JsonResponse
from django.shortcuts import redirect

from ReviewApp.settings import env
from auth_review.decorators import oauth_twitter_token
from auth_review.forms import AuthenticationForm
from django.utils.decorators import method_decorator
from auth_review.http.request import get_oauth1_twitter
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

def oauth_twitter_login(request: HttpRequest):
    params = request.GET

    if params.get(key="oauth_token") and params.get(key="oauth_verifier"):
        import time
        from auth_review.http.request import get_signature_twitter
        time_signature = round(time.time())

        oauth_verifier = params.get(key="oauth_verifier")
        oauth_token = params.get(key="oauth_token")
        auth = [
            f'oauth_consumer_key={env("API_KEY_TWITTER")}',
            'oauth_nonce=ea9ec8429b68d6b77cd5600adbbb0456',
            'oauth_signature_method=HMAC-SHA1',
            f'oauth_timestamp={time_signature}',
            f'oauth_token={oauth_token}',
            'oauth_version=1.0'
        ]
        url = f"{env('API_TWITTER')}/oauth/access_token"
        auth.insert(3, f'oauth_signature="{get_signature_twitter(url, auth)}"')
        headers = {
            "Authorization": "{0} {1}".format("OAuth", ", ".join(auth)),
            "Content-Type": "application/x-www-form-urlencoded"
        }

        res = requests.post(f"{url}?oauth_verifier={oauth_verifier}", headers=headers)

        if res.status_code == 200:
            params = QueryDict(res.text)
            oauth_token = params.get(key="oauth_token")
            oauth_token_secret = params.get(key="oauth_token_secret")
            user_id = params.get(key="user_id")

            url_user_data = f"{env('API_TWITTER_1_0')}/account/verify_credentials.json"
            user_data = requests.get(
                url_user_data,
                headers=get_oauth1_twitter(
                    env("API_KEY_TWITTER"),
                    time_signature,
                    oauth_token,
                    url_user_data,
                    "GET"
                ),
                params={
                    "include_email": 'true'
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
                        password=oauth_token_secret
                    )

                user = authenticate(username=username, password=oauth_token_secret)
                return login(request, user)
            else:
                logger.warn(
                    f"Exception raised while requesting twitter authorization {user_data.text}"
                )

        logger.warn(
            f"Exception raised while requesting twitter authorization {res.text}"
        )
        return redirect("/admin/login")

    return redirect("/admin/login")

