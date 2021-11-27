from sqlalchemy.ext.asyncio import AsyncSession

from ..models import *


def add_department(session: AsyncSession, depo_id: int, depo_name: str):
    new_depo = Depo(id=depo_id, name=depo_name)
    session.add(new_depo)
    await session.commit()
    return new_depo
