import secrets
import string

import bcrypt
from sqlalchemy.orm import Session

import core.auth
import core.crud
import core.database
from core.database import Base
from core.models import User, Auth, Permission


# DELETES EVERYTHING! BE CAREFUL, IDIOT
def drop_db():
    print("Hey. You are about to delete every bit of data in the database.")
    print("Are you ABSOLUTELY SURE you want to do this?")
    input()
    idiot_proofing = input("Please enter 'Yes I know what I'm doing and can't deny responsibility' or 'yes' ")
    if idiot_proofing == "Yes I know what I'm doing and can't deny responsibility" or idiot_proofing.lower() == "yes":
        print("deleting...")
        db: Session = next(core.database.get_db())
        Base.metadata.drop_all(bind=db.bind)
        print("deleted.")
    else:
        print("confirmation failed.")


def gen_password(length=16) -> bytes:
    return b''.join(bytes(secrets.choice(string.ascii_letters + string.digits), "utf8") for _ in range(length))


def create_user(user_name: str, display_name: str = None, password: bytes = None):
    db: Session = next(core.database.get_db())

    if not display_name:
        display_name = user_name

    new_user = User(username=user_name, display_name=display_name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    if not password:
        password = gen_password()
        print("Password for the new user:", password)

    salt = bcrypt.gensalt(14)
    scramble = core.auth.gen_scramble(len(password))
    hashed_password = bcrypt.hashpw(core.auth.pepper_pw(password, scramble), salt)
    auth = Auth(user_id=new_user.user_id, bcrypt_hash=hashed_password, scramble=scramble)
    db.add(auth)
    db.commit()
    db.refresh(auth)

    print("user created.")


# TODO cleanup. create_auth func etc
def change_password(user_id: int, new_password: bytes):
    db: Session = next(core.database.get_db())
    user: User = core.crud.get_user(db, user_id=user_id)
    db.delete(user.auth)

    salt = bcrypt.gensalt(14)
    scramble = core.auth.gen_scramble(len(new_password))
    hashed_password = bcrypt.hashpw(core.auth.pepper_pw(new_password, scramble), salt)
    auth = Auth(user_id=user_id, bcrypt_hash=hashed_password, scramble=scramble)
    db.add(auth)
    db.commit()


def add_permission_to_user(user_id: int, permission_name: str, app_name: str = None):
    db: Session = next(core.database.get_db())
    user: User = core.crud.get_user(db, user_id)
    permission: Permission = core.crud.get_permission(db, permission_name, app_name)
    user.permissions.append(permission)
    db.commit()
    db.refresh(user)
