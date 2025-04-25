import datetime

from sqlalchemy.orm import Session

from dropi import models
from dropi.models import Drop, DropStatus, DropType
from dropi.schemas import DropCreate, DropBase, DropDelete



def get_drop(db: Session, drop_token: str) -> Drop:
    db_drop: Drop = db.query(Drop).get(drop_token)
    return db_drop


def update_drop(db: Session, drop: DropBase):
    pass


def _verify_drop_type(drop_data, drop_type):
    pass


def create_drop(db: Session, drop: DropCreate, crated_by_ip_address):
    drop_data = bytes(drop.drop_data)
    drop_type = DropType(drop.drop_type)
    drop_status = DropStatus(drop.drop_status)
    drop_is_password_protected = drop.drop_is_password_encrypted
    drop_token = drop.drop_token

    db_drop = models.Drop(drop_status=drop_status, drop_type=drop_type,
                          drop_is_password_protected=drop_is_password_protected, drop_views=1, drop_data=drop_data,
                          drop_token=drop_token, drop_created_by_user="anon", drop_created_by_ip=crated_by_ip_address,
                          created_at=datetime.datetime.now())

    db.add(db_drop)
    db.commit()
    db.refresh(db_drop)
    return drop


def delete_drop(db: Session, drop: DropDelete):
    pass
