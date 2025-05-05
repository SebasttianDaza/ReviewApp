import requests, logging
from django.contrib.auth import authenticate, login

from django.contrib.auth.views import LoginView as DjangoLoginView
from django.core.signing import BadSignature
from django.http import HttpRequest, QueryDict, HttpResponseBadRequest
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods

from ReviewApp.settings import env
from auth_review.decorators import oauth_twitter_token, oauth_twitter_access_token
from auth_review.forms import AuthenticationForm
from django.utils.decorators import method_decorator
from auth_review.http.request import get_signature_twitter
from .models import AuthUser
from django.views.decorators.csrf import csrf_exempt

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

        kwargs["api_client_id_google"] = env("API_KEY_CLIENT_GOOGLE")
        return self.render_to_response(
            self.get_context_data(**kwargs),
        )

@oauth_twitter_access_token
def oauth_twitter_login(request: HttpRequest, *args):
    try:
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
        else:
            raise requests.exceptions.RequestException(user_data.text)
    except (
            requests.exceptions.RequestException or
            requests.exceptions.ConnectionError or
            requests.exceptions.Timeout or
            requests.exceptions.TooManyRedirects
    ) as e:
        logger.warn(
            f"Exception raised while requesting twitter verify credentials {e}"
        )
        pass

    return redirect("/admin/login")



@csrf_exempt
@require_http_methods(["HEAD", "POST"])
def oauth_google_login(request: HttpRequest, *args):
    payload = request.POST
    if not payload:
        return  HttpResponseBadRequest()

    csrf_token_cookie = request.COOKIES.get("g_csrf_token")
    csrf_token_body = payload.get("g_csrf_token")
    if not csrf_token_cookie or not csrf_token_body or csrf_token_cookie != csrf_token_body:
        logger.warn(
            f"Exception raised while requesting google verify csrf token"
        )
        return HttpResponseBadRequest()

    try:
        from google.oauth2 import id_token
        from google.auth.transport import requests

        id_info = id_token.verify_oauth2_token(
            payload.get("credential"),
            requests.Request(),
            payload.get("clientId")
        )
        userid = id_info['sub']
        username = id_info['name'].lower().replace(" ", "_")

        if not AuthUser.objects.filter(username=username).exists():
            AuthUser.objects.create_user(
                username=username,
                first_name=id_info['given_name'],
                last_name=id_info['family_name'],
                email=id_info['email'],
                password=userid,
                is_staff=True,
            )

        user = authenticate(username=username, password=userid)
        if user is not None:
            login(request, user)
            return redirect("/admin/")

        return redirect("/admin/login")
    except ValueError:
        logger.warn(
            f"Exception raised while requesting google verify google id token"
        )
        return HttpResponseBadRequest()

