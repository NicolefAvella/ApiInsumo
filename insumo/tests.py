import json
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from .models import Insumos
from .serializers import InsumosSerializer


class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_insumo(name="", machine=""):
        if name != "" and machine != "":
            Insumos.objects.create(name=name, machine=machine)

    def login_a_user(self, username="", password=""):
        url = reverse("auth-login")

        return self.client.post(
            url,
            data=json.dumps({
                "username": username,
                "password": password,
            }),
            content_type="application/json"
        )

    def login_client(self, username="", password=""):
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
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.token
        )
        self.client.login(username=username, password=password)
        return self.token    


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

        # Datos prueba para test obtener todos los Insumoss
        self.create_insumo("retendeor", "rectilinea")
        self.create_insumo("rueda", "rectilinea")
        self.create_insumo("cepillo", "lavadora")
        self.create_insumo("potenciometro", "mesa corte")


class GetInsumosTest(BaseViewTest):

    def test_get_all_insumos(self):

        self.login_client('test_user', 'test123')

        response = self.client.get(
            reverse("insumos-all")
        )
        

        expected = Insumos.objects.all()
        serialized = InsumosSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AuthLoginUserTest(BaseViewTest):
    """ Tests for the auth/login """

    def test_login_user_with_valid_credentials(self):
        # test login with valid credentials
        response = self.login_a_user("test_user", "test123")
        self.assertIn("token", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.login_a_user("anonymous", "pass")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class AuthRegisterUserTest(BaseViewTest):

    def test_register_a_user(self):
        response = self.register_a_user("nuevo_usuario", "test123", "test@gmail.com")

        self.assertEqual(response.data["username"], "nuevo_usuario")
        self.assertEqual(response.data["email"], "test@gmail.com")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test con datos invalidos
        response = self.register_a_user()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)