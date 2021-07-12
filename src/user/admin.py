from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html

from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'get_full_name', 'email', 'confirmed', 'user_actions')

    def do_confirm(self, request, user_id, *args, **kwargs):
        models.User.objects.filter(id=user_id).update(confirmed=True)
        return HttpResponseRedirect("../../")

    def do_ban(self, request, user_id, *args, **kwargs):
        models.User.objects.filter(id=user_id).update(is_active=False)
        return HttpResponseRedirect("../../")

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r'^(?P<user_id>.+)/confirm/$',
                self.admin_site.admin_view(self.do_confirm),
                name='user-confirm',
            ),
            url(
                r'^(?P<user_id>.+)/ban/$',
                self.admin_site.admin_view(self.do_ban),
                name='user-ban',
            ),
        ]
        return custom_urls + urls

    def user_actions(self, obj):
        if not obj.confirmed:
            return format_html(
                '<a class="button" href="{}">Подтвердить</a>',
                reverse('admin:user-confirm', args=[obj.pk])
            )
        return format_html(
            '<a class="deletelink" href="{}">Заблокировать</a>',
            reverse('admin:user-ban', args=[obj.pk])
        )

    user_actions.short_description = 'Действия'
    user_actions.allow_tags = True
