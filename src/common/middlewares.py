from typing import Awaitable, Callable
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response


class StoreRequestBodyMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]]
    ):
        # Read the body as bytes
        request_body = await request.body()

        # Store the body in request.state
        request.state.body = request_body  # Save the raw body for the handler

        # Call the next handler in the middleware chain
        response = await call_next(request)
        return response
