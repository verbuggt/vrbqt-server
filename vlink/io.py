import json
import os.path
import pathlib
import time
from typing import Optional

from fastapi import HTTPException
from starlette import status

import util


def get_links(file):
    try:
        l: dict = json.loads(file.read(100000), )
    except json.decoder.JSONDecodeError:
        l: dict = {}
    return l


# TODO use database instead of horrible file stuff
def open_links_file():
    return open("vlink/data/links.json", "r+", encoding="utf-8")


pathlib.Path('./vlink/data/').mkdir(parents=True, exist_ok=True)


# TODO use database instead of horrible file stuff
def write_links_to_disk(file, data):
    file.truncate()
    file.write(json.dumps(data))
    file.flush()
    file.close()


def create_link(vlink_id: str, redirect, created_by: str):
    links = get_links(open_links_file())

    if vlink_id in links:
        raise HTTPException(status.HTTP_409_CONFLICT, "vlink_id already exists")
    if not vlink_id.isalpha():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "vlink_id is invalid")
    if not util.validate_url(redirect):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "redirect url is invalid")

    # update links with VLINK_ID: [IP, TIMESTAMP, REDIRECT_URL]
    created_at = time.time()
    vlink = {vlink_id: {"created_by": created_by, "created_at": created_at, "url": redirect}}
    links.update(vlink)

    # write stuff to file
    write_links_to_disk(open_links_file(), links)
    return vlink


def read_link(vlink_id) -> Optional[dict]:
    links = get_links(open_links_file())

    if vlink_id not in links.keys():
        return None
    return links.get(vlink_id)
