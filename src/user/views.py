from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken as StandartObtainAuthToken
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializer import AuthTokenSerializer, ProfileSerializer


class ObtainAuthToken(StandartObtainAuthToken):
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'confirmed': user.confirmed,
            'name': user.first_name,
            'is_staff': user.is_staff,
            'id': user.id,
        })


obtain_auth_token = ObtainAuthToken.as_view()


class ProfileView(RetrieveModelMixin, GenericAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
