from sqlalchemy.orm import Session

from . import models, schemas


def get_bike(db: Session, bike_id: int):
    pass


def get_bike_by_serial(db: Session, bike_serial: str):
    pass
