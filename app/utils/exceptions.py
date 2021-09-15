from fastapi import status
from pydantic.main import BaseModel


class BadRequestError(Exception):
    """Custom exception for 400 Bad Request error."""

    def __init__(self, message: str):
        self.code = status.HTTP_400_BAD_REQUEST
        self.message = message


class ExceptionModel(BaseModel):
    """Model for the exception with custom message."""

    error: str
