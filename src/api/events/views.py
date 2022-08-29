from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from api.events import permissions, serializers
from api.user.serializer import MyInvitesSerializer
from apps.events import models
from apps.events.services import verification
from apps.helpers.report_exporter import report_exporter


class EventViewSet(ModelViewSet):
    serializer_class = serializers.EventDetailSerializer
    queryset = models.Event.objects.all()
    permission_classes = [permissions.IsOwnerOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("id", "name")

    def get_queryset(self):
        if self.action == "my":
            return self.queryset.filter(author=self.request.user)
        return self.queryset

    @action(detail=False)
    def my(self, request):
        return super().list(request)

    @swagger_auto_schema(responses={200: serializers.EventDetailSerializer}, request_body=MyInvitesSerializer)
    @action(detail=False, methods=["post"])
    def my_invites(self, request):
        serializer = MyInvitesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        invites = user.get_my_invites(serializer.validated_data["role"])
        events = self.queryset.filter(author__in=invites)
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def generate_report(self, request, pk=None):
        event = self.get_object()
        return report_exporter(event.id)


class DirectionViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = serializers.DirectionSerializer
    queryset = models.Direction.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = ["id", "name"]


class LevelViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = serializers.LevelSerializer
    queryset = models.Level.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = ["id", "name"]


class RoleViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = serializers.RoleSerializer
    queryset = models.Role.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = ["id", "name"]


class FormatViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = serializers.FormatSerializer
    queryset = models.Format.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = ["id", "name"]


class OrganizationViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = serializers.OrganizationSerializer
    queryset = models.Organization.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = ["id", "name"]


class VerifyEvent(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, event_id, *args, **kwargs):
        verification.verify_event(event_id, request.user)

        return Response(status=status.HTTP_200_OK)

    def delete(self, request, event_id, *args, **kwargs):
        verification.cancel_event_verification(event_id)

        return Response(status=status.HTTP_200_OK)


class CommentViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated, permissions.IsOwnerCommentOrReadOnly]
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def perform_create(self, serializer):
        serializer.validated_data["author"] = self.request.user
        serializer.save()

    def update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return super().update(request, *args, **kwargs)
