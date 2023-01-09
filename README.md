<h1 align="center">
	<img src='https://www.svgrepo.com/show/142693/notes.svg' alt='Icone de anotações' width='30px' height='30px'/> KenzieNotes
</h1>

## Objetivo e tecnologias utilizadas:
> Aplicação com o objetivo de auxiliar os usuários a criarem anotações online.

> Foi desenvolvida com as tecnologias Python, Django, Django Rest Framework e o banco de dados PostgreSQL.

> OBS.: Na raiz do projeto há um diretório workspace para poder ser utilizado no Insomnia

## Links:

``DER:``
```
https://drive.google.com/file/d/14o99A-noRLrae2SnxDmlVi9RNiUNdDB1/view
```

``Documentação (swagger):``

``Deploy:``

Sua url base é

## Endpoints:

A API tem 16 endpoints, sendo em volta do usuário - podendo cadastrar seu perfil, realizar login, cadastrar diários, fazer anotações em seus diários e tendo a diferença entre os usuários comuns e os administradores.

<h2>
	Endpoints que não necessitam de autenticação:
</h2> 

Não é necessário passar um token para realizar uma requisição bem sucedida nos seguintes endpoints:

<h2 align = "center">
	Criação de Usuário
</h2>

``POST -> api/users/ - FORMATO DA REQUISIÇÃO - usuário comum``

```json
{
	"username": "Kenzinho",
	"email": "kenzinho@kenzie.com",
	"password": "1234",
	"first_name": "Ken",
	"last_name": "Zinho"
}
```

``FORMATO DA RESPOSTA - STATUS 201 - CREATED``

```json
{
	"id": "5a16e3af-f38a-44e7-b977-aaed4b62479d",
	"is_superuser": false,
	"username": "Kenzinho",
	"email": "kenzinho@kenzie.com",
	"first_name": "Ken",
	"last_name": "Zinho",
	"is_adm": false
}
```

<br/>

``POST -> api/users/ - FORMATO DA REQUISIÇÃO - usuário administrador``

```json
{
	"username": "SuperUser",
	"email": "superuser@kenzie.com",
	"password": "1234",
	"first_name": "Super",
	"last_name": "User",
	"is_adm": "True"
}
```

``FORMATO DA RESPOSTA - STATUS 201 - CREATED``

```json
{
	"id": "532e1791-5a2f-44bd-b7db-08fcbea6a29d",
	"is_superuser": true,
	"username": "SuperUser",
	"email": "superuser@kenzie.com",
	"first_name": "Super",
	"last_name": "User",
	"is_adm": true
}
```
<span>Caso o usuário não passe o campo is_adm cadastrará como usuário comum</span>

<h2 align = "center">
	Possíveis Erros
</h2>
	
``POST -> api/users/ - FORMATO DA REQUISIÇÃO - username e/ou email já presentes no banco``

```json
{
	"username": "Kenzinho",
	"email": "kenzinho@kenzie.com",
	"password": "1234",
	"first_name": "Ken",
	"last_name": "Zinho"
}
```

 ``FORMATO DA RESPOSTA - STATUS 400 - BAD REQUEST``

```json
{
	"username": [
		"A user with that username already exists."
	],
	"email": [
		"A user with this email already exists."
	]
}
```

<br/>

``POST -> api/users/ - FORMATO DA REQUISIÇÃO - sem campos``

```json
{

}
```

``FORMATO DA RESPOSTA - STATUS 400 - BAD REQUEST``

```json
{
	"password": [
		"This field is required."
	],
	"username": [
		"This field is required."
	],
	"email": [
		"This field is required."
	],
	"first_name": [
		"This field is required."
	],
	"last_name": [
		"This field is required."
	]
}
```
<h2 align = "center">
	Login
</h2>

``POST -> api/login/- FORMATO DA REQUISIÇÃO - login de usuário``

```json
{
	"username": "SuperUser",
	"password": "1234"
}
```

``FORMATO DE RESPOSTA - STATUS 200 - OK``

```json
{
	"refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY3MzAxNDc2OCwiaWF0IjoxNjcyOTI4MzY4LCJqdGkiOiJiZmJkN2YxOGJlN2M0N2NhYjNkNDNlOTE3ZmU3NDVhMSIsInVzZXJfaWQiOiJiZTZjMWY0ZC1lNzU5LTRmYmEtOTEyOS00ODdkMWQ0NWZiMzgifQ.UseX_0rBG-unfE8IC3NosWewf3tRpDSMUwoNyeb8sbc",
	"access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjczMDE0NzY4LCJpYXQiOjE2NzI5MjgzNjgsImp0aSI6IjY1ZTIxOWJmOTAzYzQxNWJiZjIxMWI2OTdkOGZkNjQ5IiwidXNlcl9pZCI6ImJlNmMxZjRkLWU3NTktNGZiYS05MTI5LTQ4N2QxZDQ1ZmIzOCJ9.tuwaZn_1l7JF2Hn3JsBrT-clZeKtat8itVtu0K-_Zpg"
}
```

<h2 align = "center">
	Possíveis Erros
</h2>

``POST -> api/login/- FORMATO DA REQUISIÇÃO - sem campos``

```json
{

}
```

``FORMATO DA RESPOSTA - STATUS 400 - BAD REQUEST``

```json
{
	"username": [
		"This field is required."
	],
	"password": [
		"This field is required."
	]
}
```

<br/>

``POST -> api/login/- FORMATO DA REQUISIÇÃO - dados incorretos``

```json
{
	"username": "UsuarioErrado",
	"password": "1234"
}
```

``FORMATO DA RESPOSTA - STATUS 401 - UNAUTHORIZED``

```json
{
	"detail": "No active account found with the given credentials"
}
```
<h2>
	Endpoint que necessita de autenticação e apenas administradores podem acessar:
</h2>

Rota que necessita de autorização deve ser informado no cabeçalho da requisição o campo "Authorization", dessa forma: 

> Authorization: Bearer {token}

Após o usuário estar logado e ser um administrador, ele deve conseguir acessar a informação sem problemas.

<h2 align = "center">
	Listagem de Usuários
</h2>

``GET -> api/users/- FORMATO DA REQUISIÇÃO``

Sem corpo da requisição - Na requisição apenas é necessário um TOKEN de administrador, a aplicação ficará responsável em buscar todos os usuários.

``FORMATO DA RESPOSTA - STATUS 200 - OK``

```json
{
	"count": 2,
	"next": null,
	"previous": null,
	"results": [
		{
			"id": "5a16e3af-f38a-44e7-b977-aaed4b62479d",
			"is_superuser": false,
			"username": "Kenzinho",
			"email": "kenzinho@kenzie.com",
			"first_name": "Ken",
			"last_name": "Zinho",
			"is_adm": false
		},
		{
			"id": "532e1791-5a2f-44bd-b7db-08fcbea6a29d",
			"is_superuser": true,
			"username": "SuperUser",
			"email": "superuser@kenzie.com",
			"first_name": "Super",
			"last_name": "User",
			"is_adm": true
		}
	]
}
```
<h2 align = "center">
	Possíveis Erros
</h2>

``GET -> api/users/- FORMATO DA REQUISIÇÃO - usuário comum``

Sem corpo da requisição

``FORMATO DA RESPOSTA - STATUS 403 - FORBIDDEN``

```json
{
	"detail": "You do not have permission to perform this action."
}
```

<br/>

``GET -> api/users/- FORMATO DA REQUISIÇÃO - sem token``

Sem corpo da requisição

``FORMATO DA RESPOSTA - STATUS 401 - UNAUTHORIZED``

```json
{
	"detail": "Authentication credentials were not provided."
}
```

<h2> Endpoints que necessitam de autenticação e apenas administradores ou o próprio usuário podem acessar: </h2>

Rotas que necessitam de autorização deve ser informado no cabeçalho da requisição o campo "Authorization", dessa forma: 

> Authorization: Bearer {token}

Após o usuário estar logado, ele deve conseguir acessar as informações sem problemas.

<h2 align = "center"> Listagem de Usuário Único </h2>

``GET -> api/users/<uuid:user_id>/ - FORMATO DA REQUISIÇÃO - administrador``

Sem corpo da requisição - Na requisição apenas é necessário um TOKEN, a aplicação ficará responsável em buscar o usuário que está no parâmetro da rota.

``FORMATO DA RESPOSTA - STATUS 200 - OK``

```json
{
	"id": "5a16e3af-f38a-44e7-b977-aaed4b62479d",
	"is_superuser": false,
	"username": "Kenzinho",
	"email": "kenzinho@kenzie.com",
	"first_name": "Ken",
	"last_name": "Zinho",
	"is_adm": false
}
```

<br/>

``GET -> api/users/<uuid:user_id>/ - FORMATO DA REQUISIÇÃO - próprio usuário``

Sem corpo da requisição - Na requisição apenas é necessário um TOKEN, a aplicação ficará responsável em buscar o usuário que está no parâmetro da rota.

``FORMATO DA RESPOSTA - STATUS 200 - OK``

```json
{
	"id": "5a16e3af-f38a-44e7-b977-aaed4b62479d",
	"is_superuser": false,
	"username": "Kenzinho",
	"email": "kenzinho@kenzie.com",
	"first_name": "Ken",
	"last_name": "Zinho",
	"is_adm": false
}
```

<h2 align = "center"> Possíveis Erros </h2>

``GET -> api/users/<uuid:user_id>/ - FORMATO DA REQUISIÇÃO - outro usuário comum``

Sem corpo da requisição - Na requisição apenas é necessário um TOKEN, a aplicação ficará responsável em buscar o usuário que está no parâmetro da rota.

``FORMATO DA RESPOSTA - STATUS 403 - FORBIDDEN``

```json
{
	"detail": "You do not have permission to perform this action."
}
```

<br/>

``GET -> api/users/<uuid:user_id>/ - FORMATO DA REQUISIÇÃO - sem token``

Sem corpo da requisição - Na requisição apenas é necessário um TOKEN, a aplicação ficará responsável em buscar o usuário que está no parâmetro da rota.

``FORMATO DA RESPOSTA - STATUS 401 - UNAUTHORIZED``

```json
{
	"detail": "Authentication credentials were not provided."
}
```

<br/>

``GET -> api/users/<uuid:user_id>/ - FORMATO DA REQUISIÇÃO - id inexistente``

Sem corpo da requisição - Na requisição apenas é necessário um TOKEN, a aplicação ficará responsável em buscar o usuário que está no parâmetro da rota.

``FORMATO DA RESPOSTA - STATUS 404 - NOT FOUND``

```json
{
	"detail": "Not found."
}
```

<h2 align = "center"> Atualização de Usuário Único </h2>

``PATCH -> api/users/<uuid:user_id>/ - FORMATO DA REQUISIÇÃO - administrador``

```json
{
	"first_name": "Kenzinho - Editado por SuperUser"
}
```

``FORMATO DA RESPOSTA - STATUS 200 - OK``

```json
{
	"id": "5a16e3af-f38a-44e7-b977-aaed4b62479d",
	"is_superuser": false,
	"username": "Kenzinho",
	"email": "kenzinho@kenzie.com",
	"first_name": "Kenzinho - Editado por SuperUser",
	"last_name": "Zinho",
	"is_adm": false
}
```

<br/>

``PATCH -> api/users/<uuid:user_id>/ - FORMATO DA REQUISIÇÃO - próprio usuário``

```json
{
	"first_name": "Kenzinho - Editado por Kenzinho"
}
```

``FORMATO DA RESPOSTA - STATUS 200 - OK``

```json
{
	"id": "5a16e3af-f38a-44e7-b977-aaed4b62479d",
	"is_superuser": false,
	"username": "Kenzinho",
	"email": "kenzinho@kenzie.com",
	"first_name": "Kenzinho - Editado por Kenzinho",
	"last_name": "Zinho",
	"is_adm": false
}
```

<h2 align = "center"> Possíveis Erros </h2>

``PATCH -> api/users/<uuid:user_id>/ - FORMATO DA REQUISIÇÃO - outro usuário comum``

```json
{
	"username": "Kenzinho - Tentativa de Edição por OutroUser"
}
```

``FORMATO DA RESPOSTA - STATUS 403 - FORBIDDEN``

```json
{
	"detail": "You do not have permission to perform this action."
}
```

<br/>

``PATCH -> api/users/<uuid:user_id>/ - FORMATO DA REQUISIÇÃO - sem token``

```json
{
	"username": "Kenzinho - Tentativa de Edição sem Token"
}
```

``FORMATO DA RESPOSTA - STATUS 401 - UNAUTHORIZED``

```json
{
	"detail": "Authentication credentials were not provided."
}
```

<br/>

``PATCH -> api/users/<uuid:user_id>/ - FORMATO DA REQUISIÇÃO - id inexistente``

```json
{
	"username": "Tentativa de Edição de um User não existente"
}
```

``FORMATO DA RESPOSTA - STATUS 404 - NOT FOUND``

```json
{
	"detail": "Not found."
}
```

<h2 align = "center"> Deleção de Usuário Único </h2>

``DELETE -> api/users/<uuid:user_id>/ - FORMATO DA REQUISIÇÃO - administrador``

Sem corpo da requisição - Na requisição apenas é necessário um TOKEN, a aplicação ficará responsável em buscar o usuário que está no parâmetro da rota.

``FORMATO DA RESPOSTA - STATUS 204 - NO CONTENT``

Sem corpo da resposta, porém o usuário foi deletado.

<br/>

``DELETE -> api/users/<uuid:user_id>/ - FORMATO DA REQUISIÇÃO - próprio usuário``

Sem corpo da requisição - Na requisição apenas é necessário um TOKEN, a aplicação ficará responsável em buscar o usuário que está no parâmetro da rota.

``FORMATO DA RESPOSTA - STATUS 204 - NO CONTENT``

Sem corpo da resposta, porém o usuário foi deletado.

<h2 align = "center"> Possíveis Erros </h2>

``DELETE -> api/users/<uuid:user_id>/ - FORMATO DA REQUISIÇÃO - outro usuário comum``

Sem corpo da requisição - Na requisição apenas é necessário um TOKEN, a aplicação ficará responsável em buscar o usuário que está no parâmetro da rota.

``FORMATO DA RESPOSTA - STATUS 403 - FORBIDDEN``

```json
{
	"detail": "You do not have permission to perform this action."
}
```

<br/>

``DELETE -> api/users/<uuid:user_id>/ - FORMATO DA REQUISIÇÃO - sem token``

Sem corpo da requisição - Na requisição apenas é necessário um TOKEN, a aplicação ficará responsável em buscar o usuário que está no parâmetro da rota.

``FORMATO DA RESPOSTA - STATUS 401 - UNAUTHORIZED``

```json
{
	"detail": "Authentication credentials were not provided."
}
```

<br/>

``DELETE -> api/users/<uuid:user_id>/ - FORMATO DA REQUISIÇÃO - id inexistente``

Sem corpo da requisição - Na requisição apenas é necessário um TOKEN, a aplicação ficará responsável em buscar o usuário que está no parâmetro da rota.

``FORMATO DA RESPOSTA - STATUS 404 - NOT FOUND``

```json
{
	"detail": "Not found."
}
```

<h2> Endpoints que necessitam de autenticação e apenas o próprio usuário podem acessar: </h2>

Rotas que necessitam de autorização deve ser informado no cabeçalho da requisição o campo "Authorization", dessa forma: 

> Authorization: Bearer {token}

Após o usuário estar logado, ele deve conseguir acessar as informações sem problemas.

<h2 align = "center"> Criação de Diários </h2>

``POST -> api/diaries/ - FORMATO DA REQUISIÇÃO``

```json
{
	"name": "Diário do Kenzinho"
}
```

``FORMATO DA RESPOSTA - STATUS 201 - CREATED``

```json
{
	"id": "dfa237bb-0454-41f0-b259-6ce98cce8db1",
	"name": "Diário do Kenzinho",
	"user_id": "ad8dcba1-65eb-478b-8b59-f3a457fe92c4",
	"created_at": "2023-01-06T17:07:41.155985Z"
}
```

<h2 align = "center"> Possíveis Erros </h2>

``POST -> api/diaries/ - FORMATO DA REQUISIÇÃO - sem token``

```json
{
	"name": "Usuário sem token"
}
```

``FORMATO DA RESPOSTA - STATUS 401 - UNAUTHORIZED``

```json
{
	"detail": "Authentication credentials were not provided."
}
```

<br/>

``POST -> api/diaries/ - FORMATO DA REQUISIÇÃO - sem campos``

```json
{

}
```

``FORMATO DA RESPOSTA - STATUS 400 - BAD REQUEST``

```json
{
	"name": [
		"This field is required."
	]
}
```

<h2 align = "center"> Listagem de Diários </h2>

``GET -> api/diaries/ - FORMATO DA REQUISIÇÃO``

Sem corpo da requisição - Na requisição apenas é necessário um TOKEN, a aplicação ficará responsável em buscar os diários do usuário que está realizando a requisição.

``FORMATO DA RESPOSTA - STATUS 200 - OK``

```json
{
	"count": 1,
	"next": null,
	"previous": null,
	"results": [
		{
			"id": "dfa237bb-0454-41f0-b259-6ce98cce8db1",
			"name": "Diário do Kenzinho",
			"user_id": "ad8dcba1-65eb-478b-8b59-f3a457fe92c4",
			"created_at": "2023-01-06T17:07:41.155985Z"
		}
	]
}
```

<h2 align = "center"> Possíveis Erros </h2>

``GET -> api/diaries/ - FORMATO DA REQUISIÇÃO - sem token``

Sem corpo da requisição - Na requisição apenas é necessário um TOKEN, a aplicação ficará responsável em buscar os diários do usuário que está realizando a requisição.

``FORMATO DA RESPOSTA - STATUS 401 - UNAUTHORIZED``

```json
{
	"detail": "Authentication credentials were not provided."
}
```

<h2 align = "center"> Listagem de Diário Único </h2>

``GET -> api/diaries/<uuid:diary_id>/ - FORMATO DA REQUISIÇÃO``

Sem corpo da requisição - Na requisição apenas é necessário um TOKEN, a aplicação ficará responsável em buscar o diário que está sendo passado como parâmetro.

``FORMATO DA RESPOSTA - STATUS 200 - OK``

```json
{
	"id": "dfa237bb-0454-41f0-b259-6ce98cce8db1",
	"name": "Diário do Kenzinho",
	"user_id": "ad8dcba1-65eb-478b-8b59-f3a457fe92c4",
	"created_at": "2023-01-06T17:07:41.155985Z"
}
```

<h2 align = "center"> Possíveis Erros </h2>

``GET -> api/diaries/<uuid:diary_id>/ - FORMATO DA REQUISIÇÃO - outro usuário ou administrador``

Sem corpo da requisição - Na requisição apenas é necessário um TOKEN, a aplicação ficará responsável em buscar o diário que está sendo passado como parâmetro.

``FORMATO DA RESPOSTA - STATUS 403 - FORBIDDEN``

```json
{
	"detail": "You do not have permission to perform this action."
}
```

<br/>

``GET -> api/diaries/<uuid:diary_id>/ - FORMATO DA REQUISIÇÃO - id inexistente``

Sem corpo da requisição - Na requisição apenas é necessário um TOKEN, a aplicação ficará responsável em buscar o diário que está sendo passado como parâmetro.

``FORMATO DA RESPOSTA - STATUS 404 - NOT FOUND``

```json
{
	"detail": "Not found."
}
```

<br/>

``GET -> api/diaries/<uuid:diary_id>/ - FORMATO DA REQUISIÇÃO - sem token``

Sem corpo da requisição - Na requisição apenas é necessário um TOKEN, a aplicação ficará responsável em buscar o diário que está sendo passado como parâmetro.

``FORMATO DA RESPOSTA - STATUS 401 - UNAUTHORIZED``

```json
{
	"detail": "Authentication credentials were not provided."
}
```

<h2 align = "center"> Atualização de Diário Único </h2>

``PATCH -> api/diaries/<uuid:diary_id>/ - FORMATO DA REQUISIÇÃO``

```json
{
	"name": "Kenzinho - First - Editado pelo próprio dono"
}
```

``FORMATO DA RESPOSTA - STATUS 200 - OK``

```json
{
	"id": "dfa237bb-0454-41f0-b259-6ce98cce8db1",
	"name": "Kenzinho - First - Editado pelo próprio dono",
	"user_id": "ad8dcba1-65eb-478b-8b59-f3a457fe92c4",
	"created_at": "2023-01-06T17:07:41.155985Z"
}
```

<h2 align = "center"> Possíveis Erros </h2>

``PATCH -> api/diaries/<uuid:diary_id>/ - FORMATO DA REQUISIÇÃO - outro usuário ou administrador``

```json
{
	"name": "Tentativa de Edição por outro user"
}
```

``FORMATO DA RESPOSTA - STATUS 403 - FORBIDDEN``

```json
{
	"detail": "You do not have permission to perform this action."
}
```

<br/>

``PATCH -> api/diaries/<uuid:diary_id>/ - FORMATO DA REQUISIÇÃO - id inexistente``

```json
{
	"name": "Tentativa de Edição de Diário com id que não existente"
}
```

``FORMATO DA RESPOSTA - STATUS 404 - NOT FOUND``

```json
{
	"detail": "Not found."
}
```

<br/>

``PATCH -> api/diaries/<uuid:diary_id>/ - FORMATO DA REQUISIÇÃO - sem token``

```json
{
	"name": "Tentativa de Edição de Diário sem token"
}
```

``FORMATO DA RESPOSTA - STATUS 401 - UNAUTHORIZED``

```json
{
	"detail": "Authentication credentials were not provided."
}
```

<h2 align = "center"> Deleção de Diário Único </h2>

``DELETE -> api/diaries/<uuid:diary_id>/ - FORMATO DA REQUISIÇÃO``

Sem corpo da requisição - Na requisição apenas é necessário um TOKEN, a aplicação ficará responsável em buscar o diário que está no parâmetro da rota.

``FORMATO DA RESPOSTA - STATUS 204 - NO CONTENT``

Sem corpo da resposta, porém o diário foi deletado.

<h2 align = "center"> Possíveis Erros </h2>

``DELETE -> api/diaries/<uuid:diary_id>/ - FORMATO DA REQUISIÇÃO - outro usuário ou administrador``

Sem corpo da requisição - Na requisição apenas é necessário um TOKEN, a aplicação ficará responsável em buscar o diário que está no parâmetro da rota.

``FORMATO DA RESPOSTA - STATUS 403 - FORBIDDEN``

```json
{
	"detail": "You do not have permission to perform this action."
}
```

<br/>

``DELETE -> api/diaries/<uuid:diary_id>/ - FORMATO DA REQUISIÇÃO - id inexistente``

Sem corpo da requisição - Na requisição apenas é necessário um TOKEN, a aplicação ficará responsável em buscar o diário que está no parâmetro da rota.

``FORMATO DA RESPOSTA - STATUS 404 - NOT FOUND``

```json
{
	"detail": "Not found."
}
```

<br/>

``DELETE -> api/diaries/<uuid:diary_id>/ - FORMATO DA REQUISIÇÃO - sem token``

Sem corpo da requisição - Na requisição apenas é necessário um TOKEN, a aplicação ficará responsável em buscar o diário que está no parâmetro da rota.

``FORMATO DA RESPOSTA - STATUS 401 - UNAUTHORIZED``

```json
{
	"detail": "Authentication credentials were not provided."
}
```

<h2 align = "center"> Criação de Anotações </h2>

``POST -> api/diaries/<uuid:diary_id>/notes/ - FORMATO DA REQUISIÇÃO``

```json
{
	"title": "Anotação do Kenzinho",
	"description": "Primeira Anotação do Kenzinho Criada"
}
```

``FORMATO DA RESPOSTA - STATUS 201 - CREATED``

```json
{
	"id": "38f298cf-31e7-4cfe-9ed9-bc3801ec4966",
	"title": "Anotação do Kenzinho",
	"description": "Primeira Anotação do Kenzinho Criada",
	"priority": 2,
	"diary_id": "d0f1a087-b0c6-4743-9f41-19b5420c3a20"
}
```

<span> Priority é um campo numérico que aceita apenas de 1 a 3 e não é obrigatório passá-lo sendo preenchido com o valor 2</span> 

<ul>
	<li>1 - Baixa prioridade</li>
	<li>2 - Média prioridade</li>
	<li>3 - Alta prioridade</li>
</ul>

<h2 align = "center"> Possíveis Erros </h2>

``POST -> api/diaries/<uuid:diary_id>/notes/ - FORMATO DA REQUISIÇÃO - id de diário inexistente``

```json
{
	"title": "Anotação do Kenzinho",
	"description": "Primeira Anotação do Kenzinho Criada"
}
```

``FORMATO DA RESPOSTA - STATUS 404 - BAD REQUEST``

```json
{
	"detail": "Not found."
}
```

<br/>

``POST -> api/diaries/<uuid:diary_id>/notes/ - FORMATO DA REQUISIÇÃO - priority menor que 1``

```json
{
	"title": "Anotação do Kenzinho prioridade 0",
	"description": "Primeira Anotação do Kenzinho Criada",
	"priority": 0
}
```

``FORMATO DA RESPOSTA - STATUS 400 - BAD REQUEST``

```json
{
	"priority": [
		"Ensure this value is greater than or equal to 1."
	]
}
```

<br/>

``POST -> api/diaries/<uuid:diary_id>/notes/ - FORMATO DA REQUISIÇÃO - priority maior que 3``

```json
{
	"title": "Anotação do Kenzinho prioridade 4",
	"description": "Primeira Anotação do Kenzinho Criada",
	"priority": 4
}
```

``FORMATO DA RESPOSTA - STATUS 400 - BAD REQUEST``

```json
{
	"priority": [
		"Ensure this value is less than or equal to 3."
	]
}
```

<br/>

``POST -> api/diaries/<uuid:diary_id>/notes/ - FORMATO DA REQUISIÇÃO - priority maior que 3``

```json
{
	"title": "Anotação do Kenzinho prioridade 4",
	"description": "Primeira Anotação do Kenzinho Criada",
	"priority": 4
}
```

``FORMATO DA RESPOSTA - STATUS 400 - BAD REQUEST``

```json
{
	"priority": [
		"Ensure this value is less than or equal to 3."
	]
}
```

<br/>

``POST -> api/diaries/<uuid:diary_id>/notes/ - FORMATO DA REQUISIÇÃO - outro usuário ou administrador``

```json
{
	"title": "Travou Maitê - Conta3",
	"description": "Conta da Catarina, conta.",
	"priority": 1
}
```

``FORMATO DA RESPOSTA - STATUS 403 - FORBIDDEN``

```json
{
	"detail": "You do not have permission to perform this action."
}
```

<br/>

``POST -> api/diaries/<uuid:diary_id>/notes/ - FORMATO DA REQUISIÇÃO - sem campos``

```json
{

}
```

``FORMATO DA RESPOSTA - STATUS 400 - BAD REQUEST``

```json
{
	"title": [
		"This field is required."
	],
	"description": [
		"This field is required."
	]
}
```

<br/>

``POST -> api/diaries/<uuid:diary_id>/notes/ - FORMATO DA REQUISIÇÃO - sem token``

```json
{
	"title": "Travou Maitê - Conta3",
	"description": "Conta da Catarina, conta.",
	"priority": 3
}
```

``FORMATO DA RESPOSTA - STATUS 401 - UNAUTHORIZED``

```json
{
	"detail": "Authentication credentials were not provided."
}
```

<h2 align = "center"> Listagem de Anotações </h2>

``GET -> api/diaries/<uuid:diary_id>/notes/ - FORMATO DA REQUISIÇÃO``

Sem corpo da requisição - Na requisição apenas é necessário um TOKEN, a aplicação ficará responsável em buscar as anotações do diário que está no parâmetro da rota.

``FORMATO DA RESPOSTA - STATUS 200 - OK``

```json
{
	"count": 3,
	"next": "http://localhost:8000/api/diaries/d0f1a087-b0c6-4743-9f41-19b5420c3a20/notes/?page=2",
	"previous": null,
	"results": [
		{
			"id": "38f298cf-31e7-4cfe-9ed9-bc3801ec4966",
			"title": "Anotação do Kenzinho",
			"description": "Primeira Anotação do Kenzinho Criada",
			"priority": 2,
			"diary_id": "d0f1a087-b0c6-4743-9f41-19b5420c3a20"
		},
		{
			"id": "bcad2493-9b49-43c9-a28c-53812ce934b5",
			"title": "Anotação do Kenzinho",
			"description": "Primeira Anotação do Kenzinho Criada",
			"priority": 1,
			"diary_id": "d0f1a087-b0c6-4743-9f41-19b5420c3a20"
		}
	]
}
```

Podemos utilizar os query params para mudar a lista, filtrando por prioridade. Uma requisição apenas no api/diaries/<uuid:diary_id>/notes/ irá trazer as anotações de "priority": "3". Com o parâmetro priority, podemos filtrar por prioridade.

``GET -> api/diaries/<uuid:diary_id>/notes/?priority=2 - FORMATO DA REQUISIÇÃO``

Sem corpo da requisição - Na requisição apenas é necessário um TOKEN, a aplicação ficará responsável em buscar as anotações do diário que está no parâmetro da rota e também em filtrar a lista.

``FORMATO DA RESPOSTA - STATUS 200 - OK``

```json
{
	"count": 1,
	"next": null,
	"previous": null,
	"results": [
		{
			"id": "6226616f-eb8b-486c-a654-8ed632c39b63",
			"title": "Anotação do Kenzinho",
			"description": "Primeira Anotação do Kenzinho Criada",
			"priority": 2,
			"diary_id": "d0f1a087-b0c6-4743-9f41-19b5420c3a20"
		}
	]
}
```


<h2 align = "center"> Possíveis Erros </h2>

``GET -> api/diaries/<uuid:diary_id>/notes/ - FORMATO DA REQUISIÇÃO - outro usuário ou administrador``

Sem corpo da requisição - Na requisição apenas é necessário um TOKEN, a aplicação ficará responsável em buscar as anotações do diário que está no parâmetro da rota.

``FORMATO DA RESPOSTA - STATUS 403 - FORBIDDEN``

```json
{
	"detail": "You do not have permission to perform this action."
}
```

<br/>

``GET -> api/diaries/<uuid:diary_id>/notes/ - FORMATO DA REQUISIÇÃO - id de diário inexistente``

Sem corpo da requisição - Na requisição apenas é necessário um TOKEN, a aplicação ficará responsável em buscar as anotações do diário que está no parâmetro da rota.

``FORMATO DA RESPOSTA - STATUS 404 - NOT FOUND``

```json
{
	"detail": "Not found."
}
```

<br/>

``GET -> api/diaries/<uuid:diary_id>/notes/ - FORMATO DA REQUISIÇÃO - sem token``

Sem corpo da requisição - Na requisição apenas é necessário um TOKEN, a aplicação ficará responsável em buscar as anotações do diário que está no parâmetro da rota.

``FORMATO DA RESPOSTA - STATUS 401 - UNAUTHORIZED``

```json
{
	"detail": "Authentication credentials were not provided."
}
```

<h2 align = "center"> Listagem de Anotação Única </h2>

``GET -> api/notes/<uuid:note_id>/ - FORMATO DA REQUISIÇÃO``

Sem corpo da requisição - Na requisição apenas é necessário um TOKEN, a aplicação ficará responsável em buscar a anotação que está no parâmetro da rota.

``FORMATO DA RESPOSTA - STATUS 200 - OK``

```json
{
	"id": "38f298cf-31e7-4cfe-9ed9-bc3801ec4966",
	"title": "Anotação do Kenzinho",
	"description": "Primeira Anotação do Kenzinho Criada",
	"priority": 2,
	"diary_id": "d0f1a087-b0c6-4743-9f41-19b5420c3a20"
}
```

<h2 align = "center"> Possíveis Erros </h2>

``GET -> api/notes/<uuid:note_id>/ - FORMATO DA REQUISIÇÃO - outro usuário ou administrador``

Sem corpo da requisição - Na requisição apenas é necessário um TOKEN, a aplicação ficará responsável em buscar a anotação que está no parâmetro da rota.

``FORMATO DA RESPOSTA - STATUS 403 - FORBIDDEN``

```json
{
	"detail": "You do not have permission to perform this action."
}
```

<br/>

``GET -> api/notes/<uuid:note_id>/ - FORMATO DA REQUISIÇÃO - id inexistente``

Sem corpo da requisição - Na requisição apenas é necessário um TOKEN, a aplicação ficará responsável em buscar a anotação que está no parâmetro da rota.

``FORMATO DA RESPOSTA - STATUS 404 - NOT FOUND``

```json
{
	"detail": "Not found."
}
```

<br/>

``GET -> api/notes/<uuid:note_id>/ - FORMATO DA REQUISIÇÃO - sem token``

Sem corpo da requisição - Na requisição apenas é necessário um TOKEN, a aplicação ficará responsável em buscar a anotação que está no parâmetro da rota.

``FORMATO DA RESPOSTA - STATUS 401 - UNAUTHORIZED``

```json
{
	"detail": "Authentication credentials were not provided."
}
```

<h2 align = "center"> Atualização de Anotação Única </h2>

``PATCH -> api/notes/<uuid:note_id>/ - FORMATO DA REQUISIÇÃO``

```json
{
	"title": "Anotação do Kenzinho - Editado pelo próprio dono da anotação"
}
```

``FORMATO DA RESPOSTA - STATUS 200 - OK``

```json
{
	"id": "6226616f-eb8b-486c-a654-8ed632c39b63",
	"title": "Anotação do Kenzinho - Editado pelo próprio dono da anotação",
	"description": "Primeira Anotação do Kenzinho Criada",
	"priority": 2,
	"diary_id": "d0f1a087-b0c6-4743-9f41-19b5420c3a20"
}
```

<h2 align = "center"> Possíveis Erros </h2>

``PATCH -> api/notes/<uuid:note_id>/ - FORMATO DA REQUISIÇÃO - outro usuário ou administrador``

```json
{
	"title": "Anotação do Kenzinho - Editado por outro usuário"
}
```

``FORMATO DA RESPOSTA - STATUS 403 - FORBIDDEN``

```json
{
	"detail": "You do not have permission to perform this action."
}
```

<br/>

``PATCH -> api/notes/<uuid:note_id>/ - FORMATO DA REQUISIÇÃO - id inexistente``

```json
{
	"title": "Anotação do Kenzinho - Editado - Anotação com id que não existe"
}
```

``FORMATO DA RESPOSTA - STATUS 404 - NOT FOUND``

```json
{
	"detail": "Not found."
}
```

<br/>

``PATCH -> api/notes/<uuid:note_id>/ - FORMATO DA REQUISIÇÃO - sem token``

```json
{
	"title": "Anotação do Kenzinho - Editado sem token"
}
```

``FORMATO DA RESPOSTA - STATUS 401 - UNAUTHORIZED``

```json
{
	"detail": "Authentication credentials were not provided."
}
```

<h2 align = "center"> Deleção de Anotação Única </h2>

``DELETE -> api/notes/<uuid:note_id>/ - FORMATO DA REQUISIÇÃO``

Sem corpo da requisição - Na requisição apenas é necessário um TOKEN, a aplicação ficará responsável em buscar a anotação que está no parâmetro da rota.

``FORMATO DA RESPOSTA - STATUS 204 - NO CONTENT``

Sem corpo de resposta, porém a anotação foi excluída.

<h2 align = "center"> Possíveis Erros </h2>

``DELETE -> api/notes/<uuid:note_id>/ - FORMATO DA REQUISIÇÃO - outro usuário ou administrador``

Sem corpo da requisição - Na requisição apenas é necessário um TOKEN, a aplicação ficará responsável em buscar a anotação que está no parâmetro da rota.

``FORMATO DA RESPOSTA - STATUS 403 - FORBIDDEN``

```json
{
	"detail": "You do not have permission to perform this action."
}
```

<br/>

``DELETE -> api/notes/<uuid:note_id>/ - FORMATO DA REQUISIÇÃO - id inexistente``

Sem corpo da requisição - Na requisição apenas é necessário um TOKEN, a aplicação ficará responsável em buscar a anotação que está no parâmetro da rota.

``FORMATO DA RESPOSTA - STATUS 404 - NOT FOUND``

```json
{
	"detail": "Not found."
}
```

<br/>

``DELETE -> api/notes/<uuid:note_id>/ - FORMATO DA REQUISIÇÃO - sem token``

Sem corpo da requisição - Na requisição apenas é necessário um TOKEN, a aplicação ficará responsável em buscar a anotação que está no parâmetro da rota.

``FORMATO DA RESPOSTA - STATUS 401 - UNAUTHORIZED``

```json
{
	"detail": "Authentication credentials were not provided."
}
```

<br/>

<span>Feito com amor pela Equipe da Kenzie Notes </span>
