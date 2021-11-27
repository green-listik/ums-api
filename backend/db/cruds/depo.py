from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import *


async def add_department(session: AsyncSession, depo_id: int, depo_name: str):
    new_depo = Depo(id=depo_id, name=depo_name)
    session.add(new_depo)
    await session.commit()
    return new_depo


async def get_depo_name(session: AsyncSession, name: str):
    department = await session.execute(select(Depo).where(Depo.name == name))
    return department.scalars().one()


async def get_depo_id(session: AsyncSession, depo_id: int):
    department = await session.execute(select(Depo).where(Depo.id == depo_id))
    return department.scalars().one()


async def get_all_departaments(session: AsyncSession):
    department = await session.execute(select(Depo))
    return department.scalars().all()
