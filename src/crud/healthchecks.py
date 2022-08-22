import typing as tp

import sqlalchemy as sa

from crud.base import BaseCRUD


class HealthChecksCRUD(BaseCRUD):
    @classmethod
    async def check_database(cls) -> tp.Literal[1] | None:
        query = sa.text("SELECT 1")
        result = await cls.execute(query)
        if one := result.fetchone():
            return one[0]
        return None
