from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import Depends, FastAPI
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session

from config.settings import get_settings
from src.user.representation.api import router as user_router


app = FastAPI()
app.include_router(user_router)

# Database setup
connect_args = {}
settings = get_settings()
engine = create_engine(settings.postgresql_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDependency = Annotated[Session, Depends(get_session)]


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
