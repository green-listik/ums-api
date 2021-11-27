from sqlalchemy import select
from datetime import datetime
from ..models import *
from sqlalchemy.ext.asyncio import AsyncSession


async def add_event(session: AsyncSession, event_id: int, user_id: int, depo_id: int,
                    theme: str, reason: str,
                    event_date: datetime, place: str,
                    responsible_person: str, speaker: str,
                    key_event: bool, is_governor: bool,
                    file_name: str):
    pass


async def edit_event(event_id: int, user_id: int, depo_id: int):
    pass


def del_event(event_id: int, user_id: int, depo_id: int):
    pass


def get_all_events(session: AsyncSession, depo_id: int):
    res = await session.execute(select)
