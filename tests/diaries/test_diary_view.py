from rest_framework.test import APITestCase
from rest_framework.views import status
from users.models import User

class DiaryViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):

        super_user_data = {
            "username": "maite_kenzie",
            "email": "maite@kenzie.com",
            "first_name": "Maite",
            "last_name": "Kenzie",
            "password": "1234",
            "is_adm": "True"
        }

        common_user_data = {
            "username": "catarina_kenzie",
            "email": "catarina@kenzie.com",
            "first_name": "Catarina",
            "last_name": "Kenzie",
            "password": "1234"
        }

        cls.super_user = User.objects.create_superuser(**super_user_data)
        cls.common_user = User.objects.create_user(**common_user_data)

        cls.base_url = "/diaries/"

    def test_create_diary_with_valid_token(self):
        diary_data = {"name": "Diário da Maite"}

        login_response = self.client.post("/login/", {"username": "maite_kenzie", "password": "1234"}, format="json")

        admin_token = login_response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + admin_token)

        response = self.client.post(self.base_url, data=diary_data, format="json")

        # Verificando a resposta retornada:

        expected_keys = {"id", "name", "created_at", "user_id"}

        returned_keys = set(response.json().keys())

        msg = "Verifique se a resposta contem todos os campos esperados" 
    
        self.assertSetEqual(expected_keys, returned_keys, msg)

        # Verificando o status code retornado na resposta:

        expected_status_code = status.HTTP_201_CREATED

        returned_status_code = response.status_code

        msg = f"Verifique se o status code retornado é {expected_status_code}"
        
        self.assertEqual(expected_status_code, returned_status_code, msg)

    def test_create_diary_without_authentication(self):
        diary_data = {"name": "Diário da Maite"}

        response = self.client.post(self.base_url, data=diary_data, format="json")

        # Verificando a resposta retornada:

        expected_data = {"detail": "Authentication credentials were not provided."}

        returned_data: dict = response.json()
        
        msg = f"A resposta precisa informar que autenticação é necessária"

        self.assertDictEqual(expected_data, returned_data, msg)

        # Verificando o status code retornado na resposta:

        expected_status_code = status.HTTP_401_UNAUTHORIZED

        returned_status_code = response.status_code

        msg = f"Verifique se o status code retornado é {expected_status_code}"

        self.assertEqual(expected_status_code, returned_status_code, msg)

    def test_create_diary_with_missing_data(self):
        diary_data = {}

        login_response = self.client.post("/login/", {"username": "maite_kenzie", "password": "1234"}, format="json")

        admin_token = login_response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + admin_token)

        response = self.client.post(self.base_url, data=diary_data, format="json")

        # Verificando a resposta retornada:

        expected_data = {"name": ["This field is required."]}

        returned_data: dict = response.json()
        
        msg = f"A resposta retornada precisa indiciar que faltou passar o name no body da requisição"

        self.assertDictEqual(expected_data, returned_data, msg)

        # Verificando o status code retornado na resposta:

        expected_status_code = status.HTTP_400_BAD_REQUEST

        returned_status_code = response.status_code

        msg = f"Verifique se o status code retornado é {expected_status_code}"

        self.assertEqual(expected_status_code, returned_status_code, msg)

    def test_listing_diary_with_valid_token(self):
        first_diary_data = {"name": "Primeiro Diário da Maite"}
        second_diary_data = {"name": "Segundo Diário da Maite"}

        login_response = self.client.post("/login/", {"username": "maite_kenzie", "password": "1234"}, format="json")

        admin_token = login_response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + admin_token)

        first_diary = self.client.post(self.base_url, data=first_diary_data, format="json")
        second_diary = self.client.post(self.base_url, data=second_diary_data, format="json")

        get_response = self.client.get(self.base_url, format="json")

        # Verificando a resposta retornada:

        expected_data = 2

        returned_data: int = get_response.json()["count"]
        
        msg = f"Usuários autenticados devem conseguir listar os seus dois diários criados"

        self.assertEqual(expected_data, returned_data, msg)

        # Verificando o status code retornado na resposta:

        expected_status_code = status.HTTP_200_OK

        returned_status_code = get_response.status_code

        msg = f"Verifique se o status code retornado é {expected_status_code}"

        self.assertEqual(expected_status_code, returned_status_code, msg)

    def test_listing_diary_without_authentication(self):

        get_response = self.client.get(self.base_url, format="json")

        # Verificando a resposta retornada:

        expected_data = {"detail": "Authentication credentials were not provided."}

        returned_data: dict = get_response.json()
        
        msg = f"A resposta precisa informar que autenticação é necessária"

        self.assertDictEqual(expected_data, returned_data, msg)

        # Verificando o status code retornado na resposta:

        expected_status_code = status.HTTP_401_UNAUTHORIZED

        returned_status_code = get_response.status_code

        msg = f"Verifique se o status code retornado é {expected_status_code}"

        self.assertEqual(expected_status_code, returned_status_code, msg)