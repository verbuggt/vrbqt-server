import enum

from pydantic import BaseModel


class DropBase(BaseModel):
    drop_data: bytes
    drop_type: int
    drop_status: int

    class Config:
        orm_mode = True


class DropGet(DropBase):
    drop_token: str


class DropCreate(DropBase):
    drop_is_password_encrypted: bool
    drop_token: str


class DropDelete:
    drop_token: bytes
    pass
