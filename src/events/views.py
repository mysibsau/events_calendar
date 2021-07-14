from django.utils import timezone
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from . import models, serializers, permissions


class EventViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = serializers.EventSerializer
    queryset = models.Event.objects.all()

    def list(self, request, year=timezone.now().year, month=timezone.now().month, *args, **kwargs):
        """
        Получение списка мероприятий по датам

        если не передан year или month, то вернет мероприятия на текущий месяц
        """
        queryset = models.Event.objects.filter(start_date__year=year, start_date__month=month)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


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

    def perform_create(self, serializer):
        serializer.validated_data['responsible'] = self.request.user
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
