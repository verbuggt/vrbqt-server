import logging
import pathlib
from logging.config import dictConfig
from typing import Union

import uvicorn.config
from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request

ENABLE_DOCUMENTATION = pathlib.Path.is_file(pathlib.Path("DOC_ENABLED"))
modules = {
    "core": True,
    "watchy": False,
    "dump": True,
    "roses": True,
    "dropi": True,
    "bike": False,
    "vlink": True,
    "gunter": False,
}

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": '%(levelprefix)s %(asctime)s :: %(client_addr)s - "%(request_line)s" %(status_code)s',
            "use_colors": True
        },
    },
    "handlers": {
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "uvicorn.access": {
            "handlers": ["access"],
            "level": "INFO",
            "propagate": False
        },
    },
}

dictConfig(logging_config)

app = FastAPI(docs_url="/doc" if ENABLE_DOCUMENTATION else None,
              openapi_url="/openapi.json" if ENABLE_DOCUMENTATION else None,
              redoc_url="/redoc" if ENABLE_DOCUMENTATION else None,
              )


if ENABLE_DOCUMENTATION:
    origins = [
        "http://0.0.0.0:8000",
        "http://127.0.0.1:8000",
        "http://localhost:8082"
    ]
else:
    origins = [
        "https://vrbqt.de",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["OPTIONS", "GET", "POST"],
    allow_headers=["*"]
)


@app.get('/api/ip')
def ip_echo(request: Request):
    return request.client.host


@app.get('/api/user_agent')
def user_agent_echo(user_agent: Union[str, None] = Header(default=None)):
    return user_agent


@app.get('/api/headers')
def client_headers_echo(request: Request):
    return request.headers


if modules['core']:
    import core

    app.include_router(core.core_router, prefix='/api')
    app.include_router(core.auth_router, prefix='/api')

if modules['watchy']:
    pass

if modules['dump']:
    import dump
    app.include_router(dump.dump_router, prefix="/api")

if modules['roses']:
    import roses

    app.include_router(roses.rose_router, prefix="/api")

if modules['dropi']:
    import dropi

    app.include_router(dropi.dropy_router, prefix='/api')

if modules['bike']:
    import bike

    app.include_router(bike.bike_router, prefix='/api')

if modules['vlink']:
    import vlink

    app.include_router(vlink.vlink_router, prefix='/api')

if modules['gunter']:
    import gunter

    app.include_router(gunter.vit_router, prefix='/api')
