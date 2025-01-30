import requests

from django.contrib.auth.views import LoginView as DjangoLoginView
from django.core.signing import BadSignature
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse, QueryDict

from ReviewApp.settings import env
from auth_review.forms import AuthenticationForm


class LoginView(DjangoLoginView):
    form_class = AuthenticationForm
    template_name = "admin/login.html"

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
            

            return HttpResponse(res.text)

        return HttpResponseRedirect("")

    return HttpResponseRedirect("")
