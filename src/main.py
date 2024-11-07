from contextlib import asynccontextmanager
from datetime import datetime
import os
from fastapi import FastAPI
import logging

from common.exception_handlers import final_error_handler
from user.representation.apis import router as user_router
from config.session import create_db_and_tables


log_folder = "logs"
os.makedirs(log_folder, exist_ok=True)
log_file_name = datetime.now().strftime("%Y-%m-%d.log")
### DOCUMENT: SQLAlchemy logger setup
# go with echo=False to avoid duplicate logs)
logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,  # Prevents disabling existing loggers
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
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
                "propagate": False,  # Allow logs to propagate to root and use root handlers
            },
        },
    }
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(user_router)

app.add_exception_handler(Exception, final_error_handler)
