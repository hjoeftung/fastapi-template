from sqlalchemy.ext.asyncio import create_async_engine

from core.config import get_settings

engine = create_async_engine(get_settings().database_uri, pool_size=20)
