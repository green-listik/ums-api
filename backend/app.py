import os
import secrets

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path
import api_models
from config import ADMIN_LOGIN, ADMIN_PASWWORD
from files import writeXLSX, packZIP
from db.config import get_session, init_models
from security import verify_password, sign_jwt, JWTBearer, decode_jwt
from db.cruds.user import *
from db.cruds.depo import *
from db.cruds.event import *
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def get_user_from_jwt(session, token: str) -> User:
    data = decode_jwt(token)
    user = await get_user_id(session, data['user_id'])
    return user


@app.on_event("startup")
async def startup_event():
    # TODO   NOT FOR PRODUCTION
    await init_models()
    try:
        os.mkdir("files")
        os.mkdir("temp")
    except FileExistsError:
        pass
    session = await get_session()
    a = await register_user(session, ADMIN_LOGIN, ADMIN_PASWWORD, 'admin', 'admin', 'admin', 0, True, True, True)


@app.post("/uploadfile/", dependencies=[Depends(JWTBearer())])
async def create_upload_file(file: UploadFile = File(...), session: AsyncSession = Depends(get_session),
                             jwt=Depends(JWTBearer())):
    current_user = await get_user_from_jwt(session, jwt)

    file_name = os.getcwd() + "/files/" + file.filename.replace(" ", "-")
    new_filename = Path(file_name)
    temp = new_filename.stem + f'_{current_user.depo.name}'
    file_name = temp + new_filename.suffix
    with open(file_name, 'wb+') as f:
        f.write(file.file.read())
        f.close()

    return 'ok'


@app.post("/add_user", dependencies=[Depends(JWTBearer())])
async def add_user(user: api_models.User, session: AsyncSession = Depends(get_session), jwt=Depends(JWTBearer())):
    current_user = await get_user_from_jwt(session, jwt)
    if current_user.role.admin_service:
        res = await register_user(session, user.login, user.password, user.last_name, user.first_name,
                                  user.second_name, user.depo_id)
        return {'login': user.login, 'password': user.password}
    if current_user.role.edit_users and current_user.depo.id == user.depo_id and not user.admin_service:
        res = await register_user(session, user.login, user.password, user.last_name, user.first_name,
                                  user.second_name, current_user.depo_id)
        return {'login': user.login, 'password': user.password}
    return {'error': 'Not enough rights'}


@app.post("/login")
async def login(user: api_models.UserLoginSchema, session: AsyncSession = Depends(get_session)):
    res = await get_user_login(session, user.login)
    if res:
        if verify_password(user.password, res.hashed_pass):
            return sign_jwt(res.id)
    return {
        "error": "Wrong login details!"
    }


@app.post("/add_depo", dependencies=[Depends(JWTBearer())])
async def add_depo(depo: api_models.Depo, session: AsyncSession = Depends(get_session),
                   jwt=Depends(JWTBearer())):
    user = await get_user_from_jwt(session, jwt)
    if user.role.admin_service:
        await add_department(session, depo.name)
        res = await get_depo_name(session, depo.name)
        return res.id
    return {'error': 'Not enough rights'}


@app.post("/add_event", dependencies=[Depends(JWTBearer())])
async def add_event(event: api_models.Event,
                    session: AsyncSession = Depends(get_session), jwt=Depends(JWTBearer())):
    user = await get_user_from_jwt(session, jwt)
    file_name = os.getcwd() + "/files/" + event.file_name.replace(" ", "-")
    new_filename = Path(file_name)
    temp = new_filename.stem + f'_{user.depo.name}'
    file_name = temp + new_filename.suffix
    res = await create_event(session, user.id, user.depo_id, event.theme, event.reason, event.date, event.place,
                             event.res_person, event.speaker, event.isImportant, event.isGubernator, file_name)
    return 'ok'


@app.post("/get_events", dependencies=[Depends(JWTBearer())])
async def get_events(depo: api_models.Depo = None, session: AsyncSession = Depends(get_session),
                     jwt=Depends(JWTBearer())):
    user = await get_user_from_jwt(session, jwt)
    if depo and user.role.admin_service:
        res = await get_depo_name(session, depo.name)
        events = await get_events_depo(session, res.id)
    else:
        events = await get_events_depo(session, user.depo_id)
    res = []
    for i in events:
        temp = {'id': i.id, 'username': f"{i.user.last_name} {i.user}", 'theme': i.theme,
                'theme_reason': i.theme_reason, 'date': i.date, 'place': i.place,
                'responsible_person': i.responsible_person, 'speaker': i.speaker, 'main_event': i.main_event,
                'is_guber': i.is_guber, 'filename': i.file_name, 'created_at': i.created_at}
        res.append(temp)
    return res


@app.get('/get_zip', dependencies=[Depends(JWTBearer())])
async def get_zip(session: AsyncSession = Depends(get_session), jwt=Depends(JWTBearer())):
    user = await get_user_from_jwt(session, jwt)
    if user.role.admin_service:
        res = []
        events = await get_events_all(session)
        for i in events:
            temp = {'theme': i.theme,
                    'theme_reason': i.theme_reason, 'date': i.date, 'place': i.place,
                    'responsible_person': i.responsible_person, 'speaker': i.speaker, 'isImportant': i.main_event,
                    'isGubernator': i.is_guber}
            res.append(temp)
        xls_filename = writeXLSX(res)
        zip_filename = packZIP(xls_filename)
        return FileResponse(zip_filename)


@app.get("/get_depos", dependencies=[Depends(JWTBearer())])
async def get_depos(session: AsyncSession = Depends(get_session), jwt=Depends(JWTBearer())):
    user = await get_user_from_jwt(session, jwt)
    if user.role.admin_service:
        depos = await get_all_departaments(session)
        res = []
        for i in depos:
            temp = {'id': i.id, 'name': i.name}
            res.append(temp)
        return res
    return {'error': 'Not enough rights'}


if __name__ == '__main__':
    uvicorn.run(app)
