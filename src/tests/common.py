from sqlalchemy import orm

from core.config import get_settings

TEST_SETTINGS = get_settings()
ALEMBIC_PATH = TEST_SETTINGS.PROJECT_ROOT
FACTORIES_SESSION = orm.scoped_session(orm.sessionmaker())
