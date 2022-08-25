from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from rangefilter.filters import DateRangeFilter

from . import models
from .services import verification
from .services.exporters import export_as_csv
from apps.helpers.report_exporter import report_exporter


class ImportantDateInline(admin.TabularInline):
    model = models.ImportantDate


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "start_date", "responsible", "verified_date", "event_actions", "author", "status")
    list_filter = (("start_date", DateRangeFilter),)

    inlines = [ImportantDateInline]

    actions = ["export_as_csv", "generate_report"]

    fields = (
        ("name", "direction"),
        "free_plan",
        ("level", "role", "format"),
        ("educational_work_in_opop", "hours_count"),
        "educational_work_outside_opop",
        ("start_date", "stop_date"),
        "place",
        ("coverage_participants_plan", "number_organizers"),
        ("responsible", "position", "organization"),
        "coverage_participants_fact",
        "links",
        "description",
    )

    def event_actions(self, obj):
        if not obj.verified:
            return format_html(
                '<a class="button" href="{}">Верифицировать</a>', reverse("admin:verification", args=[obj.pk])
            )
        return format_html(
            obj.verified.first_name + '<a class="deletelink" href="{}"></a>',
            reverse("admin:cancle_verificate", args=[obj.pk]),
        )

    event_actions.short_description = "Верификация"
    event_actions.allow_tags = True

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r"^(?P<event_id>.+)/verification/$",
                self.admin_site.admin_view(self.verificate),
                name="verification",
            ),
            url(
                r"^(?P<event_id>.+)/cancle_verificate/$",
                self.admin_site.admin_view(self.cancle_verificate),
                name="cancle_verificate",
            ),
        ]
        return custom_urls + urls

    def verificate(self, request, event_id, *args, **kwargs):
        verification.verify_event(event_id, request.user)
        return HttpResponseRedirect("../../")

    def cancle_verificate(self, request, event_id, *args, **kwargs):
        verification.cancel_event_verification(event_id)
        return HttpResponseRedirect("../../")

    def export_as_csv(self, request, queryset):
        return export_as_csv(queryset)

    def generate_report(self, request, event_id):
        return report_exporter(event_id)

    generate_report.short_description = "Создать отчет"
    export_as_csv.short_description = "Экспортировать в csv"

    def save_model(self, request, obj, *args) -> None:
        obj.author = request.user
        return super().save_model(request, obj, *args)


@admin.register(models.Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(models.Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(models.Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(models.Format)
class FormatAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(models.Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "event")


@admin.register(models.ImportantDate)
class ImportantDateAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "date", "event")
