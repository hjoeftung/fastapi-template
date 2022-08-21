from pydantic import BaseModel


class FieldErrorModel(BaseModel):
    field: str
    message: str


class ExceptionModel(BaseModel):
    code: int = 400
    message: str
    field_errors: list[FieldErrorModel] | None = None
