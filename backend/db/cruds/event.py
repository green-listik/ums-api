
from datetime import datetime

def add_event(event_id: int, user_id: int, depo_id: int,
              theme: str, reason: str,
              event_date: datetime, place: str,
              responsible_person: str, speaker: str,
              key_event: bool, is_governor: bool,
              file_name: str
              ):
    pass


def edit_event(event_id: int,  user_id: int, depo_id: int):
    pass


def del_event(event_id: int,  user_id: int, depo_id: int):
    pass


def get_all_events(depo_id: int):
    pass