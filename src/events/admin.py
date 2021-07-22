import csv

from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html
from rangefilter.filter import DateRangeFilter

from . import models


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'responsible', 'verified_date', 'event_actions')
    list_filter = (
        ('start_date', DateRangeFilter),
    )

    actions = ['export_as_csv']

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
        return format_html(
            obj.verified.first_name + '<a class="deletelink" href="{}"></a>',
            reverse('admin:cancle_verificate', args=[obj.pk])
        )

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
            url(
                r'^(?P<event_id>.+)/cancle_verificate/$',
                self.admin_site.admin_view(self.cancle_verificate),
                name='cancle_verificate',
            ),
        ]
        return custom_urls + urls

    def verificate(self, request, event_id, *args, **kwargs):
        models.Event.objects.filter(id=event_id).update(
            verified=request.user,
            verified_date=timezone.now(),
        )
        return HttpResponseRedirect("../../")

    def cancle_verificate(self, request, event_id, *args, **kwargs):
        models.Event.objects.filter(id=event_id).update(
            verified=None,
            verified_date=None,
        )
        return HttpResponseRedirect("../../")

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={meta.verbose_name_plural}_{timezone.localtime()}.csv'

        writer = csv.writer(response)
        writer.writerow(field.verbose_name for field in meta.fields)

        for obj in queryset:
            writer.writerow(
                obj.__getattribute__(field.name)
                for field in meta.fields
            )

        return response

    export_as_csv.short_description = 'Экспортировать в csv'


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
