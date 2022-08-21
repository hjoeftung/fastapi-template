import pydantic


class IntegerID(pydantic.BaseModel):
    id: int
