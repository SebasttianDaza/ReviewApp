import sys, requests, time
from ReviewApp.settings import env
from urllib.parse import quote, quote_plus


def get_signature_twitter():
    from hashlib import sha1
    import hmac
    import base64

    query = [
        f'oauth_callback={quote(env("OAUTH_CALLBACK_URL_TWITTER"))}',
        f'oauth_consumer_key={env("API_KEY_TWITTER")}',
        'oauth_nonce=ea9ec8429b68d6b77cd5600adbbb0456',
        'oauth_signature_method=HMAC-SHA1',
        f'oauth_timestamp={round(time.time())}',
        f'oauth_token={env("OAUTH_TOKEN_TWITTER")}',
        'oauth_version=1.0'
    ]

    signature_base = f"POST&{env('API_TWITTER')}&{quote_plus('&'.join(query))}"
    key = f"{env('API_SECRET_TWITTER')}&{env('OAUTH_TOKEN_SECRET_TWITTER')}"

    hashed = hmac.new(key.encode("utf-8"), signature_base.encode("utf-8"), sha1)

    return quote_plus(base64.urlsafe_b64encode(hashed.digest()).decode("utf-8"))


def auth_twitter_middleware(get_response):
    def middleware(request):
        response = get_response(request)

        try:
            auth = [
                f'OAuth oauth_callback="{quote(env("OAUTH_CALLBACK_URL_TWITTER"))}"',
                f'oauth_consumer_key="{env("API_KEY_TWITTER")}"',
                'oauth_nonce="ea9ec8429b68d6b77cd5600adbbb0456"',
                f'oauth_signature="{get_signature_twitter()}"',
                'oauth_signature_method="HMAC-SHA1"',
                f'oauth_timestamp="{round(time.time())}"',
                'oauth_version="1.0"'
            ]

            headers = {
                "Authorization": ", ".join(auth)
            }
            print(headers)
            sys.exit()

            res = requests.post(f"{env('API_TWITTER')}", headers=headers)
            if res.status_code == 200:
                print(res.json())
                sys.exit()
            else:
                print(res)
                sys.exit(res.json())
        except requests.exceptions.RequestException:
            pass

        return response

    return middleware
