import asyncio
import os
from importlib import reload
from types import SimpleNamespace
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from alembic import command as alembic_command
from alembic.config import Config
from database import engine as engine_module
from fastapi import FastAPI
from httpx import AsyncClient
from requests import Session as RequestSession
from sqlalchemy import create_engine
from starlette.testclient import TestClient

from crud.base import BaseCRUD
from tests import utils as test_utils
from tests.common import FACTORIES_SESSION, TEST_SETTINGS
from tests.utils import make_alembic_config


@pytest.fixture(scope="session")
def event_loop():
    """
    Creates event loop for tests.
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    yield loop
    loop.close()


@pytest.fixture(scope="session")
def template_db() -> AsyncGenerator[str, None]:
    with test_utils.tmp_db(db_name=TEST_SETTINGS.POSTGRES_DB, is_template=True) as tmp_name:
        os.environ["POSTGRES_DB"] = tmp_name
        tmp_url = test_utils.build_db_uri(tmp_name)
        alembic_config_ = test_utils.alembic_config_from_url(tmp_url)
        alembic_command.upgrade(alembic_config_, "head")
        yield tmp_name
        os.environ["POSTGRES_DB"] = TEST_SETTINGS.POSTGRES_DB


@pytest.fixture(autouse=True)
def migrated_db(
    template_db: str,
) -> AsyncGenerator[str, None]:  # pylint: disable=redefined-outer-name
    with test_utils.tmp_db(
        db_name=TEST_SETTINGS.POSTGRES_DB, from_template=template_db
    ) as tmp_name:
        os.environ["POSTGRES_DB"] = tmp_name
        reload(engine_module)
        BaseCRUD.engine = engine_module.engine
        engine = create_engine(test_utils.build_db_uri(tmp_name))
        FACTORIES_SESSION.configure(bind=engine)
        yield tmp_name
        FACTORIES_SESSION.remove()
        engine.dispose()
        os.environ["POSTGRES_DB"] = TEST_SETTINGS.POSTGRES_DB


@pytest.fixture
def empty_db() -> str:
    with test_utils.tmp_db(db_name=TEST_SETTINGS.POSTGRES_DB) as tmp_name:
        yield test_utils.build_db_uri(tmp_name)


@pytest.fixture
def alembic_config(empty_db: str) -> Config:
    """
    Создает файл конфигурации для alembic.
    """
    cmd_options = SimpleNamespace(
        config="alembic.ini",
        name="alembic",
        pg_url=empty_db,
        raiseerr=False,
        x=None,
    )
    return make_alembic_config(cmd_options)


@pytest_asyncio.fixture
async def async_client(app: FastAPI, client: TestClient) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url=client.base_url) as async_test_client:
        yield async_test_client


@pytest.fixture
def client(app: FastAPI) -> Generator[RequestSession, None, None]:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def app() -> FastAPI:
    from main import app as fastapi_app

    return fastapi_app
