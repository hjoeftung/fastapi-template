import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

from core.config import get_settings


def init_sentry():
    sentry_sdk.init(
        dsn=get_settings().SENTRY_DSN,
        integrations=[
            LoggingIntegration(event_level=None),
            SqlalchemyIntegration(),
        ],
    )
