from django.contrib import admin
from .models import AuthUser
from django.contrib.auth.admin import UserAdmin


class AuthUserAdmin(UserAdmin):
    model = AuthUser
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