from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from schemas import Message

app = FastAPI(title='Minha API Bala!')


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}


@app.get('/ex1', status_code=HTTPStatus.OK, response_class=HTMLResponse)
def ola_mundo():
    mensagem_html = """<html>
      <head>
        <title> Meu Olá Mundo!</title>
      </head>
      <body>
        <h1> Olá Mundo! </h1>
      </body>
      </html>
        """
    return mensagem_html
