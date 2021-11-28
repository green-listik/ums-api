import bcrypt as bcrypt
from sqlalchemy import Column, ForeignKey, DateTime, Boolean, TIMESTAMP
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy.orm import relationship
import datetime

from .config import Base


class DepoRoles(Base):
    __tablename__ = "depo_roles"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    depo_id = Column(Integer, ForeignKey('depos.id'))
    depo = relationship("Depo", backref="roles", lazy="joined")
    get_all_events = Column(Boolean, default=False)


class UserRoles(Base):
    __tablename__ = "user_roles"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    edit_events = Column(Boolean, default=False)
    edit_users = Column(Boolean, default=False)
    admin_service = Column(Boolean, default=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    login = Column(String, unique=True)
    hashed_pass = Column(String)
    last_name = Column(String)
    first_name = Column(String)
    patronymic = Column(String)
    depo_id = Column(Integer, ForeignKey('depos.id'))
    depo = relationship('Depo', backref='users', lazy="joined")
    role_id = Column(Integer, ForeignKey('user_roles.id'))
    role: UserRoles = relationship('UserRoles', backref='user', lazy="joined")


class Depo(Base):
    __tablename__ = "depos"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String)


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", backref="events", lazy="joined")
    depo_id = Column(Integer, ForeignKey('depos.id'))
    depo = relationship("Depo", backref="events", lazy="joined")
    theme = Column(String)
    theme_reason = Column(String)
    date = Column(DateTime)
    place = Column(String)
    responsible_person = Column(String)
    speaker = Column(String)
    main_event = Column(Boolean)
    is_guber = Column(Boolean)
    file_name = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.now())
