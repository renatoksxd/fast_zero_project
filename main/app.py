import asyncio
import sys
from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from main.schemas import Message
from routers import auth, todos, users

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI(title='Minha API Bala!')

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(todos.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
async def read_root():
    return {'message': 'Olá Mundo!'}


@app.get('/ex1', status_code=HTTPStatus.OK, response_class=HTMLResponse)
async def ola_mundo():
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
