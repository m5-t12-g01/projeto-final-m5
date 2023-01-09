from rest_framework.test import APITestCase
from rest_framework.views import status
from users.models import User
from diaries.models import Diary

class NoteViewTest(APITestCase):
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

        super_diary_data = {
            "name": "Diário da Maite"
        }

        common_diary_data = {
            "name": "Diário da Catarina"
        }

        cls.super_user = User.objects.create_superuser(**super_user_data)
        cls.common_user = User.objects.create_user(**common_user_data)

        cls.super_diary = Diary.objects.create(**super_diary_data, user=cls.super_user)
        cls.common_diary = Diary.objects.create(**common_diary_data, user=cls.common_user)

        cls.admin_url = f"/diaries/{cls.super_diary.id}/notes/"
        cls.common_url = f"/diaries/{cls.common_diary.id}/notes/"

    def test_create_note_with_valid_token(self):
        note_data = {
            "title": "Anotação da Maite",
            "description": "Descrição da anotação da Maite",
            "priority": 1 
        }

        login_response = self.client.post("/login/", {"username": "maite_kenzie", "password": "1234"}, format="json")

        admin_token = login_response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + admin_token)

        response = self.client.post(self.admin_url, data=note_data, format="json")

        # Verificando a resposta retornada:

        expected_keys = {"id", "title", "description", "priority", "diary_id"}

        returned_keys = set(response.json().keys())

        msg = "Verifique se a resposta contem todos os campos esperados" 
    
        self.assertSetEqual(expected_keys, returned_keys, msg)

        # Verificando o status code retornado na resposta:

        expected_status_code = status.HTTP_201_CREATED

        returned_status_code = response.status_code

        msg = f"Verifique se o status code retornado é {expected_status_code}"
        
        self.assertEqual(expected_status_code, returned_status_code, msg)

    def test_create_note_for_another_user(self):
        note_data = {
            "title": "Anotação da Catarina",
            "description": "Descrição da anotação da Catarina",
            "priority": 1 
        }

        login_response = self.client.post("/login/", {"username": "maite_kenzie", "password": "1234"}, format="json")

        admin_token = login_response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + admin_token)

        response = self.client.post(self.common_url, data=note_data, format="json")

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

    def test_create_note_without_authentication(self):
        note_data = {
            "title": "Anotação da Maite",
            "description": "Descrição da anotação da Maite",
            "priority": 1 
        }

        response = self.client.post(self.admin_url, data=note_data, format="json")

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

    def test_create_note_with_missing_data(self):
        note_data = {
            "title": "Anotação da Maite",
        }

        login_response = self.client.post("/login/", {"username": "maite_kenzie", "password": "1234"}, format="json")

        admin_token = login_response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + admin_token)

        response = self.client.post(self.admin_url, data=note_data, format="json")

        # Verificando a resposta retornada:

        expected_data = {"description": ["This field is required."]}

        returned_data: dict = response.json()
        
        msg = f"A resposta retornada precisa indiciar que faltou passar a description no body da requisição"

        self.assertDictEqual(expected_data, returned_data, msg)

        # Verificando o status code retornado na resposta:

        expected_status_code = status.HTTP_400_BAD_REQUEST

        returned_status_code = response.status_code

        msg = f"Verifique se o status code retornado é {expected_status_code}"

        self.assertEqual(expected_status_code, returned_status_code, msg)

    def test_listing_notes_with_valid_token(self):
        first_note_data = {
            "title": "Primeiira Anotação da Maite",
            "description": "Descrição da primeira anotação da Maite",
            "priority": 1 
        }

        second_note_data = {
            "title": "Segunda Anotação da Maite",
            "description": "Descrição da segunda anotação da Maite",
            "priority": 3 
        }

        login_response = self.client.post("/login/", {"username": "maite_kenzie", "password": "1234"}, format="json")

        admin_token = login_response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + admin_token)

        first_note = self.client.post(self.admin_url, data=first_note_data, format="json")
        second_note = self.client.post(self.admin_url, data=second_note_data, format="json")

        get_response = self.client.get(self.admin_url, format="json")

        # Verificando a resposta retornada:

        expected_data = 2

        returned_data: int = get_response.json()["count"]
        
        msg = f"Usuários autenticados devem conseguir listar as suas duas anotações criadas"

        self.assertEqual(expected_data, returned_data, msg)

        # Verificando o status code retornado na resposta:

        expected_status_code = status.HTTP_200_OK

        returned_status_code = get_response.status_code

        msg = f"Verifique se o status code retornado é {expected_status_code}"

        self.assertEqual(expected_status_code, returned_status_code, msg)

    def test_listing_notes_from_another_user(self):
        first_note_data = {
            "title": "Primeira Anotação da Catarina",
            "description": "Descrição da primeira anotação da Catarina",
            "priority": 1 
        }

        second_note_data = {
            "title": "Segunda Anotação da Catarina",
            "description": "Descrição da segunda anotação da Catarina",
            "priority": 3 
        }

        common_login_response = self.client.post("/login/", {"username": "catarina_kenzie", "password": "1234"}, format="json")

        common_token = common_login_response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + common_token)

        first_common_note = self.client.post(self.common_url, data=first_note_data, format="json") # Usuário comum cria as anotações
        second_common_note = self.client.post(self.common_url, data=second_note_data, format="json")

        admin_login_response = self.client.post("/login/", {"username": "maite_kenzie", "password": "1234"}, format="json")

        admin_token = admin_login_response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + admin_token)

        get_response = self.client.get(self.common_url, format="json")  # Usuário administrador tenta listar as anotações do usuário comum

        # Verificando a resposta retornada:

        expected_data = {"detail": "You do not have permission to perform this action."}

        returned_data: dict = get_response.json()

        msg = "A resposta retornada precisa indiciar que o usuário não tem permissão" 
    
        self.assertDictEqual(expected_data, returned_data, msg)

        # Verificando o status code retornado na resposta:

        expected_status_code = status.HTTP_403_FORBIDDEN

        returned_status_code = get_response.status_code

        msg = f"Verifique se o status code retornado é {expected_status_code}"
        
        self.assertEqual(expected_status_code, returned_status_code, msg)

    def test_listing_notes_without_authentication(self):
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
