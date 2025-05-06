from django.core.signing import BadSignature
from ReviewApp.settings import env
import requests, time, logging
from urllib.parse import quote_plus
from django.http import QueryDict

logger = logging.getLogger("review_app.middleware")

def oauth_twitter_token(view_func):
    def wrapper(request, *args, **kwargs):
        from auth_review.http.request import get_signature_twitter
        from ReviewApp.helpers import site
        response = view_func(request, *args, **kwargs)

        try:
            cookie_token = request.get_signed_cookie(
                key="OAUTH_TOKEN_TWITTER",
                salt=env("API_KEY_TWITTER")
            )
            if cookie_token:
                return response
        except KeyError or BadSignature:
            pass

        try:
            time_signature = round(time.time())
            url = f"{env('API_TWITTER')}/oauth/request_token"
            auth = [
                f'oauth_callback={quote_plus(site(request) + "/auth-twitter")}',
                f'oauth_consumer_key={env("API_KEY_TWITTER")}',
                'oauth_nonce=ea9ec8429b68d6b77cd5600adbbb0456',
                'oauth_signature_method=HMAC-SHA1',
                f'oauth_timestamp={time_signature}',
                f'oauth_token={env("OAUTH_TOKEN_TWITTER")}',
                'oauth_version=1.0'
            ]
            auth.insert(3, f'oauth_signature="{get_signature_twitter(url, auth)}"')
            headers = {
                "Authorization": "{0} {1}".format("OAuth", ", ".join(auth))
            }

            res = requests.post(url, headers=headers)
            if res.status_code == 200:
                token = res.text
                response.set_signed_cookie(
                    key="OAUTH_TOKEN_TWITTER",
                    value=token,
                    max_age=300,
                    httponly=True,
                    salt=env("API_KEY_TWITTER"),
                    samesite="Strict"
                )
            else:
                raise requests.exceptions.RequestException(res.text)
        except (
                requests.exceptions.RequestException or
                requests.exceptions.ConnectionError or
                requests.exceptions.Timeout or
                requests.exceptions.TooManyRedirects
        ) as e:
            logger.warn(
                f'Exception raised while requesting twitter authorization. {e}',
                exc_info=True
            )
            pass

        return response

    return wrapper

def oauth_twitter_access_token(view_func):
    def wrapper(request, *args, **kwargs):
        from django.shortcuts import redirect
        params = request.GET

        if params.get(key="oauth_token") and params.get(key="oauth_verifier"):
            try:
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
                    params_verifier = QueryDict(res.text)
                    args = args + ({
                        "oauth_token": params_verifier.get(key="oauth_token"),
                        "oauth_token_secret": params_verifier.get(key="oauth_token_secret"),
                        "user_id": params.get(key="user_id"),
                        "time_signature": time_signature
                    },)
                    response = view_func(request, *args, **kwargs)
                    return response
                else:
                    raise requests.exceptions.RequestException(res.text)
            except (
                    requests.exceptions.RequestException or
                    requests.exceptions.ConnectionError or
                    requests.exceptions.Timeout or
                    requests.exceptions.TooManyRedirects
            ) as e:
                logger.warn(
                    f"Exception raised while requesting twitter access token {e}"
                )
                pass

        return redirect("/admin/login")


    return wrapper
