from django.contrib.auth.views import LoginView as BaseLoginView
from ReviewApp.settings import env


class LoginView(BaseLoginView):
    template_name = "admin/login.html"

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""
        auth_token_twitter = self.request.get_signed_cookie(
            key="OAUTH_TOKEN_TWITTER",
            salt=env("API_KEY_TWITTER")
        )
        kwargs["auth_token_twitter"] = auth_token_twitter
        return self.render_to_response(
            self.get_context_data(**kwargs),
        )
