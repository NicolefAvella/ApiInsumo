from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from .models import Insumo
from .serializers import InsumoSerializer


class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_insumo(name="", machine=""):
        if name != "" and machine != "":
            Insumo.objects.create(name=name, machine=machine)

    def setUp(self):
        # Datos prueba para test
        self.create_insumo("retendeor", "rectilinea")
        self.create_insumo("rueda", "rectilinea")
        self.create_insumo("depillo", "lavadora")
        self.create_insumo("potenciometro", "mesa corte")


class GetInsumosTest(BaseViewTest):
	

    def test_get_all_insumos(self):
        """
        This test ensures that all insumos added in the setUp method
        exist when we make a GET request to the insumos/ endpoint
        """
        response = self.client.get(
            reverse("insumos-all")
        )
        

        expected = insumos.objects.all()
        serialized = insumosSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
