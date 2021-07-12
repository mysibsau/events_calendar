from django.contrib import admin
from django.db.models import Count, Avg

from . import models


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_date', 'start_date', 'user', 'num_participants', 'avg_rate')

    def num_participants(self, obj):
        return obj.num_participants
    num_participants.short_description = 'Заявок'

    def avg_rate(self, obj):
        return obj.avg_rate
    avg_rate.short_description = 'Средний балл'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(num_participants=Count('request', distinct=True), avg_rate=Avg('feedback__rating'))


@admin.register(models.Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'date')


@admin.register(models.Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'date', 'rating')
