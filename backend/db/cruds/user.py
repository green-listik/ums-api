from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import *


def register_user(session: AsyncSession, user_id: int, login: str, hashed_password: str, surname: str, name: str,
                  patronymic: str, depo_id: int):
    new_user = User(id=user_id, login=login, hashed_pass=hashed_password, last_name=surname, first_name=name,
                    patronymic=patronymic, department_id=depo_id)
    session.add(new_user)
    await session.commit()
    return new_user

