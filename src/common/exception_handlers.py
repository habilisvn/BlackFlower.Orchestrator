from fastapi.responses import JSONResponse
from sqlalchemy.exc import DBAPIError
from fastapi import Request
import logging

from common.exceptions import IsExistentException


logger = logging.getLogger(__name__)


async def final_error_handler(request: Request, exc: DBAPIError):
    logger.error(f"Final exception handler: {exc}")
    return JSONResponse(
        status_code=503,
        content={"detail": "Service temporarily unavailable"},
    )


async def value_error_handler(request: Request, exc: IsExistentException):
    return JSONResponse(status_code=400, content={"detail": str(exc).capitalize()})
