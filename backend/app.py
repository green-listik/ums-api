import secrets

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status

import api_models
from db.config import get_session, init_models
from errors import AuthError
from security import verify_password, sign_jwt, get_hash_password
from db.cruds.user import *
from db.cruds.depo import *
from db import config
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await init_models()
    # session = await get_session()
    # a = await register_user(session, 'sadfsad', 'asdf', 'asdfsadf', 'asdfsda', 'asdf', depo_id=1)
    # print(a.last_name)



@app.post("/register")
async def register(user: api_models.User):
    session = await get_session()
    res = await register_user(session, user.login, user.password, user.last_name, user.first_name,
                              user.second_name, user.depo_id)
    return {'login': user.login, 'password': user.password}


@app.post("/login")
async def login(user: api_models.UserLoginSchema, session: AsyncSession = Depends(get_session)):
    res = await get_user_login(session, user.login)
    if res:
        return sign_jwt(res.id)
    return {
        "error": "Wrong login details!"
    }


@app.post("/add_depo")
async def add_depo(depo: api_models.Depo, session: AsyncSession = Depends(get_session)):
    res = await add_department(session, depo.name)
    return res


@app.post("/add_user")
async def add_user(user: api_models.User, depo: api_models.Depo, session: AsyncSession = Depends(get_session)):
    pass


@app.post("/add_event")
async def add_event(user: api_models.User, event: api_models.Event, depo: api_models.Depo,
                    session: AsyncSession = Depends(get_session)):
    pass


@app.get("/get_events", response_model=list[api_models.Event])
async def get_events(session: AsyncSession = Depends(get_session)):
    pass


@app.get("/get_depos", response_model=list[api_models.Depo])
async def get_depos(session: AsyncSession = Depends(get_session)):
    pass


if __name__ == '__main__':
    uvicorn.run(app)
