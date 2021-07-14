from django.urls import path
from events import views as event_views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('events', event_views.EventViewSet)
router.register('events/(?P<month>[0-9]{2}).(?P<year>[0-9]{4})', event_views.EventViewSet)

urls = [
    path('events/<int:pk>', event_views.EventDetailView.as_view()),
]

__all__ = [
    router,
    urls,
]
