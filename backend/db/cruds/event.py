from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import *


async def create_event(session: AsyncSession, user_id, depo_id,
                       theme: str, reason: str,
                       event_date: datetime, place: str,
                       responsible_person: str, speaker: str,
                       main_event: bool, is_governor: bool,
                       file_name: str
                       ):
    new_event = Event(theme=theme, theme_reason=reason,
                      date=event_date, place=place, responsible_person=responsible_person,
                      speaker=speaker, main_event=main_event, is_guber=is_governor, file_name=file_name,
                      depo_id=depo_id, user_id=user_id)
    session.add(new_event)
    await session.commit()
    return new_event


async def get_event_id(session: AsyncSession, event_id: int):
    event = await session.execute(select(Event).where(Event.id == event_id))

    return event.scalars().first()


async def edit_event(session: AsyncSession, event_id: int, theme: str, reason: str,
                     event_date: datetime, place: str,
                     responsible_person: str, speaker: str,
                     main_event: bool, is_governor: bool,
                     file_name: str):
    event: Event = await get_event_id(session, event_id)

    event.theme = theme
    event.theme_reason = reason
    event.event_date = event_date
    event.place = place
    event.responsible_person = responsible_person
    event.speaker = speaker
    event.main_event = main_event
    event.is_guber = is_governor
    event.file_name = file_name

    await session.commit()
    return event


async def get_events_all(session: AsyncSession):
    events = await session.execute(select(Event))
    return events.scalars().all()


async def get_events_depo(session: AsyncSession, depo_id: int):
    events = await session.execute(select(Event).where(Event.depo.id == depo_id))
    return events.scalars().all()


async def get_events_user_id(session: AsyncSession, user_id: int):
    events = await session.execute(select(Event).where(Event.user.id == user_id))
    return events.scalars().all()


async def get_events_user_name(session: AsyncSession, user_name: str):
    events = await session.execute(select(Event).where(Event.user.name == user_name))
    return events.scalars().all()


async def get_events_user(session: AsyncSession, user: User):
    events = await session.execute(select(Event).where(Event.user == user))
    return events.scalars().all()


async def get_events_place(session: AsyncSession, place: str):
    events = await session.execute(select(Event).where(Event.place == place))
    return events.scalars().all()


async def get_events_is_guber(session: AsyncSession, place: str):
    events = await session.execute(select(Event).where(Event.place == place))
    return events.scalars().all()
