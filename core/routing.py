import random
import time
from asyncio import sleep
from datetime import timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from core import schemas, crud, auth, models, access
from core.auth import get_user_from_jwt
from core.crud import get_user_by_name
from core.database import get_db
from core.models import User

# TODO dependencies
# TODO admin depend

# CORE ROUTING
core_router = APIRouter(
    prefix="/core",
    tags=["core"],
    dependencies=[Depends(auth.get_user_from_jwt)],
    responses={404: {"warning": "Not found"}}
)


@core_router.get("/")
def core_index():
    return {
        "app": "core",
        "version": "0.2",
        "status": "dev",
        "author": "verbuqqt",
    }


@core_router.get("/users/me", dependencies=[Depends(access.debug_access)])
async def read_current_user(current_user: models.User = Depends(get_user_from_jwt)):
    return schemas.User.from_orm(current_user)


@core_router.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="username already registered")  # delay (for sEcUrItY)? nö.
    return crud.create_user(db=db, user=user)


@core_router.get("/users/", response_model=List[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@core_router.get("/users/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# AUTHENTICATION ROUTING
auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"warning": "Not found"}}
)


@auth_router.get("/")
def auth_index():
    return {
        "app": "core_auth",
        "version": "0.0",
        "status": "unstable/untested",
        "author": "verbuqqt",
    }


@auth_router.post("/auth")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user: User = get_user_by_name(db, form_data.username)
    t1 = time.time()
    if not user or not auth.authenticate_user(user, bytes(form_data.password, "latin1")):
        if not user:
            await sleep(random.uniform(0.741021, 0.79))
        await sleep(random.uniform(0.0472, 0.1813))
        print(f'{time.time() - t1:.20f}')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    await sleep(random.uniform(0.1, 0.2))
    print(f'{time.time() - t1}')
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/register")
async def register():
    return "no"
