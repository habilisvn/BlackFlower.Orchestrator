import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from alembic import context  # type: ignore

from config.settings import get_settings
from common.base import Base
from sqlalchemy.ext.asyncio import async_engine_from_config

# DOCUMENT: don't remove this import

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config  # type: ignore

settings = get_settings()
config.set_main_option(  # type: ignore
    "sqlalchemy.url",
    f"{settings.postgresql_prefix_async}://"
    f"{settings.postgresql_username}:"
    f"{settings.postgresql_password}@"
    f"{settings.postgresql_host}:"
    f"{settings.postgresql_port}/"
    f"{settings.postgresql_db_name}",
)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:  # type: ignore
    fileConfig(config.config_file_name)  # type: ignore

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")  # type: ignore
    context.configure(  # type: ignore
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():  # type: ignore
        context.run_migrations()  # type: ignore


def do_run_migrations(connection):
    print(f"Metadata: {target_metadata}")
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        print("Running migrations")
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        print("Running migrations")
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    asyncio.run(run_async_migrations())


if context.is_offline_mode():  # type: ignore
    print("Offline mode")
    run_migrations_offline()
else:
    print("Online mode")
    run_migrations_online()
