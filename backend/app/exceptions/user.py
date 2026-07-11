from app.exceptions import AppException

class UserAlreadyExistError(AppException):
    status_code = 409
    message = "Email already registered"
    
class CollegeNotFoundError(AppException):
    status_code = 404
    message = "College not registered"
    
class AuthenticationError(AppException):
    status_code = 401
    message = "Invalid token"
    
class CollegeAlreadyExistError(AppException):
    status_code = 409
    message = "College already registered"