from rest_framework import serializers
from .models import Insumo


class InsumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insumo
        fields = ("name", "machine")