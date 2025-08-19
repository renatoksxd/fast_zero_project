from http import HTTPStatus


def test_read_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')  # act (ação)

    assert response.status_code == HTTPStatus.OK  # assert (confirmação)
    assert response.json() == {'message': 'Olá Mundo!'}  # assert
    # (confirmação)


def test_ola_mundo_retorna_ok_e_ola_mundo_ex(client):
    acao = client.get('/ex1')  # act

    assert acao.status_code == HTTPStatus.OK
    assert '<h1> Olá Mundo! </h1>' in acao.text
