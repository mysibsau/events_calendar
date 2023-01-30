from itertools import chain

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
from apps.user.models import UserRole
from apps.events.services.exporters import export_as_csv


class EventViewSet(ModelViewSet):
    serializer_class = serializers.EventDetailSerializer
    queryset = models.Event.objects.all()
    permission_classes = [permissions.IsOwnerOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("level",
                     "educational_work_in_opop",
                     "role",
                     "format",
                     "organization",
                     "direction")

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

    def validate_event(self, event, user):
        allowed_users = [
            event.author,
            *list(
                chain.from_iterable(
                    [
                        user.get_my_invites(role)
                        for role in [
                            UserRole.author,
                            UserRole.moderator,
                            UserRole.administrator,
                            UserRole.super_admin,
                        ]
                    ]
                )
            ),
        ]
        if event.author not in allowed_users:
            return Response({"detail": "Это не ваше мероприятие"}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=["post"])
    def generate_report(self, request, pk=None):
        event = self.get_object()
        if error := self.validate_event(event, self.request.user):
            return error
        report = models.Report.objects.create(
            count_index=request.data['count_index'],
            name=event.name,
            description=event.description,
            organization=event.organization,
            start_date_fact=request.data['start_date_fact'],
            stop_date_fact=request.data['stop_date_fact'],
            place_fact=request.data['place_fact'],
            coverage_participants_fact=request.data['coverage_participants_fact'],
            links=request.data['links']

        )

        for organizator in request.data['organizators']:
            orgz = models.Organiztor.objects.create(
                name=organizator['name'],
                position=organizator['position'],
                description=organizator['description']
            )
            report.organizators.add(orgz)
            orgz.save()
        event.report = report
        event.status = 5
        event.save()
        report.save()

        return Response({
            "report_id": report.id
        })

    @action(detail=True, methods=["get"])
    def export_report(self, request, pk=None):
        event = self.get_object()
        if error := self.validate_event(event, self.request.user):
            return error

        if self.request.user.role in [UserRole.administrator, UserRole.moderator]:
            return report_exporter(event)

        return Response(
            {"response": "Вы не можете выполнить данное действие"},
            status=status.HTTP_403_FORBIDDEN,
        )

    @action(detail=True, methods=["get"])
    def get_report(self, request, pk=None):
        event = self.get_object()
        if error := self.validate_event(event, self.request.user):
            return error
        if event.report is None:
            return Response(
                {
                    "response": "Для этого мероприятия еще нет отчета"
                },
                status=status.HTTP_403_FORBIDDEN
            )
        report = event.report
        report = serializers.ReportSerializer(report)

        return Response(report.data)

    @action(detail=False, methods=["get"])
    def get_reports_csv(self, request, pk=None):
        reports = models.Report.objects.all().filter(event__status=3)

        return export_as_csv(reports)

    @action(detail=True, methods=["post"])
    def verificate(self, request, pk=None):
        event = self.get_object()
        if error := self.validate_event(event, self.request.user):
            return error
        event.verificate()
        return Response({"status": event.status})

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        event = self.get_object()
        if error := self.validate_event(event, self.request.user):
            return error
        event.reject(request.data["comment"])

        return Response({"status": event.status})


class DirectionViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = serializers.DirectionSerializer
    queryset = models.Direction.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_fields = ["id", "name"]


class OrgRoleViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = serializers.OrgRoleSerializer
    queryset = models.OrganizatorRole.objects.all()


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


class EventGroupViewsSet(ModelViewSet):
    serializer_class = serializers.EventGroupSerializer
    queryset = models.EventGroup.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.EventGroup.objects.all().filter(author=self.request.user)
