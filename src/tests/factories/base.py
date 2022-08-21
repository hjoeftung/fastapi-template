import asyncio

import factory
from factory import fuzzy

from tests import common as tests_common


class Base(factory.alchemy.SQLAlchemyModelFactory):
    id = fuzzy.FuzzyInteger(1, 10**8)  # noqa: A003

    @classmethod
    def _create(cls, model_class, **kwargs):
        async def create_coro(**kwargs):
            instance = cls._meta.model(**kwargs)
            async with tests_common.TestGlobalSession() as session:
                async with session.begin():
                    session.add(instance)
                await session.commit()
            return instance

        return asyncio.create_task(create_coro(**kwargs))
