from rest_framework import generics
from .models import Insumo
from .serializers import InsumoSerializer


class ListInsumosView(generics.ListAPIView):

    queryset = Insumo.objects.all()
    serializer_class = InsumoSerializer