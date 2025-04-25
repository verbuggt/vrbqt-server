import bcrypt
from fastapi import HTTPException
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import Session
from starlette import status

from . import models, schemas, auth


# USER
def create_user(db: Session, user: schemas.UserCreate):
    # check pw
    if len(user.password) < 8:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "password is to short")

    db_user = models.User(username=user.username, is_admin=False)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    salt = bcrypt.gensalt(14)
    scramble = auth.gen_scramble(len(user.password))
    hashed_password = bcrypt.hashpw(auth.pepper_pw(user.password, scramble), salt)
    db_user_auth = models.Auth(user_id=db_user.user_id, bcrypt_hash=hashed_password, scramble=scramble)
    db.add(db_user_auth)
    db.commit()
    db.refresh(db_user_auth)

    return db_user


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()


def get_user_by_name(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users


def get_permission(db: Session, permission_name: str):
    try:
        p = db.query(models.Permission).filter(models.Permission.permission_name == permission_name).first()
    except ProgrammingError:
        return None
    return p
