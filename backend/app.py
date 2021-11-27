import secrets

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasicCredentials, HTTPBasic

import api_models
from backend.db.config import get_session
from backend.errors import AuthError
from backend.security import verify_password
from db.cruds.user import *
from db import config
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()
security = HTTPBasic()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    session = Depends(get_session)
    user = await get_user_by_login(session, credentials.username)
    if not user:
        raise AuthError
    correct_password = verify_password(credentials.password, user.password)
    if not correct_password:
        raise AuthError
    return user


@app.post("/register")
async def register(user: api_models.User, session: AsyncSession = Depends(get_session)):
    await register_user(session, user.login, user.password, user.last_name, user.first_name, user.second_name)
    return {"message": "ok"}


@app.post("/login")
async def login(user: User, dep):



@app.post("/add_depo")
async def add_depo(depo: api_models.Depo, session: AsyncSession = Depends(get_session)):
    pass


@app.post("/add_user")
async def add_user(user: User, depo: api_models.Depo, session: AsyncSession = Depends(get_session)):
    pass


@app.post("/add_event")
async def add_event(user: User, event: api_models.Event, depo: api_models.Depo,
                    session: AsyncSession = Depends(get_session)):
    pass


@app.get("/get_events", response_model=list[api_models.Event])
async def get_events(session: AsyncSession = Depends(get_session)):
    pass


@app.get("/get_depos", response_model=list[api_models.Depo])
async def get_depos(session: AsyncSession = Depends(get_session)):
    pass
