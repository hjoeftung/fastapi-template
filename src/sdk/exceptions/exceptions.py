from starlette import status

__all__ = ["BaseHTTPException", "LogicValidationError"]

from sdk.exceptions.schemas import FieldErrorModel


class BaseHTTPException(Exception):
    """Base exception class"""

    message: str | None
    code: int = status.HTTP_400_BAD_REQUEST
    field_errors: list[FieldErrorModel] | None = None

    def __init__(
        self,
        message: str | None = None,
        code: int = 400,
        field_errors: list[FieldErrorModel] | None = None,
    ) -> None:
        self.message = message or self.message
        self.code = code or self.code
        self.field_errors = field_errors or self.field_errors


class LogicValidationError(BaseHTTPException):
    """Business logic validation error"""

    message: str | None = "Logic Validation Failed"
