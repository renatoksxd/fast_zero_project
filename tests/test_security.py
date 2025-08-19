from http import HTTPStatus

from jwt import decode

from main.security import create_access_token


def test_jwt(settings):
    data = {'teste': 'teste'}

    token = create_access_token(data)

    decoded = decode(token, settings.SECRET_KEY, settings.ALGORITHM)

    assert decoded['teste'] == data['teste']
    assert 'exp' in decoded


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
