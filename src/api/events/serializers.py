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


class ImportantDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ImportantDate
        fields = ("name", "date")


class EventSerializer(serializers.ModelSerializer):
    # TODO: Эта дичь может возвращать none, нужно пофиксить
    is_verified = serializers.BooleanField(read_only=True, source="verified")
    important_dates = ImportantDateSerializer(many=True, read_only=True)
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


class EventDetailSerializer(serializers.ModelSerializer):
    verified = serializers.StringRelatedField(source="verified.first_name", read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    can_edit = serializers.BooleanField(read_only=True, label="Может ли данный пользователь редактировать мероприятие")
    important_dates = ImportantDateSerializer(many=True, required=False)
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.CharField(read_only=True)
    verified_date = serializers.DateTimeField(read_only=True)

    def create(self, validated_data: dict):
        important_dates = validated_data.pop("important_dates", None)
        event = models.Event.objects.create(**validated_data)
        important_dates = [{**dates, "event": event} for dates in important_dates]
        if ImportantDateSerializer(data=important_dates, many=True).is_valid(raise_exception=True):
            for date in important_dates:
                models.ImportantDate.objects.create(**date)
        return event

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
