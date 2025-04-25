from typing import Union, Optional
from urllib import parse
from fastapi import APIRouter, HTTPException, Query, Path
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse
from util.security import load_secret_str

import util
from vlink import io

# TODO fix bad. this is bad. no hardcoded key thingies. don't commit that.
keys = load_secret_str("vlink.access_key").split("\n")

vlink_router = APIRouter(
    prefix="/vlink",
    tags=["vlink"],
    dependencies=[],
    responses={404: {"warning": "Not found"}}
)


@vlink_router.get("/")
async def core_index(request: Request):
    return {
        "app": "vlink",
        "version": "0.1",
        "status": "dev",
        "author": "verbuqqt",
    }


@vlink_router.get("/{vlink_id}/")
async def redirect_link(vlink_id: str):
    vlink = io.read_link(vlink_id)
    if not vlink:
        raise HTTPException(status_code=404, detail="vlink not found")
    return {
        "url": vlink['url']
    }


@vlink_router.post("/cv")
async def create_vlink(request: Request, rurl: str):
    vlid = request.query_params.get('vlid')
    print(request.path_params, request.query_params)
    key_header = str(request.headers.get("X-API-Key"))
    if not key_header or key_header not in keys:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Authentication required")
    if not vlid:
        vlid = util.get_random_str(6)
    tries = 0
    while io.read_link(vlid) is not None:
        tries += 1
        if tries > 3:
            vlid = util.get_random_str(12)
            continue
        vlid = util.get_random_str(6)
    io.create_link(vlid, rurl, request.client.host)
    return {
        vlid: {
            "url": parse.urljoin(str(request.base_url), vlid),
            "redirect_url": rurl,
        }
    }
