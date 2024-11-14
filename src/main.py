import asyncio
from contextlib import asynccontextmanager
from datetime import datetime
import os
from fastapi import FastAPI
import logging

import uvloop

from common.exception_handlers import final_error_handler, value_error_handler
from common.exceptions import IsExistentException
from user.repr.api.user import router as user_router
from config.session import create_db_and_tables


log_folder = "logs"
os.makedirs(log_folder, exist_ok=True)
log_file_name = datetime.now().strftime("%Y-%m-%d.log")

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
        },
        "handlers": {
            "file": {
                "class": "logging.FileHandler",
                "filename": f"logs/{log_file_name}",
                "formatter": "default",
                "level": "INFO",
            },
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
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
