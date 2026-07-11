from fastapi import APIRouter, Depends
from app.schemas import SignupResponse, SignupRequest, LoginResponse, LoginRequest
from app.services import UserService
from app.core.di import get_user_service

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@auth_router.post("/signup", response_model=SignupResponse)
async def signup(data: SignupRequest, service: UserService = Depends(get_user_service)):
    return await service.signup(data)

@auth_router.post("/login", response_model=LoginResponse)
async def login(data:LoginRequest, service: UserService = Depends(get_user_service)):
    return await service.login(data)

