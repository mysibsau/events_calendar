from django.db import transaction
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer as AuthTokenSerializerDefault

from apps.user.models import Invite, PersonalStatus, User, UserRole


class AuthTokenSerializer(AuthTokenSerializerDefault):
    id = serializers.IntegerField(label="ID", read_only=True)
    name = serializers.CharField(label="Имя отчество пользователя", read_only=True)
    role = serializers.ChoiceField(label="Роль пользователя", read_only=True, choices=UserRole.choices)
    code = serializers.CharField(label="Код подтверждения", write_only=True, required=False, allow_blank=True)

    def _code_is_valid(self, attrs):
        try:
            return Invite.objects.filter(pk=attrs.get("code"), user__isnull=True).exists()
        except:
            return False

    def _user_is_exist(self, attrs):
        try:
            return User.objects.filter(username=attrs.get("username")).exists()
        except:
            return False

    def validate(self, attrs):
        with transaction.atomic():
            if self._user_is_exist(attrs):
                attrs = super().validate(attrs)
            elif self._code_is_valid(attrs):
                attrs = super().validate(attrs)
                invite = Invite.objects.get(pk=attrs.get("code"))
                invite.user = attrs.get("user")
                invite.save()
                attrs.get("user").role = invite.role
                attrs.get("user").status = invite.status
                attrs.get("user").position = invite.position
                attrs.get("user").save()
            else:
                raise serializers.ValidationError("Неверный код подтверждения")

            return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "contact_info", "role", "status", "position", "creation_date")


class CreateInviteSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(label="Роль пользователя", choices=UserRole.choices)
    status = serializers.ChoiceField(label="Статус пользователя", choices=PersonalStatus.choices)
    contact_info = serializers.CharField(label="Контактная информация")

    class Meta:
        model = Invite
        fields = ("role", "position", "status", "contact_info")


class InviteSerializer(serializers.Serializer):
    code = serializers.CharField(label="Код приглашения", read_only=True)


class MyInvitesSerializer(serializers.Serializer):
    role = serializers.ChoiceField(label="Роль пользователя", choices=UserRole.choices)


class EditUser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("contact_info",)


class DeleteUserSerializer(serializers.Serializer):
    user_for_transfer = serializers.IntegerField(label="ID пользователя которому передают мероприятия/авторов")
