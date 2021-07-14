from django.contrib import admin

from . import models


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'responsible', 'verified_date')

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
