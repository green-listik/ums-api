from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.models import User


def register_user(session: AsyncSession, login: str, password: str, surname: str, name: str, patronymic: str):
    pass


async def get_user_by_login(session: AsyncSession, login: str):
    q = await session.execute(select(User).where(User.login == login))
    return q.scalars().first()
