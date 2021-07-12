from django.urls import path
from rest_framework.routers import SimpleRouter

from events import views as event_views

router = SimpleRouter()
router.register('events', event_views.EventViewSet)
router.register('my_events', event_views.MyEventViewSet, basename='my_events')

urls = [
    path('events/<int:pk>/detail', event_views.EventDetailView.as_view()),
]

__all__ = [
    router,
    urls,
]
