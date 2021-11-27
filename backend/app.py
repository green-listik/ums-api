from fastapi import FastAPI
from pydantic import BaseModel
# from fastapi_asyncalchemy import service
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()

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

@app.post("/register")
async def register(user: User, session: AsyncSession):
	pass

@app.post("/login")
async def login(user: User, session: AsyncSession):
	pass

@app.post("/add_depo")
async def add_depo(depo: Depo, session: AsyncSession):
	pass

@app.post("/add_user")
async def add_user(user: User, depo: Depo, session: AsyncSession):
	pass

@app.post("/add_event")
async def add_event(user: User, event: Event, depo: Depo, session: AsyncSession):
	pass

@app.get("/get_events", response_model = list[Event])
async def get_events(session: AsyncSession):
	pass

@app.get("/get_depos", response_model = list[Depo])
async def get_depos(session: AsyncSession):
	pass