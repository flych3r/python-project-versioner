from fastapi import status
from pydantic.main import BaseModel


class BadRequestException(Exception):
    def __init__(self, message: str):
        self.code = status.HTTP_400_BAD_REQUEST
        self.message = message


class ExceptionModel(BaseModel):
    error: str
