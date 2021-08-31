from django.db.models import fields
from rest_framework import serializers, fields

from . import models


class EventSerializer(serializers.ModelSerializer):
    # TODO: Эта дичь может возвращать none, нужно пофиксить
    is_verified = serializers.BooleanField(read_only=True, source='verified')

    class Meta:
        model = models.Event
        fields = ('id', 'name', 'start_date', 'stop_date', 'is_verified')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        read_only=True,
        label='Id автора'
    )
    author_name = serializers.CharField(
        source='author.first_name',
        read_only=True,
        label='Имя отчество автора',
        allow_blank=True,
    )
    text = serializers.CharField(allow_blank=False)

    class Meta:
        model = models.Comment
        fields = ('id', 'author', 'author_name', 'text', 'event', 'date')


class EventDetailSerializer(serializers.ModelSerializer):
    responsible = serializers.CharField(read_only=True)
    verified = serializers.StringRelatedField(source='verified.first_name', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    can_edit = serializers.BooleanField(read_only=True, label='Может ли данный пользователь редактировать мероприятие')

    class Meta:
        model = models.Event
        fields = '__all__'


class DirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Direction
        fields = '__all__'


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Level
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = '__all__'


class FormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Format
        fields = '__all__'


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Organization
        fields = '__all__'
