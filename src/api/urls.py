from django.urls import path
from rest_framework.routers import SimpleRouter

from api.events import views as event_views
from api.user.views import UserViewSet, obtain_auth_token

router = SimpleRouter()
router.register("events", event_views.EventViewSet)
router.register("event_groups", event_views.EventGroupViewsSet)
router.register("users", UserViewSet)
router.register("comment", event_views.CommentViewSet)
router.register("reference/directions", event_views.DirectionViewSet)
router.register("reference/levels", event_views.LevelViewSet)
router.register("reference/roles", event_views.RoleViewSet)
router.register("reference/formats", event_views.FormatViewSet)
router.register("reference/organizations", event_views.OrganizationViewSet)


urls = [
    path("event/vereficate/<int:event_id>", event_views.VerifyEvent.as_view()),
    path("auth/", obtain_auth_token),
] + router.urls
