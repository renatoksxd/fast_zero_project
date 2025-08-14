from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from main.database import get_session
from main.models import User
from main.schemas import Message, UserList, UserPublic, UserSchema

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


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session=Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username já existe',
            )
        else:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Email já existe',
            )
    db_user = User(
        username=user.username, email=user.email, password=user.password
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', response_model=UserList)
def read_users(
    limit: int = 10, offset: int = 0, session: Session = Depends(get_session)
):
    users = session.scalars(select(User).limit(limit).offset(offset))
    return {'users': users}


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    user_db = session.scalar(select(User).where(User.id == user_id))
    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    try:
        user_db.username = user.username
        user_db.email = user.email
        user_db.password = user.password

        session.add(user_db)
        session.commit()
        session.refresh(user_db)

        return user_db
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or email already exist',
        )


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user_db = session.scalar(select(User).where(User.id == user_id))
    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    session.delete(user_db)
    session.commit()

    return {'message': 'User deleted'}


@app.get('/users/{user_id}', response_model=UserPublic)
def read_user(user_id: int):
    if user_id < 1 or user_id > len():
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    return [user_id - 1]
