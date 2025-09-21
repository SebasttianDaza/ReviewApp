def get_signature_twitter(
    url,
    auth,
    method="POST",
    oauth_token_secret=None
):
    from ReviewApp.settings import env
    from urllib.parse import quote_plus
    from hashlib import sha1
    import hmac
    import base64
    if oauth_token_secret is None:
        oauth_token_secret = env('OAUTH_TOKEN_SECRET_TWITTER')

    signature_base = f"{method}&{quote_plus(url)}&{quote_plus('&'.join(auth))}"
    key = f"{env('API_SECRET_TWITTER')}&{oauth_token_secret}"
    hashed = hmac.new(key.encode("utf-8"), signature_base.encode("utf-8"), sha1)

    return quote_plus(base64.urlsafe_b64encode(hashed.digest()).decode("utf-8"))
