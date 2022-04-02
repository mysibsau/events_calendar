from django.urls import path
from rest_framework.routers import SimpleRouter

from api.events import views as event_views
from api.user.views import ProfileView, UserViewSet, obtain_auth_token

router = SimpleRouter()
router.register('events', event_views.EventViewSet)
router.register('users', UserViewSet)
router.register('events/(?P<month>[0-9]{2}).(?P<year>[0-9]{4})', event_views.EventViewSet)
router.register('event', event_views.EventDetailView)
router.register('comment', event_views.CommentViewSet)
router.register('reference/directions', event_views.DirectionViewSet)
router.register('reference/levels', event_views.LevelViewSet)
router.register('reference/roles', event_views.RoleViewSet)
router.register('reference/formats', event_views.FormatViewSet)
router.register('reference/organizations', event_views.OrganizationViewSet)


urls = [
    path('user/', ProfileView.as_view()),
    path('event/vereficate/<int:event_id>', event_views.VerifyEvent.as_view()),
    path('auth/', obtain_auth_token),
] + router.urls
