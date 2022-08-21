import typing as tp

from database import engine as engine_module
from sqlalchemy.ext.asyncio import AsyncEngine
from structlog import get_logger

logger = get_logger(__name__)


class BaseCRUD:
    engine: AsyncEngine = engine_module.engine

    @classmethod
    async def execute(
        cls, statement: tp.Any, values: tp.Union[list[dict], dict, None] = None
    ) -> tp.Any:
        async with cls.engine.begin() as conn:
            return await conn.execute(statement, parameters=values)
