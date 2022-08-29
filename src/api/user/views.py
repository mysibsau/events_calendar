from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken as StandartObtainAuthToken
from rest_framework.decorators import action
from rest_framework.mixins import UpdateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.user.serializer import (
    AuthTokenSerializer,
    CreateInviteSerializer,
    EditUser,
    InviteSerializer,
    MyInvitesSerializer,
    UserSerializer,
)
from apps.user.models import Invite, User, UserRole


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


class UserViewSet(ReadOnlyModelViewSet, UpdateModelMixin):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
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
    @action(detail=False, methods=["get"])
    def my_invites(self, request):
        serializer = MyInvitesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        invites = user.get_my_invites(serializer.validated_data["role"])
        serializer = UserSerializer(invites, many=True)
        return Response(serializer.data)
