from django.db.models import Count, Avg
from django.db.models.functions import Coalesce
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from . import models, serializers, permissions, services


class EventViewSet(ModelViewSet):
    queryset = models.Event.objects.filter(
        start_date__gt=timezone.now(),
    ).annotate(
        num_participants=Count('request', distinct=True),
        avg_rate=Coalesce(Avg('feedback__rating'), 0.0)
    )
    serializer_class = serializers.EventSerializer
    permission_classes = [permissions.IsConfirmedOrReadOnly, permissions.IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['name']
    search_fields = ['name', 'start_date', 'user__username']
    ordering_fields = ['name', 'start_date', 'user__username', 'num_participants', 'avg_rate']

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        serializer.save()


class MyEventViewSet(EventViewSet):
    queryset = None
    permission_classes = [IsAuthenticated, permissions.IsOwnerOrReadOnly]

    def get_queryset(self):
        return services.gey_my_events(self.request.user)


class EventDetailView(RetrieveAPIView):
    queryset = models.Event.objects.all().select_related()
    serializer_class = serializers.EventDetailSerializer
