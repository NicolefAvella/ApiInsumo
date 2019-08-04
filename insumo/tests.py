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

    def make_a_request(self, kind="post", **kwargs):

        if kind == "post":
            return self.client.post(
                reverse("insumos-list-create"
            ),
            content_type="application/json"
        )

        elif kind == "put":
            return self.client.put(
                reverse(
                    "insumos-detail",
                    kwargs={
                        "pk": kwargs["id"]
                    }
                ),
            data=json.dumps(kwargs["data"]),
            content_type="application/json"
            )
        else:
             return None

    def retrieve_insumo(self, pk=0):
        return self.client.get(
            reverse(
                "insumos-detail",
                kwargs ={
                    "pk": pk
                }
            )
        )

    def delete_insumo(self, pk=0):
        return self.client.delete(
            reverse(
                "insumos-detail",
                kwargs ={
                    "pk": pk
                }
            )
        )



    def login_a_user(self, username="", password=""):
        url = reverse("auth-login")

        return self.client.post(
            url,
            data=json.dumps({
                "username": username,
                "password": password
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
                "auth-register"
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

        self.valid_data = {
            "name": "test name",
            "machine" : "test machine"
        }

        self.valid_data = {
            "name": "",
            "machine" : ""
        }

        self.valid_insumo_id = 1
        self.invalid_insumo_id = 1000000


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

class GetSingleInsumoTest(BaseViewTest):

	def test_get_insumo(self):
		"""Test un insumo es devuelto por id"""
        self.login_client("test_user", "test123")

        response = self.retrieve_insumo(self.valid_insumo_id)
        expected = Insumos.objects.get(pk=self.valid_insumo_id)
        serialized = InsumosSerializer(expected)

        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.retrieve_insumo(self.invalid_insumo_id)
        self.assertEqual(
        	response.data["message"],
        	"No existe insumo con ese id"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class AddInsumosTest(BaseViewTest):

    def test_create_insumo(self):
        """Test verifica insumo es creado"""
        self.login_client('test_user', 'test123')

        response = self.make_a_request(
            kind="post",
            data=self.valid_data
        )
        self.assertEqual(response.data, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # test con datos no validos
        response = self.make_a_request(
            kind="post",
            data=self.invalid_data
        )
        self.assertEqual(
            response.data["message"],
            "No pueden existir campos vacios"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateInsumosTest(BaseViewTest):

    def test_update_a_song(self):
        """Test actualizar insumo"""

        self.login_client('test_user', 'test123')

        response = self.make_a_request(
            kind="put",
            id=2,
            data=self.valid_data
        )
        self.assertEqual(response.data, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.make_a_request(
            kind="put",
            id=3,
            data=self.invalid_data
        )
        self.assertEqual(
            response.data["message"],
            "No pueden existir campos vacios"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSongsTest(BaseViewTest):

    def test_delete_a_song(self):
        """Test borrar insumo """

        self.login_client('test_user', 'test123')

        response = self.delete_a_song(1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.delete_a_song(100)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



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
