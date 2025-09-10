from http import HTTPStatus

from main.schemas import UserPublic


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


def test_read_user_com_id(client, user):
    response = client.get(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user.id,
        'username': user.username,
        'email': user.email,
    }


def test_read_user_deve_retornar_erro_ex(client, user):
    response = client.get('/users/100')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_read_users(client, user, token):
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


def test_update_integrity_error(client, user, other_user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': other_user.username,
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username or email already exist'}


def test_update_user_with_wrong_user(client, other_user, token):
    response = client.put(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_delete_user_wrong_user(client, other_user, token):
    response = client.delete(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}
