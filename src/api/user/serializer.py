from apps.user.models import User, UserRole
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer as AuthTokenSerializerDefault


class AuthTokenSerializer(AuthTokenSerializerDefault):
    id = serializers.IntegerField(label="ID", read_only=True)
    name = serializers.CharField(label="Имя отчество пользователя", read_only=True)
    role = serializers.ChoiceField(label="Роль пользователя", read_only=True, choices=UserRole.choices)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "role")
