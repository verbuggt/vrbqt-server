from fastapi import APIRouter

bike_router = APIRouter(
    prefix="/bike",
    tags=["bike"],
    # dependencies=[Depends(auth.oauth2_scheme)],
    responses={404: {"warning": "Not found"}}
)
