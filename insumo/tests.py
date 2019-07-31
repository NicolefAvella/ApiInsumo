import json
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from .models import Insumo
from .serializers import InsumoSerializer

from django.contrib.auth.models import User

class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_insumo(name="", machine=""):
        if name != "" and machine != "":
            Insumo.objects.create(name=name, machine=machine)

    def login_client(self, username="", password=""):
        # get a token from DRF
        response = self.client.post(
            reverse('create-token'),
            data=json.dumps(
                {
                    'username': username,
                    'password': password
                }
            ),
            content_type='application/json'
        )
        self.token = response.data['token']
        # set the token in the header
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.token
        )
        self.client.login(username=username, password=password)
        return self.token    



    def login_a_user(self, username="", password=""):
        url = reverse(
            "auth-login",
        )
        return self.client.post(
            url,
            data=json.dumps({
                "username": username,
                "password": password
            }),
            content_type="application/json"
        ) 


    def register_a_user(self, username="", password="", email=""):
        return self.client.post(
            reverse(
                "auth-register",
            ),
            data=json.dumps(
                {
                    "username": username,
                    "password": password,
                    "email": email
                }
            ),
            content_type='application/json'
        )       

    def setUp(self):

        # Datos para creacion super usuario
        self.user = User.objects.create_superuser(
            username="test_user",
            email="test@gmail.com",
            password="test123",
            first_name="test",
            last_name="user",
        )

        # Datos prueba para test obtener todos los insumos
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
        self.login_client('test_user', 'testing')

        response = self.client.get(
            reverse("insumos-all")
        )
        

        expected = Insumo.objects.all()
        serialized = InsumoSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AuthLoginUserTest(BaseViewTest):
    """ Tests for the auth/login """

    def test_login_user_with_valid_credentials(self):
        # test login with valid credentials
        response = self.login_a_user("test_user", "testing")
        # assert token key exists
        self.assertIn("token", response.data)
        # assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # test login with invalid credentials
        response = self.login_a_user("anonymous", "pass")
        # assert status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)