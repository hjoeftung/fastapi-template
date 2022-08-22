from fastapi import HTTPException
from starlette import status
from starlette.responses import JSONResponse, PlainTextResponse

from crud.healthchecks import HealthChecksCRUD
from sdk.logging.logged_router import LoggingAPIRouter

router = LoggingAPIRouter()


@router.get("/ping/", response_class=PlainTextResponse)
def check_if_alive():
    """Endpoint to check if service responds"""

    return "OK"


@router.get("/db/")
async def check_database() -> JSONResponse:
    """Endpoint to check DB connection"""

    result = await HealthChecksCRUD.check_database()
    if result:
        return JSONResponse({"status": "OK"})
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Database not responding",
    )


@router.get("/sentry_debug/")
def sentry_debug():
    """Simplest check to ensure errors are sent to Sentry"""

    raise Exception
