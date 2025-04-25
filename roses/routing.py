import time
from typing import List

from fastapi import APIRouter
from starlette.requests import Request

from roses import io, schemas
from roses.schemas import RoseIn

rose_router = APIRouter(
    prefix="/rose",
    tags=["rose"],
    dependencies=[],
    responses={404: {"warning": "Not found"}}
)


@rose_router.get("/")
async def roses_index(request: Request):
    return {
        "app": "roses",
        "version": "0.0",
        "status": "roses are red, violets are blue, this api is held together with shitty programming glue",
        "author": "vrbqt",
    }


# return json rose array
@rose_router.get("/get_roses", response_model=List[schemas.RoseOut])
def get_roses():
    return io.get_roses()


# create a new rose
@rose_router.post("/add_rose", response_model=schemas.RoseOut)
def add_rose(request: Request, rose_in: RoseIn):
    return io.add_rose(request.client.host, time.time(), rose_in.cat, rose_in.position, rose_in.size)

