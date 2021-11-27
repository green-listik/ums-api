from pydantic import BaseModel


class User(BaseModel):
    name: str
    login: str
    password: str
    last_name: str
    first_name: str
    second_name: str


class Depo(BaseModel):
    name: str


class Event(BaseModel):
    user: str
    depo: str
    theme: str
    reason: str
    date: int
    place: str
    res_person: str
    speaker: str
    isImportant: bool
    isGubernator: bool
    file_name: str
    created_date: int
