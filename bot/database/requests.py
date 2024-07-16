from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from .models.users import User

async def register_user(session: AsyncSession, username: str, password: str, name: str, surname: str, patronymic: str) -> User:
    user = User(
        username=username,
        name=name,
        surname=surname,
        patronymic=patronymic,
    )
    
    user.set_password(password)
    
    try:
        session.add(user)
        await session.commit()
        return user
    except IntegrityError:
        await session.rollback()
        raise Exception("Пользователь с таким именем пользователя или электронной почтой уже существует")
    except Exception as e:
        await session.rollback()
        raise Exception(f"Произошла ошибка при регистрации пользователя: {e}")