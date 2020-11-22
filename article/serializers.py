from rest_framework import serializers

from .models import Download


class DownloadSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    jsonData = serializers.CharField()
    created_at = serializers.CharField()

    def create(self, validated_data):
        return Download.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.jsonData = validated_data.get('jsonData', instance.jsonData)
        instance.id = validated_data.get('id', instance.id)
        instance.save()
        return instance


class DownloadSerializer2(serializers.Serializer):
    jsonData = serializers.CharField()

    def create(self, validated_data):
        return Download.objects.create(**validated_data)

