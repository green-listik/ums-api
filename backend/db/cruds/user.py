from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import bcrypt
from ..models import *


async def register_user(session: AsyncSession, login: str, password: str, surname: str, name: str,
                        patronymic: str, depo_id: int, edit_events: bool = False, edit_users: bool = False,
                        admin_service: bool = False):
    role = UserRoles(edit_users=edit_users, edit_events=edit_events, admin_service=admin_service)
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    session.add(role)
    new_user = User(login=login, hashed_pass=hashed_password, last_name=surname, first_name=name,
                    patronymic=patronymic, depo_id=depo_id, role_id=role.id)
    new_user.role = role
    session.add(new_user)
    await session.commit()
    return new_user


async def get_user_id(session: AsyncSession, user_id: int):
    user = await session.execute(select(User).where(User.id == user_id))
    return user.scalars().first()


async def get_user_login(session: AsyncSession, user_login: str):
    user = await session.execute(select(User).where(User.login == user_login))
    return user.scalars().first()


async def get_all_users_one_depo(session: AsyncSession, depo_id: int):
    users = await session.execute(select(User).where(User.depo.id == depo_id))
    return users.scalars().all()
