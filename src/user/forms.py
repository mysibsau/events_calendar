from django.contrib.admin.forms import AdminAuthenticationForm as AdminAuthenticationFormDefault
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError


class AdminAuthenticationForm(AdminAuthenticationFormDefault):
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            elif not self.user_cache.confirmed:
                raise ValidationError(
                    "%(username)s, твоя учетная запись еще не подтверждена."
                    "Пожалуйста, дождись пока администратор проверит ее.",
                    code='invalid_login',
                    params={'username': self.user_cache.first_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
