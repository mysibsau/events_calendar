from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.user'
    verbose_name = 'Пользователи'

    def ready(self) -> None:
        from django.contrib import admin
        from apps.user.forms import AdminAuthenticationForm

        admin.site.login_form = AdminAuthenticationForm
