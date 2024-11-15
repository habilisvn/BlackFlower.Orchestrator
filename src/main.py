import asyncio
from contextlib import asynccontextmanager
from datetime import datetime
import os
from typing import Any, Awaitable, Callable
from fastapi import FastAPI, Request, Response
import logging
import json
import uvloop
from uvicorn.logging import ColourizedFormatter
from starlette.middleware.base import BaseHTTPMiddleware

from common.exception_handlers import (
    final_error_handler,
    value_error_handler,
)
from common.exceptions import IsExistentException
from user.router import router as user_router
from config.session import create_db_and_tables


log_folder = "logs"
os.makedirs(log_folder, exist_ok=True)
log_file_name = datetime.now().strftime("%Y-%m-%d.log")

# Create a custom log formatter to handle extra data


class CustomJsonFormatter(ColourizedFormatter):
    def format(self, record: logging.LogRecord) -> str:
        new_msg: dict[str, Any] = dict()

        # Convert the log message to a dictionary
        new_msg["time"] = self.formatTime(record, self.datefmt)
        new_msg["level"] = record.levelname
        new_msg["message"] = record.getMessage()

        # Add custom fields (extra data) to the log record if available
        if hasattr(record, "request"):
            new_msg["request"] = record.request  # type: ignore
        if hasattr(record, "error"):
            new_msg["error"] = record.error  # type: ignore
        if hasattr(record, "errors"):
            new_msg["errors"] = record.errors  # type: ignore

        # Create a new record with the formatted message
        new_record = logging.LogRecord(
            name=record.name,
            level=record.levelno,
            pathname=record.pathname,
            lineno=record.lineno,
            msg=f"Message: {json.dumps(new_msg)}",
            args=record.args,
            exc_info=record.exc_info,
            func=record.funcName
        )

        return super().format(new_record)


# DOCUMENT: SQLAlchemy logger setup
# go with echo=False to avoid duplicate logs)
logging.config.dictConfig(  # type: ignore
    {
        "version": 1,
        # Prevents disabling existing loggers
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": (
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                ),
            },
            "json": {
                "()": CustomJsonFormatter,
                "use_colors": True,
                "fmt": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            }
        },
        "handlers": {
            "file": {
                "class": "logging.FileHandler",
                "filename": f"logs/{log_file_name}",
                "formatter": "json",
                "level": "ERROR",
            },
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "json",
                "level": "INFO",
            },
        },
        "root": {
            "level": "INFO",
            "handlers": [
                "file",
                "console",
            ],  # Both file and console handlers for root logger
        },
        "loggers": {
            "sqlalchemy.engine": {
                "level": "INFO",  # Set to INFO to capture SQL statements
                "propagate": False,  # Allow logs to propagate to root
            },
            "fastapi.error_logger": {
                "handlers": ["file"],
                "level": "ERROR",
                "propagate": False,
            },
        },
    }
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()

    yield


# DOCUMENT: Set uvloop as the default event loop policy
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

app = FastAPI(lifespan=lifespan)
app.include_router(user_router)

app.add_exception_handler(
    IsExistentException, value_error_handler  # type: ignore
)
app.add_exception_handler(Exception, final_error_handler)  # type: ignore


# TEMPORARY: Remove this after
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


app.add_middleware(StoreRequestBodyMiddleware)
