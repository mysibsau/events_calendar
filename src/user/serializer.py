from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer as AuthTokenSerializerDefault
from .models import User


class AuthTokenSerializer(AuthTokenSerializerDefault):
    name = serializers.CharField(
        label="Имя отчество пользователя",
        read_only=True
    )
    confirmed = serializers.BooleanField(
        label="Подтвержденный ли аккаунт",
        read_only=True
    )
    is_staff = serializers.BooleanField(
        label="является ли сотрудником",
        read_only=True,
    )


class ProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        label='Имя отчество пользователя',
        source='first_name',
        read_only=True
    )

    class Meta:
        model = User
        fields = ('name', 'confirmed', 'is_staff')
