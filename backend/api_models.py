from typing import Optional

from pydantic import BaseModel, Field


class User(BaseModel):
    depo_id: int
    name: str
    login: str
    password: str
    last_name: str
    first_name: str
    second_name: str


class UserLoginSchema(BaseModel):
    login: str
    password: str


class Depo(BaseModel):
    name: str


class Event(BaseModel):
    theme: str
    reason: str
    date: int
    place: str
    res_person: str
    speaker: str
    isImportant: bool
    isGubernator: bool
