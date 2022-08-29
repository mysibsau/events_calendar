from rest_framework import serializers

from apps.events import models
from apps.user.models import User


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True, label="Id автора")
    author_name = serializers.CharField(
        source="author.first_name",
        read_only=True,
        label="Имя отчество автора",
        allow_blank=True,
    )
    text = serializers.CharField(allow_blank=False)

    class Meta:
        model = models.Comment
        fields = ("id", "author", "author_name", "text", "event", "date")



class EventSerializer(serializers.ModelSerializer):
    # TODO: Эта дичь может возвращать none, нужно пофиксить
    is_verified = serializers.BooleanField(read_only=True, source="verified")
    author = serializers.PrimaryKeyRelatedField(read_only=True, label="Id автора")

    def create(self, validated_data):
        user = self.context["request"].user
        if not user or not user.is_authenticated:
            raise serializers.ValidationError("Вы не авторизованы")
        validated_data["author"] = user
        return super().create(validated_data)

    class Meta:
        model = models.Event
        fields = "__all__"


class OrganizatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Organiztor
        fields = "__all__"


class EventDetailSerializer(serializers.ModelSerializer):
    verified = serializers.StringRelatedField(source="verified.first_name", read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.CharField(read_only=True)
    verified_date = serializers.DateTimeField(read_only=True)
    organizators = OrganizatorSerializer(many=True, required=False)


    class Meta:
        model = models.Event
        fields = "__all__"


class DirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Direction
        fields = "__all__"


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Level
        fields = "__all__"


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = "__all__"


class FormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Format
        fields = "__all__"


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Organization
        fields = "__all__"
