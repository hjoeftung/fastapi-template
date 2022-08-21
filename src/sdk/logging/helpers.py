import uuid
from typing import Any

import structlog
from starlette.requests import Request

from sdk.logging import exception_logger


def configure_structlog_logger() -> None:
    if structlog.is_configured():
        return

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.filter_by_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_request_header(request: Request, header_key: str) -> Any:
    if hasattr(request, "headers"):
        return request.headers.get(header_key)

    return None


def log_exception(error_type: str, request: Request, exception: Exception) -> None:
    structlog.contextvars.clear_contextvars()

    ip = request.client.host if request.client else None
    method = request.method
    path = request.url.path
    request_id = get_request_header(request, "x-request-id") or str(uuid.uuid4())
    url = str(request.url)
    user_agent = get_request_header(request, "user-agent")

    structlog.contextvars.bind_contextvars(
        ip=ip,
        method=method,
        path=path,
        url=url,
        request_id=request_id,
        exc_info=exception,
    )

    exception_logger.error(
        error_type,
        user_agent=user_agent,
    )
