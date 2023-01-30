from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from rangefilter.filters import DateRangeFilter

from . import models
from .services import verification
from .services.exporters import export_as_csv


@admin.register(models.Report)
class RepAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Organiztor)
class OrgAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "start_date", "verified_date", "event_actions", "author", "status")
    list_filter = (("start_date", DateRangeFilter),)

    actions = ["export_as_csv"]

    fields = (
        ("name", "direction"),
        "comment",
        "free_plan",
        ("level", "role", "format"),
        ("educational_work_in_opop", "hours_count"),
        ("start_date", "stop_date"),
        "place",
        ("coverage_participants_plan", "number_organizers"),
        "organization",
        "coverage_participants_fact",
        "links",
        'group',
        'organizators'
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


@admin.register(models.EventGroup)
class GroupEvent(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(models.OrganizatorRole)
class OrgRoleAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
