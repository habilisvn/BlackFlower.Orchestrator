from fastapi import APIRouter


router = APIRouter(
    prefix="/api/v1/users",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)
