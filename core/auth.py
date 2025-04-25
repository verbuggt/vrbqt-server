import random
import secrets
import string
from datetime import timedelta, datetime
from typing import Union

import bcrypt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

from core import models
from core.database import get_db
from core.models import User

ALGORITHM = "HS256"
SECRET_KEY = "".join([secrets.choice(string.ascii_letters + string.digits) for _ in range(128)])
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fixed_offsets = [-9, 11, -18, -9, 7, 5, -14, 15, 10]
bcrypt_limit = 72
min_pw_length = 8
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

random = random.SystemRandom()


def authenticate_user(user: User, password: bytes) -> bool:
    return bcrypt.checkpw(pepper_pw(password, user.auth.scramble), user.auth.bcrypt_hash)


def gen_salt(rounds=14) -> bytes:
    return bcrypt.gensalt(rounds)


# TODO fuck off with password length. generate scramble randomly!
def gen_scramble(pl: int):
    scramble = ""
    sub = random.randint(33, 126)
    offset = random.randint(33, 79)
    scramble += chr(offset + sub) + chr(sub)
    for i in range(4):
        scramble += chr(random.randrange(1, pl) + offset + fixed_offsets[i])
    for i in range(5):
        scramble += chr(random.randrange(0, 72 - pl) + offset + fixed_offsets[4 + i])
    return scramble


# TODO adapt to improved scramble when implemented
def pepper_pw(password: bytes, scramble: str) -> bytes:
    scramble_offset = ord(scramble[0]) - ord(scramble[1])

    pass_indices = [0] + \
                   [ord(scramble[i]) - scramble_offset - fixed_offsets[i - 2] for i in range(2, 6)] + \
                   [len(password)]
    pass_indices.sort()

    pepper_indices = [
                         ord(scramble[i]) - scramble_offset - fixed_offsets[i - 2]
                         for i in range(6, 11)
                     ] + [72 - len(password)]
    pepper_indices.sort()

    scramble_vals = [(pass_indices[i], pass_indices[i + 1]) for i in range(0, 5)]
    pepper_vals = [(pepper_indices[i], pepper_indices[i + 1]) for i in range(0, 5)]

    pepper = bytes(open('pepper.key').read(72), 'latin1')

    pass_split = [s for s in [password[i:j] for (i, j) in scramble_vals]]
    pepper_split = [s for s in [pepper[i:j] for (i, j) in pepper_vals]]

    return b''.join([pepper_split[i] + pass_split[i] for i in range(5)])


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_user_from_jwt(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    validation_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Validation Error",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # decode token and extract the values
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        exp = payload.get("exp")

        # check if jwt contains all necessary fields, if not abort
        if not username or not exp:
            raise validation_error

        # check if token is expired, if so, abort
        if datetime.utcnow() >= datetime.fromtimestamp(exp):
            raise validation_error
    except JWTError:
        raise validation_error

    # get db user - abort
    from core.crud import get_user_by_name
    user: models.User = get_user_by_name(db, username)
    if not user:
        # TODO This should never happen. add debug if it does
        raise validation_error
    return user
