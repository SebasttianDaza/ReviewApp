from django.contrib.auth.forms import AuthenticationForm as DjangoAuthenticationForm, UsernameField


class AuthenticationForm(DjangoAuthenticationForm):
    use_required_attribute = False
