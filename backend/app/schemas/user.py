from pydantic import BaseModel, EmailStr, Field, model_validator
from app.models import UserRole

class SignupRequest(BaseModel):
    email: EmailStr = Field(..., max_length=255)
    full_name: str = Field(..., min_length=5, max_length=100)
    password: str = Field(..., min_length=8, max_length=255)
    confirm_password: str = Field(..., min_length=8, max_length=255)
    role: UserRole
    
    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("password and confirm password do not match")
        return self

class SignupResponse(BaseModel):
    access_token: str
    refresh_token: str
    
class LoginRequest(BaseModel):
    email: EmailStr = Field(..., max_length=255)
    password: str = Field(..., min_length=8, max_length=255)
    
class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str