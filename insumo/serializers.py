from rest_framework import serializers
from .models import Insumo


class InsumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insumo
        fields = ("name", "machine")

class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)        