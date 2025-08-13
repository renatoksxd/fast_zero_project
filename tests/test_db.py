from sqlalchemy import select

from main.models import User


def test_create_user(session):
    user = User(
        username='bob', password='minha_senha-legal', email='bob@gmail.com'
    )
    session.add(user)
    session.commit()

    result = session.scalar(select(User).where(User.email == 'bob@gmail.com'))

    assert result.id == 1
