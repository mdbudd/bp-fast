from fastapi import FastAPI, Depends, Response, Request, status, APIRouter, Security
from fastapi.security import HTTPBasicCredentials, HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import pandas as pd
import json
import os
import datetime
from typing import Optional, List
from sqlalchemy.orm import Session
from api.db import engine1, Session1

# from api.db import engine2, Session2, table1, table2, sesh
from models.people import Login, Info, DBEmployee
from models.places import DBPlace, Place
from api.utils import create_access_token, decode_token, verify_jwt
from packages.data.methods import get_db, get_place, get_places, get_employee_a, create_place

from api.jwt import JWTBearer

# security = HTTPBearer()
security = JWTBearer()

v0 = APIRouter(prefix="/api/v0", tags=["Authentication"])


@v0.post("/authenticate/*", status_code=200)
def login_view(login: Login, response: Response):
    domain, ident = ["mattbudd.co.uk", "mbudd"]
    administrators = ["mbudd"]
    if ident is None:
        response.status_code = 401
        return {"message": "Invalid credentials"}
    payload = {
        "iat": datetime.datetime.utcnow(),
        "jti": "f58b0243-24f3-427f-9e6f-39fa0a3a3896",
        "type": "access",
        "sub": ident,
        "nbf": datetime.datetime.utcnow(),
        # "aud": "matt.app",
        "iss": "PingAccessAuthToken",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
        "is_admin": any(item == ident for item in administrators),
        "domain": domain,
        # "roles": init["slxRoles"],
        # "srn": init["srn"],
        "impng": False,
    }

    token = create_access_token(payload)
    # response.status_code = 201
    return {"access_token": token}


# Routes for interacting with the API


@v0.post("/info/")
def info_view(info: Info, credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials
    data = {}

    print(verify_jwt(token))
    if verify_jwt(token):
        claims = decode_token(token)
        print(claims)
        try:
            selection = json.loads(info.selection)
            # print(selection)
            # data = getUser(claims, selection)
            data = [claims, selection]
            return data
        except json.decoder.JSONDecodeError:
            return {"error": "Invalid Json"}, 404
    return data


@v0.post("/places/*", response_model=Place)
def create_places_view(place: Place, db: Session = Depends(get_db)):
    print(place)
    db_place = create_place(db, place)
    return db_place


@v0.get("/places/*", response_model=List[Place])
def get_places_view(db: Session = Depends(get_db)):
    return get_places(db)


@v0.get("/place/{place_id}")
def get_place_view(place_id: int, db: Session = Depends(get_db)):
    return get_place(db, place_id)


# @app.get("/employee/{srn}")
# async def get_data_view(srn: int, db: Session = Depends(get_db2)):
#     return get_data(db, srn)


# @v0.get("/meta/{page_id}")
# async def get_meta_view(page_id: int):
#     # return id
#     return get_meta(page_id)


# @v0.get("/employee/{srn}")
# async def get_emp_view(
#     srn: int, credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db2)
# ):
#     # return id
#     print(credentials)
#     # return get_employee(srn)
#     return get_employee_a(db, srn)

# relook at vd for better code
@v0.get("/auth/")
async def get_auth_view():
    import jwt
    import datetime
    import base64
    from cryptography.hazmat.primitives import serialization

    payload = {
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7, seconds=0),
        "iat": datetime.datetime.utcnow(),
        "id": 123,
        "roles": ["admin"],
    }
    with open("certs/private.ec.key", "rb") as key_file:
        private_key = serialization.load_pem_private_key(key_file.read(), password=None)

    key = private_key.private_bytes(
        serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()
    )
    return jwt.encode(payload, key, algorithm="ES256")


@v0.post("/login/")
async def get_auth_view(token: str):
    import jwt

    with open("certs/public.pem", "rb") as key_file:
        public_key = key_file.read()

    return jwt.decode(token, public_key, algorithms=["ES256"])


@v0.get("/")
async def root():
    return {"message": "Hello World! "}
