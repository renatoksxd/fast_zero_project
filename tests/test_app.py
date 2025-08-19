from http import HTTPStatus

from main.schemas import UserPublic
from main.security import create_access_token


def test_read_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')  # act (ação)

    assert response.status_code == HTTPStatus.OK  # assert (confirmação)
    assert response.json() == {'message': 'Olá Mundo!'}  # assert
    # (confirmação)


def test_ola_mundo_retorna_ok_e_ola_mundo_ex(client):
    acao = client.get('/ex1')  # act

    assert acao.status_code == HTTPStatus.OK
    assert '<h1> Olá Mundo! </h1>' in acao.text


def test_create_user(client):
    response = client.post(  # UserSchema
        '/users/',
        json={
            'username': 'testusername',
            'email': 'test@test.com',
            'password': 'password',
        },
    )

    # Voltou o status code correto?
    assert response.status_code == HTTPStatus.CREATED
    # Validar UserPublic
    assert response.json() == {
        'username': 'testusername',
        'email': 'test@test.com',
        'id': 1,
    }


def test_create_user_valida_erro_de_usuario_existente_ex(client):
    client.post(  # incluindo cadastro lucas
        '/users',
        json={
            'username': 'lucas',
            'email': 'lucas@example.com',
            'password': 'teste',
        },
    )

    response = client.post(  # Tentanco criar novo usuário
        '/users',
        json={
            'username': 'lucas',
            'email': 'teste@example.com',
            'password': 'testeteste',
        },
    )
    # Validando erro
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already exist'}


def test_create_user_valida_erro_de_email_existente_ex(client):
    client.post(  # incluindo cadastro lucas
        '/users',
        json={
            'username': 'lucas',
            'email': 'lucas@example.com',
            'password': 'teste',
        },
    )

    response = client.post(  # Tentanco criar novo usuário
        '/users',
        json={
            'username': 'luiz',
            'email': 'lucas@example.com',
            'password': 'testeteste',
        },
    )
    # Validando erro
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exist'}


def test_read_user_ex(client, user):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'Teste',
        'email': 'teste@test.com',
        'id': 1,
    }


def test_read_user_deve_retornar_erro_ex(client, user):
    response = client.get('/users/100')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_read_users_with_user(client, user, token):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get(
        '/users/', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, token):
    response = client.put(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'testusername2',
            'email': 'test@test.com',
            'password': '123',
            'id': 1,
        },
    )

    assert response.json() == {
        'username': 'testusername2',
        'email': 'test@test.com',
        'id': 1,
    }


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_update_integrity_error(client, user, token):
    # Inserindo Fausto
    client.post(
        '/users',
        json={
            'username': 'fausto',
            'email': 'fausto@example.com',
            'password': 'secret',
        },
    )

    # Alterando o user da fixture para Fausto
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'fausto',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username or email already exist'}


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'bearer'
    assert 'access_token' in token


def test_get_token_current_user_erro_ex(client):
    data = {'email': 'test'}
    token = create_access_token(data)

    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_token_current_user_nao_encontrado_ex(client):
    data = {'sub': 'test@test'}
    token = create_access_token(data)

    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
