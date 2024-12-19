from fastapi.responses import JSONResponse
from fastapi import Request
import logging

from common.exceptions import IsExistentException


logger = logging.getLogger(__name__)


async def get_request_data(request: Request):
    """Helper function to read and return request data for logging."""
    # Access the stored request body from the middleware
    if request.state.body and b"file" in request.state.body:
        request_body = "<file upload>"
    else:
        request_body = (
            request.state.body.decode("utf-8")
            if request.state.body
            else "<empty body>"
        )

    request_data = {
        "method": request.method,
        "url": str(request.url),
        "headers": dict(request.headers),
        "body": request_body,
        "query_params": dict(request.query_params),
    }
    return request_data


async def final_error_handler(request: Request, exc: Exception):
    request_data = await get_request_data(request)

    logger.error(f"Exception: {exc}", extra={"request": request_data})
    return JSONResponse(
        status_code=503,
        content={"detail": "Service temporarily unavailable"},
    )


async def value_error_handler(request: Request, exc: IsExistentException):
    return JSONResponse(
        status_code=400, content={"detail": str(exc).capitalize()}
    )
