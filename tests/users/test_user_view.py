from rest_framework.test import APITestCase
from rest_framework.views import status
from users.models import User

class UserViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.base_url = "/api/users/"

    def test_admin_user_creation(self):
        user_data = {
            "username": "maite_kenzie",
            "email": "maite@kenzie.com",
            "first_name": "Maite",
            "last_name": "Kenzie",
            "password": "1234",
            "is_adm": "True"
        }

        response = self.client.post(self.base_url, data=user_data, format="json")

        # Verificando a resposta retornada:

        expected_keys = {"id", "is_superuser", "username", "email", "first_name", "last_name", "is_adm"}

        returned_keys = set(response.json().keys())

        msg = "Verifique se a resposta contem todos os campos esperados" 
        admin_msg = "Os campos is_superuser e is_adm precisam ser True"

        self.assertSetEqual(expected_keys, returned_keys, msg)
        self.assertTrue(response.json()['is_superuser'], admin_msg)
        self.assertTrue(response.json()['is_adm'], admin_msg)

        # Verificando o status code retornado na resposta:

        expected_status_code = status.HTTP_201_CREATED

        returned_status_code = response.status_code

        msg = f"Verifique se o status code retornado é POST - {expected_status_code}"
        
        self.assertEqual(expected_status_code, returned_status_code, msg)

    def test_common_user_creation(self):
        user_data = {
            "username": "catarina_kenzie",
            "email": "catarina@kenzie.com",
            "first_name": "Catarina",
            "last_name": "Kenzie",
            "password": "1234"
        }

        response = self.client.post(self.base_url, data=user_data, format="json")

        # Verificando a resposta retornada:

        expected_keys = {"id", "is_superuser", "username", "email", "first_name", "last_name", "is_adm"}

        returned_keys = set(response.json().keys())

        msg = "Verifique se a resposta contem todos os campos esperados" 
        admin_msg = "Os campos is_superuser e is_adm precisam ser False"

        self.assertSetEqual(expected_keys, returned_keys, msg)
        self.assertFalse(response.json()['is_superuser'], admin_msg)
        self.assertFalse(response.json()['is_adm'], admin_msg)

        # Verificando o status code retornado na resposta:

        expected_status_code = status.HTTP_201_CREATED

        returned_status_code = response.status_code

        msg = f"Verifique se o status code retornado é POST - {expected_status_code}"
        
        self.assertEqual(expected_status_code, returned_status_code, msg)



    