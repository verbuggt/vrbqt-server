from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel
from starlette.requests import Request

from dump import io

dump_router = APIRouter(
    prefix="/dump",
    tags=["dump"],
    dependencies=[],
    responses={404: {"warning": "Not found"}}
)

dump_key = open("dump_key.secret").read().strip()


@dump_router.get("/")
async def dump_index(request: Request):
    return {
        "app": "dump",
        "version": "0.0",
        "status": "if u spam ill print it out and send it to u",
        "author": "vrbqt",
    }


class Dump(BaseModel):
    dump_type: str
    dump_name: str
    dump_data: str | bytes


# dump
@dump_router.post("/dump", )
def dump(request: Request, web_dump: Dump):
    return io.dump(web_dump.dump_type, web_dump.dump_name, web_dump.dump_data)
