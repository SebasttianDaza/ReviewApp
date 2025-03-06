def get_signature_twitter(url, auth, method="POST"):
    from ReviewApp.settings import env
    from urllib.parse import quote_plus
    from hashlib import sha1
    import hmac
    import base64

    signature_base = f"{method}&{quote_plus(url)}&{quote_plus('&'.join(auth))}"
    key = f"{env('API_SECRET_TWITTER')}&{env('OAUTH_TOKEN_SECRET_TWITTER')}"
    hashed = hmac.new(key.encode("utf-8"), signature_base.encode("utf-8"), sha1)

    return quote_plus(base64.urlsafe_b64encode(hashed.digest()).decode("utf-8"))


def get_oauth1_twitter(
        oauth_token,
        time_signature,
        oauth_token_secret,
        url,
        method="POST",
):
    auth = [
        f'oauth_consumer_key={oauth_token}',
        'oauth_nonce=ea9ec8429b68d6b77cd5600adbbb0456',
        'oauth_signature_method=HMAC-SHA1',
        f'oauth_timestamp={time_signature}',
        f'oauth_token={oauth_token_secret}',
        'oauth_version=1.0'
    ]
    auth.insert(3, f'oauth_signature="{get_signature_twitter(url, auth, method)}"')
    headers = {
        "Authorization": "{0} {1}".format("OAuth", ", ".join(auth)),
        "Content-Type": "application/json"
    }

    return headers