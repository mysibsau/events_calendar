from itertools import chain

from rest_framework import serializers

from apps.events import models
from apps.user.models import User, UserRole


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
    author_name = serializers.SerializerMethodField(method_name='get_author_full_name')
    author_id = serializers.SerializerMethodField(method_name='get_author_id')

    def get_author_full_name(self, obj):
        return str(obj.author.first_name)

    def get_author_id(self, obj):
        return obj.author.id

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


class EventGroupSerializer(serializers.ModelSerializer):
    events = EventDetailSerializer(many=True, read_only=True)
    events_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data: dict):
        events_ids = validated_data.pop("events_ids", None)
        group = models.EventGroup.objects.create(**validated_data)
        for event_id in events_ids:
            event = models.Event.objects.filter(id=event_id).first()
            if event.group is None:
                event.group = group
                event.save()

        return group

    def update(self, instance: models.EventGroup, validated_data: dict):
        old_events = models.Event.objects.all().filter(group=instance)
        new_events_ids = validated_data.pop("events_ids", None)

        for event in old_events:
            event.group = None
            event.save()

        for event_id in new_events_ids:
            event = models.Event.objects.filter(id=event_id).first()
            event.group = instance
            event.save()

        return super().update(instance, validated_data)

    class Meta:
        model = models.EventGroup
        fields = "__all__"

