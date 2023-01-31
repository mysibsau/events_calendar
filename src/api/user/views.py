from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken as StandartObtainAuthToken
from rest_framework.decorators import action
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.user.serializer import (
    AuthTokenSerializer,
    CreateInviteSerializer,
    EditUser,
    InviteSerializer,
    MyInvitesSerializer,
    UserSerializer,
    DeleteUserSerializer
)
from apps.user.models import Invite, User, UserRole
from apps.events.models.event import Event


class ObtainAuthToken(StandartObtainAuthToken):
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "role": user.role,
                "name": user.first_name,
                "id": user.id,
            }
        )


obtain_auth_token = ObtainAuthToken.as_view()


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"


class UserViewSet(ReadOnlyModelViewSet, UpdateModelMixin, DestroyModelMixin):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filter_fields = ["username", "email"]
    search_fields = ["username", "email"]

    def get_serializer_class(self):
        if self.action in ("update", "partial_update"):
            return EditUser
        return self.serializer_class

    def get_permissions(self):
        if self.action in ("update", "partial_update"):
            return []
        return super().get_permissions()

    def update(self, request, *args, **kwargs):
        if request.user != self.get_object():
            return Response({"error": "вы не можете редактировать других пользователей"}, status=403)
        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=['delete'])
    def delete_user(self, request, pk=None):
        delete_user = self.get_object()
        serializer = DeleteUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        transfer_user = User.objects.filter(id=request.data["user_for_transfer"]).first()
        events = Event.objects.all().filter(author=delete_user)

        if delete_user.role == UserRole.author:

            if events:
                for event in events:
                    event.author = transfer_user
                    if event.original_author is None:
                        event.original_author = str(delete_user.get_full_name())
                    event.save()

            delete_user.delete()
            return Response({"detail": "Пользователь успешно удален"}, status=200)

        if delete_user.role == UserRole.moderator and transfer_user.role == UserRole.moderator:
            invites = Invite.objects.all().filter(author=delete_user)
            if invites:
                for invite in invites:
                    invite.author = transfer_user
                    invite.save()

            if events:
                for event in events:
                    event.author = transfer_user
                    if event.original_author is None:
                        event.original_author = str(delete_user.get_full_name())
                    event.save()

            delete_user.delete()
            return Response({"detail": "Пользователь успешно удален"}, status=200)

        else:
            return Response({"detail": "Автор не может перенять других пользователей"}, status=403)

    @swagger_auto_schema(request_body=CreateInviteSerializer, responses={200: InviteSerializer})
    @action(detail=False, methods=["post"])
    def invite(self, request):
        serializer = CreateInviteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        role = serializer.validated_data["role"]
        if user.role < UserRole.moderator or role >= user.role:
            return Response({"detail": "Недостаточно прав"}, status=403)
        invite = serializer.save(author=user)
        return Response({"code": invite.id})

    @swagger_auto_schema(responses={200: UserSerializer}, request_body=MyInvitesSerializer)
    @action(detail=False, methods=["post"])
    def my_invites(self, request):
        serializer = MyInvitesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        invites = user.get_my_invites(serializer.validated_data["role"])
        serializer = UserSerializer(invites, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def get_all_authors(self, request):
        if self.request.user.role not in [UserRole.administrator, UserRole.super_admin]:
            return Response(
                {'response': 'У вас недостаточно прав'}
            )
        authors_list = []
        authors = User.objects.all().filter(role=UserRole.author)
        for author in authors:
            authors_list.append(UserSerializer(author).data)

        return Response(authors_list)

    @action(detail=False, methods=['get'])
    def get_all_moderators(self, request):
        if self.request.user.role not in [UserRole.administrator, UserRole.super_admin]:
            return Response(
                {'response': 'У вас недостаточно прав'}
            )
        moderators_list = []
        moderators = User.objects.all().filter(role=UserRole.moderator)
        for moderator in moderators:
            moderators_list.append(UserSerializer(moderator).data)

        return Response(moderators_list)
