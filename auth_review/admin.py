from django.contrib import admin

from .decorators import oauth_twitter_token
from .models import AuthUser
from django.contrib.auth.admin import UserAdmin
from django.utils.decorators import method_decorator


class AuthUserAdmin(UserAdmin):
    model = AuthUser
    @method_decorator(oauth_twitter_token)
    def add_view(self, request, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context["login_twitter"] = True
        return super().add_view(
            request,
            form_url,
            extra_context=extra_context,
        )

# Register your models here.
admin.site.register(AuthUser, AuthUserAdmin)