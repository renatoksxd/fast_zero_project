from dataclasses import asdict

from sqlalchemy import select

from main.models import User


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='bob', password='minha_senha-legal', email='bob@gmail.com'
        )
        session.add(new_user)
        session.commit()

        user = session.scalar(select(User).where(User.username == 'bob'))

    assert asdict(user) == {
        'id': 1,
        'username': 'bob',
        'password': 'minha_senha-legal',
        'email': 'bob@gmail.com',
        'created_at': time,
        'updated_at': time,
    }
