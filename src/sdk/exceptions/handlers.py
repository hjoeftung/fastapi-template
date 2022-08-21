import sentry_sdk
from asyncpg.exceptions import ForeignKeyViolationError
from fastapi.exceptions import HTTPException, RequestValidationError
from sentry_sdk import capture_exception
from sqlalchemy.exc import IntegrityError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from sdk.exceptions.exceptions import LogicValidationError
from sdk.exceptions.schemas import ExceptionModel, FieldErrorModel
from sdk.logging.helpers import log_exception


def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Request validation errors from Pydantic"""

    log_exception(error_type="request_validation_error", request=request, exception=exc)
    field_errors: list[FieldErrorModel] = []
    for error in exc.errors():
        field = [str(loc) for loc in error.get("loc", "")]

        joined_field = ", ".join(field)
        message = error.get("msg", "")
        field_errors.append(FieldErrorModel(field=joined_field, message=message))

    content = ExceptionModel(
        code=status.HTTP_400_BAD_REQUEST,
        message="Validation Failed",
        field_errors=field_errors,
    )

    return JSONResponse(content.dict(), status_code=status.HTTP_400_BAD_REQUEST)


def logic_validation_exception_handler(request: Request, exc: LogicValidationError) -> JSONResponse:
    """Business logic validation errors"""

    log_exception(error_type="logic_validation_error", request=request, exception=exc)
    if exc.field_errors:
        field_errors = [
            FieldErrorModel(field=fe.field, message=fe.message) for fe in exc.field_errors
        ]

    else:
        field_errors = []

    content = ExceptionModel(
        code=exc.code,
        message=exc.message,
        field_errors=field_errors,
    )

    return JSONResponse(content.dict(), status_code=exc.code)


def not_found_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """404 exception handler"""

    log_exception(error_type="not_found_error", request=request, exception=exc)

    error_message = "Item not found"
    if hasattr(exc, "detail") and exc.detail:
        error_message = exc.detail

    content = ExceptionModel(
        code=404,
        message=error_message,
        field_errors=[],
    )

    return JSONResponse(content.dict(), status_code=404)


def foreign_key_error_handler(request: Request, exc: ForeignKeyViolationError) -> JSONResponse:
    """Handler for foreign key errors"""

    log_exception(
        error_type="foreign_key_violation_error",
        request=request,
        exception=exc,
    )

    content = ExceptionModel(error_message=exc.detail)
    return JSONResponse(content.dict(), status_code=status.HTTP_400_BAD_REQUEST)


def unexpected_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Fallback handler for any unexpected errors"""

    sentry_sdk.capture_exception(exc)
    log_exception(error_type="unexpected_error", request=request, exception=exc)
    error_message = "Oops! Unexpected error occurred"
    content = ExceptionModel(code=status.HTTP_400_BAD_REQUEST, message=error_message)
    capture_exception(exc)
    return JSONResponse(content.dict(), status_code=400)


exception_handlers = {
    Exception: unexpected_exception_handler,
    404: not_found_exception_handler,
    LogicValidationError: logic_validation_exception_handler,
    RequestValidationError: request_validation_exception_handler,
    IntegrityError: foreign_key_error_handler,
}
