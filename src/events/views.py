from django.db.models import Q
from django.utils import timezone
from rest_framework import mixins, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from . import models, serializers, permissions
from .services import verification
from rest_framework.decorators import api_view
from datetime import datetime


class EventViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = serializers.EventSerializer
    queryset = models.Event.objects.all()
    permissions = {
        'my': [IsAuthenticated()],
        'unverified': [IsAdminUser()],
    }

    def get_permissions(self):
        return self.permissions.get(self.action, super().get_permissions())

    def list(self, request, year=timezone.now().year, month=timezone.now().month, *args, **kwargs):
        """
        Получение списка мероприятий по датам

        если не передан year или month, то вернет мероприятия на текущий месяц
        """
        queryset = models.Event.objects.filter(
            Q(start_date__year=year, start_date__month=month) |
            Q(stop_date__year=year, stop_date__month=month)
        )
        if not request.user.is_staff:
            queryset = queryset.filter(verified__isnull=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def my(self, request):
        self.queryset = models.Event.objects.filter(author=request.user)
        return super().list(request)

    @action(detail=False)
    def unverified(self, request):
        self.queryset = models.Event.objects.filter(verified__isnull=True)
        return super().list(request)


class EventDetailView(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      GenericViewSet):
    """
    Получение детальной информации

    """
    queryset = models.Event.objects.all().select_related()
    serializer_class = serializers.EventDetailSerializer
    permission_classes = [permissions.IsOwnerOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['can_edit'] = request.user.is_staff or instance.author == request.user
        return Response(data)

    def perform_create(self, serializer):
        serializer.validated_data['author'] = self.request.user
        if not serializer.validated_data.get('stop_date'):
            serializer.validated_data['stop_date'] = serializer.validated_data['start_date']
        serializer.save()


class DirectionViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = serializers.DirectionSerializer
    queryset = models.Direction.objects.all()


class LevelViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = serializers.LevelSerializer
    queryset = models.Level.objects.all()


class RoleViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = serializers.RoleSerializer
    queryset = models.Role.objects.all()


class FormatViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = serializers.FormatSerializer
    queryset = models.Format.objects.all()


class OrganizationViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = serializers.OrganizationSerializer
    queryset = models.Organization.objects.all()


class VerifyEvent(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, event_id, *args, **kwargs):
        verification.verify_event(event_id, request.user)

        return Response(status=status.HTTP_200_OK)

    def delete(self, request, event_id, *args, **kwargs):
        verification.cancel_event_verification(event_id)

        return Response(status=status.HTTP_200_OK)


class CommentViewSet(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    permission_classes = [IsAuthenticated, permissions.IsOwnerCommentOrReadOnly]
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def perform_create(self, serializer):
        serializer.validated_data['author'] = self.request.user
        serializer.save()

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)
