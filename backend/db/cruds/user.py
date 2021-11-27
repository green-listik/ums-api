from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import bcrypt
from ..models import *


def register_user(session: AsyncSession, user_id: int, login: str, password: str, surname: str, name: str,
                  patronymic: str, depo_id: int):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_user = User(id=user_id, login=login, hashed_pass=hashed_password, last_name=surname, first_name=name,
                    patronymic=patronymic, department_id=depo_id)
    session.add(new_user)
    await session.commit()
    return new_user


def get_user_id(session: AsyncSession, user_id: int):
    user = await session.execute(select(User).where(User.id == user_id))
    return user.scalars().one()


def get_user_login(session: AsyncSession, user_login: str):
    user = await session.execute(select(User).where(User.login == user_login))
    return user.scalars().one()


def get_all_users_one_depo(session: AsyncSession, depo_id: int):
    users = await session.execute(select(User).where(User.depo.id == depo_id))
    return users.scalars().all()

