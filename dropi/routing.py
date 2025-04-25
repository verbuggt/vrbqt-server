import string
import time
from ctypes import CDLL, c_char_p

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.requests import Request

from core.database import get_db
from dropi import schemas, crud

dropy_router = APIRouter(
    prefix="/dropi",
    tags=["core"],
    dependencies=[],
    responses={404: {"warning": "Not found"}}
)


@dropy_router.get("/")
def dropi_index():
    return {
        "app": "dropi",
        "version": "0.3",
        "status": "dev/stable",
        "author": "verbuqqt",
    }


# create drop
@dropy_router.post("/cd")
def create_drop(request: Request, drop: schemas.DropCreate, db: Session = Depends(get_db)):
    # TODO is drop_is_password_encrypted necessary? probably yes... idk
    if bool(drop.drop_is_password_encrypted):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="password encryption is not supported yet :(")
    if drop.drop_status not in [0, 1]:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="only plaintext/source code is supported yet")
    if crud.get_drop(db, drop.drop_token):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="drop already exists")

    crud.create_drop(db, drop, request.client.host)
    return {
        "status": "success",
        "data": drop.json(include={"drop_data", "drop_token", "drop_type"})
    }


def pyval(unsafe: str, length: int, allowed: str = string.ascii_letters + string.digits):
    if length != 0 and length != len(unsafe):
        return False
    for char in unsafe:
        if char not in allowed:
            return False
    return True


# get drop
def cval(unsafe_string, length: int = 0, allowed_charaters: str = string.ascii_letters):
    validate_file = "dropi/photons/libuntitled.so"
    validate_c = CDLL(validate_file)
    if not validate_c.validate_string(c_char_p(bytes(unsafe_string, "utf-8")), length):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Validation Error. what u doing? hm°!°")


@dropy_router.get("/gd")
def get_drop(request: Request, tkn: str, db: Session = Depends(get_db)):
    cval(tkn)
    db_drop = crud.get_drop(db, tkn)
    # drop = DropGet(drop_data=db_drop.drop_data, drop_type=db_drop.drop_type, drop_status=db_drop.drop_status)
    if db_drop:
        return {
            "drop_data": db_drop.drop_data,
            "drop_type": db_drop.drop_type,
            "drop_status": db_drop.drop_status
        }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="drop not found")
