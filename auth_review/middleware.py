import sys

import requests, time, logging

from django.core.signing import BadSignature

from ReviewApp.settings import env
from urllib.parse import quote_plus


def AuthTwitterMiddleware(get_response):
    def middleware(request):
        from auth_review.http.request import get_signature_twitter
        response = get_response(request)

        try:
            cookie_token = request.get_signed_cookie(
                key="OAUTH_TOKEN_TWITTER",
                salt=env("API_KEY_TWITTER")
            )
            if cookie_token:
                return response
        except KeyError or BadSignature:
            pass

        if (
            request.user.is_authenticated or
            request.path not in ["/admin/login/", "/redirect", "/admin/auth/user/add/"]
        ):
            return response

        logger = logging.getLogger("review_app.middleware")
        try:
            time_signature = round(time.time())
            url = f"{env('API_TWITTER')}/oauth/request_token"
            auth = [
                f'oauth_callback={quote_plus(env("OAUTH_CALLBACK_URL_TWITTER"))}',
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
                raise requests.exceptions.RequestException
        except (
                requests.exceptions.RequestException or
                requests.exceptions.ConnectionError or
                requests.exceptions.Timeout or
                requests.exceptions.TooManyRedirects
        ):
            logger.warn(
                "Exception raised while requesting twitter authorization.",
                exc_info=True
            )
            pass

        return response

    return middleware
