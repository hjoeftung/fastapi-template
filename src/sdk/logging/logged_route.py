import time
import typing as tp
import uuid

import structlog
from fastapi.routing import APIRoute
from starlette.requests import Request
from starlette.responses import Response

from sdk.logging import helpers as logging_helpers
from sdk.logging import request_logger


class LoggedRoute(APIRoute):
    @staticmethod
    async def _get_request_payload(request: Request) -> dict | None:
        """Get application/json payload from request"""

        if "application/json" in request.headers.get("content-type", ""):
            return await request.json() or None

        return None

    async def _log_request(self, request: Request) -> None:
        """Log request"""

        ip = request.client.host if request.client else None
        method = request.method
        path = request.url.path
        request_id = logging_helpers.get_request_header(request, "x-request-id") or str(
            uuid.uuid4()
        )
        url = str(request.url)
        user_agent = logging_helpers.get_request_header(request, "user-agent")
        request_payload = await self._get_request_payload(request)

        structlog.contextvars.bind_contextvars(
            ip=ip,
            method=method,
            path=path,
            url=url,
            request_id=request_id,
            request_payload=request_payload,
        )
        request_logger.info(
            "request_started",
            user_agent=user_agent,
        )

        request.request_id = request_id  # type: ignore

    @staticmethod
    def _log_response(response: Response, request_start_time: float):
        """Log response"""

        status_code = response.status_code
        response_time = time.monotonic() - request_start_time
        request_logger.info(
            "request_finished",
            code=status_code,
            response_time=response_time,
        )

    def get_route_handler(self) -> tp.Callable:
        original_route_handler = super().get_route_handler()

        async def log_handler(request: Request) -> Response:
            """Log request and response"""

            structlog.contextvars.clear_contextvars()
            request_start_time = time.monotonic()
            await self._log_request(request)

            response: Response = await original_route_handler(request)

            self._log_response(response, request_start_time=request_start_time)

            return response

        return log_handler
