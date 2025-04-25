from pydantic import BaseModel


class RoseIn(BaseModel):
    cat: str
    position: float
    size: float


class RoseOut(RoseIn):
    timestamp: float


class Rose(RoseOut):
    creator_ip: str

