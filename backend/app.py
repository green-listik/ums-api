from fastapi import FastAPI, Depends
from api_models import *
from backend.db.config import get_session
from db import config
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()


@app.post("/register")
async def register(user: User, session: AsyncSession = Depends(get_session)):
    pass


@app.post("/login")
async def login(user: User, session: AsyncSession = Depends(get_session)):
    pass


@app.post("/add_depo")
async def add_depo(depo: Depo, session: AsyncSession = Depends(get_session)):
    pass


@app.post("/add_user")
async def add_user(user: User, depo: Depo, session: AsyncSession = Depends(get_session)):
    pass


@app.post("/add_event")
async def add_event(user: User, event: Event, depo: Depo, session: AsyncSession = Depends(get_session)):
    pass


@app.get("/get_events", response_model=list[Event])
async def get_events(session: AsyncSession = Depends(get_session)):
    pass


@app.get("/get_depos", response_model=list[Depo])
async def get_depos(session: AsyncSession = Depends(get_session)):
    pass
