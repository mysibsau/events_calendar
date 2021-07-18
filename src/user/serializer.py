from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer as AuthTokenSerializerDefault
from django.utils.translation import gettext_lazy as _


class AuthTokenSerializer(AuthTokenSerializerDefault):
    name = serializers.CharField(
        label=_("name"),
        read_only=True
    )
    confirmed = serializers.BooleanField(
        label=_("confirmed"),
        read_only=True
    )
