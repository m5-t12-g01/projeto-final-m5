from rest_framework.test import APITestCase
from rest_framework.views import status

class UserViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.base_url = "/users/"

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

        msg = f"Verifique se o status code retornado é {expected_status_code}"
        
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

        msg = f"Verifique se o status code retornado é {expected_status_code}"
        
        self.assertEqual(expected_status_code, returned_status_code, msg)

    def test_username_and_email_uniqueness(self):
        user_data = {
            "username": "maite_kenzie",
            "email": "maite@kenzie.com",
            "first_name": "Maite",
            "last_name": "Kenzie",
            "password": "1234",
            "is_adm": "True"
        }

        response = self.client.post(self.base_url, data=user_data, format="json")
        second_response = self.client.post(self.base_url, data=user_data, format="json")

        # Verificando a resposta retornada:

        expected_data = {"username": ["A user with that username already exists."], "email": ["A user with this email already exists."]}

        returned_data: dict = second_response.json()
        
        msg = f"A resposta retornada precisa indiciar que o username e o email já existem"

        self.assertDictEqual(expected_data, returned_data, msg)

        # Verificando o status code retornado na resposta:

        expected_status_code = status.HTTP_400_BAD_REQUEST

        returned_status_code = second_response.status_code

        msg = f"Verifique se o status code retornado é {expected_status_code}"
    
        self.assertEqual(expected_status_code, returned_status_code, msg)

    def test_user_creation_with_missing_data(self):
        user_data = {
            "username": "maite_kenzie",
            "email": "maite@kenzie.com",
        }

        response = self.client.post(self.base_url, data=user_data, format="json")

        # Verificando a resposta retornada:

        expected_data = {"password": ["This field is required."], "first_name": ["This field is required."], "last_name": ["This field is required."]}

        returned_data: dict = response.json()
        
        msg = f"A resposta retornada precisa indiciar que faltou passar o password, o first_name e o last_name no body da requisição"

        self.assertDictEqual(expected_data, returned_data, msg)

        # Verificando o status code retornado na resposta:

        expected_status_code = status.HTTP_400_BAD_REQUEST

        returned_status_code = response.status_code

        msg = f"Verifique se o status code retornado é {expected_status_code}"

        self.assertEqual(expected_status_code, returned_status_code, msg)

    def test_listing_with_super_user(self):
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

        super_user = self.client.post(self.base_url, data=super_user_data, format="json")
        common_user = self.client.post(self.base_url, data=common_user_data, format="json")
        login_response = self.client.post("/login/", {"username": "maite_kenzie", "password": "1234"}, format="json")

        token = login_response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

        get_response = self.client.get(self.base_url, format="json")

        # Verificando a resposta retornada:

        expected_data = 2

        returned_data: int = get_response.json()["count"]
        
        msg = f"Usuários administradores devem conseguir listar os dois usuários criados"

        self.assertEqual(expected_data, returned_data, msg)

        # Verificando o status code retornado na resposta:

        expected_status_code = status.HTTP_200_OK

        returned_status_code = get_response.status_code

        msg = f"Verifique se o status code retornado é {expected_status_code}"

        self.assertEqual(expected_status_code, returned_status_code, msg)

    def test_listing_with_common_user(self):
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

        super_user = self.client.post(self.base_url, data=super_user_data, format="json")
        common_user = self.client.post(self.base_url, data=common_user_data, format="json")
        login_response = self.client.post("/login/", {"username": "catarina_kenzie", "password": "1234"}, format="json")

        token = login_response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

        get_response = self.client.get(self.base_url, format="json")

        # Verificando a resposta retornada:

        expected_data = {"detail": "You do not have permission to perform this action."}

        returned_data: dict = get_response.json()
        
        msg = f"Usuários comuns não devem conseguir acessar a rota de listagem"

        self.assertDictEqual(expected_data, returned_data, msg)

        # Verificando o status code retornado na resposta:

        expected_status_code = status.HTTP_403_FORBIDDEN

        returned_status_code = get_response.status_code

        msg = f"Verifique se o status code retornado é {expected_status_code}"

        self.assertEqual(expected_status_code, returned_status_code, msg)

    def test_listing_without_authentication(self):
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

        super_user = self.client.post(self.base_url, data=super_user_data, format="json")
        common_user = self.client.post(self.base_url, data=common_user_data, format="json")

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
        






    