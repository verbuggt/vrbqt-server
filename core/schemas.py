from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: bytes


class User(UserBase):
    display_name: str

    class Config:
        orm_mode = True
