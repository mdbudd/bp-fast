from sqlalchemy import Boolean, Column, Float, String, Integer, MetaData, Table
from pydantic import BaseModel
from api.db import Base


class Login(BaseModel):
    username: str
    password: str


class Info(BaseModel):
    selection: str


class DBEmployee(Base):
    __tablename__ = "employee"

    salaryref = Column(Integer, primary_key=True, index=True)
    forename = Column(String(50), nullable=True)
    surname = Column(String(50), nullable=True)
    known_as = Column(String(50), nullable=True)
