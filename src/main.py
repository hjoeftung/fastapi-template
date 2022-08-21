from logging import config as logging_config

import uvicorn
from database.engine import engine
from fastapi import FastAPI
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from api.routes import api_router
from core.config import get_settings
from core.sentry import init_sentry
from sdk.exceptions.handlers import exception_handlers
from sdk.logging.config import LOGGING
from sdk.logging.helpers import configure_structlog_logger

logging_config.dictConfig(LOGGING)
configure_structlog_logger()


app = FastAPI(
    title=get_settings().PROJECT_NAME,
    exception_handlers=exception_handlers,  # type: ignore
)

app.include_router(api_router)

if get_settings().SENTRY_DSN:
    init_sentry()
    app.add_middleware(SentryAsgiMiddleware)


@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True, access_log=False)
