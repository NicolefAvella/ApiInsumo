from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Insumos


class InsumosSerializer(serializers.ModelSerializer):

    class Meta:
        model = Insumos
        fields = ("name", "machine")

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.machine = validated_data.get("machine", instance.machine)
        instance.save()
        return instance

class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)   


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email")     

