from rest_framework.test import APITestCase
from rest_framework.views import status
from users.models import User

class UserDetailViewTest(APITestCase):
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

        cls.base_url = "/users/"
        cls.admin_url = f"/users/{cls.super_user.id}/"
        cls.common_url = f"/users/{cls.common_user.id}/"

    def test_retrieve_another_user_data_with_admin_token(self):
        login_response = self.client.post("/login/", {"username": "maite_kenzie", "password": "1234"}, format="json")

        admin_token = login_response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + admin_token)

        response = self.client.get(self.common_url, format="json")

        # Verificando a resposta retornada:

        expected_keys = {"id", "is_superuser", "username", "email", "first_name", "last_name", "is_adm"}

        returned_keys = set(response.json().keys())

        msg = "Verifique se a resposta contem todos os campos esperados" 
    
        self.assertSetEqual(expected_keys, returned_keys, msg)

        # Verificando o status code retornado na resposta:

        expected_status_code = status.HTTP_200_OK

        returned_status_code = response.status_code

        msg = f"Verifique se o status code retornado é {expected_status_code}"
        
        self.assertEqual(expected_status_code, returned_status_code, msg)

    def test_retrieve_another_user_data_with_common_token(self):
        login_response = self.client.post("/login/", {"username": "catarina_kenzie", "password": "1234"}, format="json")

        common_token = login_response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + common_token)

        response = self.client.get(self.admin_url, format="json")

        # Verificando a resposta retornada:

        expected_data = {"detail": "You do not have permission to perform this action."}

        returned_data: dict = response.json()

        msg = "A resposta retornada precisa indiciar que o usuário não tem permissão" 
    
        self.assertDictEqual(expected_data, returned_data, msg)

        # Verificando o status code retornado na resposta:

        expected_status_code = status.HTTP_403_FORBIDDEN

        returned_status_code = response.status_code

        msg = f"Verifique se o status code retornado é {expected_status_code}"
        
        self.assertEqual(expected_status_code, returned_status_code, msg)

    def test_retrieve_owner_user_data_with_common_token(self):
        login_response = self.client.post("/login/", {"username": "catarina_kenzie", "password": "1234"}, format="json")

        common_token = login_response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + common_token)

        response = self.client.get(self.common_url, format="json")

        # Verificando a resposta retornada:

        expected_keys = {"id", "is_superuser", "username", "email", "first_name", "last_name", "is_adm"}

        returned_keys = set(response.json().keys())

        msg = "Verifique se a resposta contem todos os campos esperados" 
    
        self.assertSetEqual(expected_keys, returned_keys, msg)

        # Verificando o status code retornado na resposta:

        expected_status_code = status.HTTP_200_OK

        returned_status_code = response.status_code

        msg = f"Verifique se o status code retornado é {expected_status_code}"
        
        self.assertEqual(expected_status_code, returned_status_code, msg)

    def test_retrieve_user_without_authentication(self):
        response = self.client.get(self.admin_url, format="json")

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

    def test_retrieve_user_with_invalid_id(self):
        login_response = self.client.post("/login/", {"username": "maite_kenzie", "password": "1234"}, format="json")

        admin_token = login_response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + admin_token)

        response = self.client.get(f"{self.base_url}407e8394-2e52-4924-aab2-047f73447eff/", format="json")

        # Verificando a resposta retornada:

        expected_data = {"detail": "Not found."}

        returned_data: dict = response.json()
        
        msg = f"A resposta precisa informar que não foi encontrado usuário com o id passado na url"

        self.assertDictEqual(expected_data, returned_data, msg)

        # Verificando o status code retornado na resposta:

        expected_status_code = status.HTTP_404_NOT_FOUND

        returned_status_code = response.status_code

        msg = f"Verifique se o status code retornado é {expected_status_code}"

        self.assertEqual(expected_status_code, returned_status_code, msg)

    def test_update_another_user_data_with_admin_token(self):
        update_data = {"username": "catarina_editada"}

        login_response = self.client.post("/login/", {"username": "maite_kenzie", "password": "1234"}, format="json")

        admin_token = login_response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + admin_token)

        response = self.client.patch(self.common_url, data=update_data, format="json")

        # Verificando a resposta retornada:

        expected_data = "catarina_editada"

        returned_data = response.json()["username"]

        msg = "O administrador precisa conseguir atualizar o username de outros usuários" 
    
        self.assertEqual(expected_data, returned_data, msg)

        # Verificando o status code retornado na resposta:

        expected_status_code = status.HTTP_200_OK

        returned_status_code = response.status_code

        msg = f"Verifique se o status code retornado é {expected_status_code}"
        
        self.assertEqual(expected_status_code, returned_status_code, msg)

    def test_update_another_user_data_with_common_token(self):
        update_data = {"username": "maite_editada"}

        login_response = self.client.post("/login/", {"username": "catarina_kenzie", "password": "1234"}, format="json")

        common_token = login_response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + common_token)

        response = self.client.patch(self.admin_url, data=update_data, format="json")

        # Verificando a resposta retornada:

        expected_data = {"detail": "You do not have permission to perform this action."}

        returned_data: dict = response.json()

        msg = "A resposta retornada precisa indiciar que o usuário não tem permissão" 
    
        self.assertDictEqual(expected_data, returned_data, msg)

        # Verificando o status code retornado na resposta:

        expected_status_code = status.HTTP_403_FORBIDDEN

        returned_status_code = response.status_code

        msg = f"Verifique se o status code retornado é {expected_status_code}"
        
        self.assertEqual(expected_status_code, returned_status_code, msg)

    def test_update_owner_user_data_with_common_token(self):
        update_data = {"username": "catarina_editada"}

        login_response = self.client.post("/login/", {"username": "catarina_kenzie", "password": "1234"}, format="json")

        common_token = login_response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + common_token)

        response = self.client.patch(self.common_url, data=update_data, format="json")

        # Verificando a resposta retornada:

        expected_data = "catarina_editada"

        returned_data = response.json()["username"]

        msg = "O usuário autenticado precisa conseguir atualizar seu próprio username" 
    
        self.assertEqual(expected_data, returned_data, msg)

        # Verificando o status code retornado na resposta:

        expected_status_code = status.HTTP_200_OK

        returned_status_code = response.status_code

        msg = f"Verifique se o status code retornado é {expected_status_code}"
        
        self.assertEqual(expected_status_code, returned_status_code, msg)

    def test_update_user_without_authentication(self):
        update_data = {"username": "catarina_editada"}

        response = self.client.patch(self.common_url, data=update_data, format="json")

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

    def test_update_user_with_invalid_id(self):
        update_data = {"username": "catarina_editada"}

        login_response = self.client.post("/login/", {"username": "maite_kenzie", "password": "1234"}, format="json")

        admin_token = login_response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + admin_token)

        response = self.client.patch(f"{self.base_url}407e8394-2e52-4924-aab2-047f73447eff/", data=update_data, format="json")

        # Verificando a resposta retornada:

        expected_data = {"detail": "Not found."}

        returned_data: dict = response.json()
        
        msg = f"A resposta precisa informar que não foi encontrado usuário com o id passado na url"

        self.assertDictEqual(expected_data, returned_data, msg)

        # Verificando o status code retornado na resposta:

        expected_status_code = status.HTTP_404_NOT_FOUND

        returned_status_code = response.status_code

        msg = f"Verifique se o status code retornado é {expected_status_code}"

        self.assertEqual(expected_status_code, returned_status_code, msg)

    def test_delete_another_user_data_with_admin_token(self):
        login_response = self.client.post("/login/", {"username": "maite_kenzie", "password": "1234"}, format="json")

        admin_token = login_response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + admin_token)

        response = self.client.delete(self.common_url, format="json")

        # Verificando o status code retornado na resposta:

        expected_status_code = status.HTTP_204_NO_CONTENT

        returned_status_code = response.status_code

        msg = f"Verifique se o status code retornado é {expected_status_code}"
        
        self.assertEqual(expected_status_code, returned_status_code, msg)

    def test_delete_another_user_data_with_common_token(self):
        login_response = self.client.post("/login/", {"username": "catarina_kenzie", "password": "1234"}, format="json")

        common_token = login_response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + common_token)

        response = self.client.delete(self.admin_url, format="json")

        # Verificando a resposta retornada:

        expected_data = {"detail": "You do not have permission to perform this action."}

        returned_data: dict = response.json()

        msg = "A resposta retornada precisa indiciar que o usuário não tem permissão" 
    
        self.assertDictEqual(expected_data, returned_data, msg)

        # Verificando o status code retornado na resposta:

        expected_status_code = status.HTTP_403_FORBIDDEN

        returned_status_code = response.status_code

        msg = f"Verifique se o status code retornado é {expected_status_code}"
        
        self.assertEqual(expected_status_code, returned_status_code, msg)

    def test_delete_owner_user_data_with_common_token(self):
        login_response = self.client.post("/login/", {"username": "catarina_kenzie", "password": "1234"}, format="json")

        common_token = login_response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + common_token)

        response = self.client.delete(self.common_url, format="json")

        # Verificando o status code retornado na resposta:

        expected_status_code = status.HTTP_204_NO_CONTENT

        returned_status_code = response.status_code

        msg = f"Verifique se o status code retornado é {expected_status_code}"
        
        self.assertEqual(expected_status_code, returned_status_code, msg)

    def test_delete_user_without_authentication(self):
        response = self.client.delete(self.common_url, format="json")

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

    def test_delete_user_with_invalid_id(self):
        login_response = self.client.post("/login/", {"username": "maite_kenzie", "password": "1234"}, format="json")

        admin_token = login_response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + admin_token)

        response = self.client.delete(f"{self.base_url}407e8394-2e52-4924-aab2-047f73447eff/", format="json")

        # Verificando a resposta retornada:

        expected_data = {"detail": "Not found."}

        returned_data: dict = response.json()
        
        msg = f"A resposta precisa informar que não foi encontrado usuário com o id passado na url"

        self.assertDictEqual(expected_data, returned_data, msg)

        # Verificando o status code retornado na resposta:

        expected_status_code = status.HTTP_404_NOT_FOUND

        returned_status_code = response.status_code

        msg = f"Verifique se o status code retornado é {expected_status_code}"

        self.assertEqual(expected_status_code, returned_status_code, msg)