import requests, time, logging

from django.core.signing import BadSignature

from ReviewApp.settings import env
from urllib.parse import quote_plus


def get_signature_twitter(time_signature):
    from hashlib import sha1
    import hmac
    import base64

    query = [
        f'oauth_callback={quote_plus(env("OAUTH_CALLBACK_URL_TWITTER"))}',
        f'oauth_consumer_key={env("API_KEY_TWITTER")}',
        'oauth_nonce=ea9ec8429b68d6b77cd5600adbbb0456',
        'oauth_signature_method=HMAC-SHA1',
        f'oauth_timestamp={time_signature}',
        f'oauth_token={env("OAUTH_TOKEN_TWITTER")}',
        'oauth_version=1.0'
    ]

    signature_base = f"POST&{quote_plus(env('API_TWITTER'))}&{quote_plus('&'.join(query))}"
    key = f"{env('API_SECRET_TWITTER')}&{env('OAUTH_TOKEN_SECRET_TWITTER')}"

    hashed = hmac.new(key.encode("utf-8"), signature_base.encode("utf-8"), sha1)

    return quote_plus(base64.urlsafe_b64encode(hashed.digest()).decode("utf-8"))


def auth_twitter_middleware(get_response):
    def middleware(request):
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
            "/admin/login" not in request.path
        ):
            return response

        time_signature = round(time.time())
        logger = logging.getLogger("review_app.middleware")

        try:
            auth = [
                f'OAuth oauth_callback="{quote_plus(env("OAUTH_CALLBACK_URL_TWITTER"))}"',
                f'oauth_consumer_key="{env("API_KEY_TWITTER")}"',
                'oauth_nonce="ea9ec8429b68d6b77cd5600adbbb0456"',
                f'oauth_signature="{get_signature_twitter(time_signature)}"',
                'oauth_signature_method="HMAC-SHA1"',
                f'oauth_timestamp="{time_signature}"',
                f'oauth_token="{env("OAUTH_TOKEN_TWITTER")}"',
                'oauth_version="1.0"'
            ]

            headers = {
                "Authorization": ", ".join(auth)
            }

            res = requests.post(f"{env('API_TWITTER')}", headers=headers)
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
