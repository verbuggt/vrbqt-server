from pydantic import BaseModel


class BikeBase(BaseModel):
    bike_name: str


class BikeCreate(BikeBase):
    frame_serial_number: str
    name: str
    owner: str
    missing: str
