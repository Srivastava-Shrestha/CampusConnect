from app.exceptions.base import AppException
from app.exceptions.user import (
    UserAlreadyExistError, CollegeNotFoundError, AuthenticationError,
    CollegeAlreadyExistError, IncorrectCredentialError
)