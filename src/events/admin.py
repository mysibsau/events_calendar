from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html

from . import models


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'responsible', 'verified_date', 'event_actions')

    fields = (
        ('name', 'direction'),
        'free_plan',
        ('level', 'role', 'format'),
        ('educational_work_in_opop', 'hours_count'),
        'educational_work_outside_opop',
        ('start_date', 'stop_date'),
        'place',
        ('coverage_participants_plan', 'number_organizers'),
        ('responsible', 'organization'),
        'coverage_participants_fact',
        'links'
    )

    def event_actions(self, obj):
        if not obj.verified:
            return format_html(
                '<a class="button" href="{}">Верифицировать</a>',
                reverse('admin:verification', args=[obj.pk])
            )
        return obj.verified.first_name

    event_actions.short_description = 'Верификация'
    event_actions.allow_tags = True

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r'^(?P<event_id>.+)/verification/$',
                self.admin_site.admin_view(self.verificate),
                name='verification',
            ),
        ]
        return custom_urls + urls

    def verificate(self, request, event_id, *args, **kwargs):
        models.Event.objects.filter(id=event_id).update(
            verified=request.user,
            verified_date=timezone.now()
        )
        return HttpResponseRedirect("../../")


@admin.register(models.Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(models.Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(models.Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(models.Format)
class FormatAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(models.Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'event')
