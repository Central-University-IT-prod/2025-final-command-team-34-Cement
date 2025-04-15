from rest_framework import serializers

from .models import Tag


class TagSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Tag
        fields = ['id', 'name']


class ListTagSerializer(serializers.Serializer):
    tags = TagSerializer(many=True)
