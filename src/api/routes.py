from api.v1 import healthchecks
from sdk.logging.logged_router import LoggingAPIRouter

api_router = LoggingAPIRouter()

api_router.include_router(healthchecks.router, prefix="/healthchecks", tags=["healthchecks"])
