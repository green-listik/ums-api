from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import *

from datetime import datetime

async def add_event(session: AsyncSession, event_id: int, user: User, depo: Depo,
              theme: str, reason: str,
              event_date: datetime, place: str,
              responsible_person: str, speaker: str,
              main_event: bool, is_governor: bool,
              file_name: str
              ):
    new_event = Event(id=event_id, user=user, depo=depo, theme=theme, theme_reason=reason,
                      date=event_date, place=place, responsible_person=responsible_person,
                      speaker=speaker, main_event=main_event, is_guber=is_governor, file_name=file_name)
    session.add(new_event)
    await session.commit()
    return new_event


async def get_event(session: AsyncSession, event_id: int):
    event = await session.execute(select(Event).where(Event.id == event_id))

    return event.scalars().one()


async def edit_event(session: AsyncSession, event_id: int,  user_id: int, depo_id: int):
    pass


async def get_all_events(session: AsyncSession):
    events = await session.execute(select(Event))
    return events.scalars().all()


async def get_depo_events(session: AsyncSession, depo_id: int):
    events = await session.execute(select(Event).where(Event.depo.id == depo_id))
    return events.scalars().all()