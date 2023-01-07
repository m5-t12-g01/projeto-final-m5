from rest_framework.test import APITestCase
from rest_framework.views import status
from users.models import User

class LoginViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.base_url = "/api/login/"

    def test_login_success(self):
        user_data = {
            "username": "maite_kenzie",
            "email": "maite@kenzie.com",
            "first_name": "Maite",
            "last_name": "Kenzie",
            "password": "1234",
            "is_adm": "True"
        }

        User.objects.create_superuser(**user_data) # Criação de usuário

        login_data = {
            "username": "maite_kenzie",
            "password": "1234",
        }

        response = self.client.post(self.base_url, data=login_data, format="json") # Resposta do login de usuário 

        # Verificando a resposta retornada:

        expected_keys = {"access", "refresh"}

        returned_keys = set(response.json().keys())

        msg = f"Verifique se os tokens de acesso e refresh estão sendo retornados corretamente na rota {self.base_url}"

        self.assertSetEqual(expected_keys, returned_keys, msg)

        # Verificando o status code retornado na resposta:

        expected_status_code = status.HTTP_200_OK

        returned_status_code = response.status_code

        msg = f"Verifique se o status code retornado é {expected_status_code}"

        self.assertEqual(expected_status_code, returned_status_code, msg)

    def test_login_wrong_data(self):
        login_data = {
            "username": "wrong_user",
            "password": "1234",
        }

        response = self.client.post(self.base_url, data=login_data, format="json")

        # Verificando a resposta retornada:

        expected_data = {"detail": "No active account found with the given credentials"}

        returned_data: dict = response.json()
        
        msg = f"A resposta retornada ao tentar logar com credenciais inválidas precisa ser {expected_data}"

        self.assertDictEqual(expected_data, returned_data, msg)

        # Verificando o status code retornado na resposta:

        expected_status_code = status.HTTP_401_UNAUTHORIZED

        returned_status_code = response.status_code

        msg = f"Verifique se o status code retornado é {expected_status_code}"
        

        self.assertEqual(expected_status_code, returned_status_code, msg)

    def test_login_missing_data(self):
        login_data = {
            "username": "missing_user",
        }

        response = self.client.post(self.base_url, data=login_data, format="json")

        # Verificando a resposta retornada:

        expected_data = {"password": ["This field is required."]}

        returned_data: dict = response.json()
        
        msg = f"A resposta retornada precisa indiciar que faltou passar o password no body da requisição"

        self.assertDictEqual(expected_data, returned_data, msg)

        # Verificando o status code retornado na resposta:

        expected_status_code = status.HTTP_400_BAD_REQUEST

        returned_status_code = response.status_code

        msg = f"Verifique se o status code retornado é {expected_status_code}"

        self.assertEqual(expected_status_code, returned_status_code, msg)
    


    