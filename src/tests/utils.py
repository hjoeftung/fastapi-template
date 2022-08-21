import argparse
import contextlib
import os
import random
import types
import typing as tp
import uuid

import pydantic
import sqlalchemy_utils
from alembic import config as alembic_config

from tests import common as tests_common
from tests.common import TEST_SETTINGS


def get_fake_uuid(
    *,
    to_str: bool = True,
    constant: bool = False,
    seed: int = 0,
) -> tp.Union[uuid.UUID, str]:
    """Returns generated UUID for test objects

    If `constant=True`, returns the same uuid4
    """
    if constant:
        return "5000edcf-b2e7-4c32-b8ef-3f9bf6d9111f"

    rand = random.Random()
    rand.seed(seed)
    result = uuid.UUID(int=rand.getrandbits(128))
    return str(result) if to_str else result


def _ordering(reverse: bool = False) -> tp.Callable:
    return lambda x, y: (x >= y) if reverse else (x <= y)


def is_ordered(lst: list, key: tp.Callable, *, reverse: bool = False) -> bool:
    """
    Checks whether the list is sorted ascending

    If :reverse = True checks descending sorting

    :key - field to check for:
        lambda x: x.id
    Example:
        lst = [1,2,3]

        is_ordered(lst, lambda x: x)
    """
    return all(_ordering(reverse)(key(lst[i]), key(item)) for i, item in enumerate(lst[1:]))


def build_db_uri(db_name: str) -> str:
    return pydantic.PostgresDsn.build(
        scheme="postgresql",
        user=TEST_SETTINGS.POSTGRES_USER,
        host=TEST_SETTINGS.POSTGRES_HOST,
        port=str(TEST_SETTINGS.POSTGRES_PORT),
        password=TEST_SETTINGS.POSTGRES_PASSWORD,
        path=f"/{db_name}",
    )


@contextlib.contextmanager
def tmp_db(
    db_name: str,
    is_template: bool = False,
    from_template: str | None = None,
) -> tp.Generator[str, None, None]:
    """Generate a temporary db"""

    unique_suffix = str(uuid.uuid4())[:8]
    if is_template:
        db_name += f"_template_{unique_suffix}"
    else:
        db_name += f"_test_{unique_suffix}"

    db_url = build_db_uri(db_name)
    if sqlalchemy_utils.database_exists(db_url):
        sqlalchemy_utils.drop_database(db_url)

    sqlalchemy_utils.create_database(db_url, template=from_template)

    try:
        yield db_name
    finally:
        sqlalchemy_utils.drop_database(db_url)


def make_alembic_config(
    cmd_opts: tp.Union[argparse.Namespace, types.SimpleNamespace],
    base_path: str = tests_common.ALEMBIC_PATH,
) -> alembic_config.Config:
    """Load alembic config"""

    # Replace path to alembic.ini file to absolute
    if not os.path.isabs(cmd_opts.config):
        cmd_opts.config = os.path.join(base_path, cmd_opts.config)

    config = alembic_config.Config(
        file_=cmd_opts.config, ini_section=cmd_opts.name, cmd_opts=cmd_opts
    )

    # Replace path to alembic folder to absolute
    alembic_location = config.get_main_option("script_location")
    if not alembic_location:
        raise FileNotFoundError("env.py not found")

    if not os.path.isabs(alembic_location):
        config.set_main_option("script_location", os.path.join(base_path, alembic_location))
    if cmd_opts.pg_url:
        config.set_main_option("sqlalchemy.url", cmd_opts.pg_url)

    return config


def alembic_config_from_url(
    pg_url: str | None = None,
) -> alembic_config.Config:
    """
    Provides Python object, representing alembic.ini file.
    """
    cmd_options = argparse.Namespace(
        config="alembic.ini",
        name="alembic",
        pg_url=pg_url,
        raiseerr=False,
        x=None,
    )
    return make_alembic_config(cmd_options)
