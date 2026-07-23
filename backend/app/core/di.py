from app.core.database import get_db
from fastapi import Depends, Security
from sqlalchemy.ext.asyncio import AsyncSession
from app.repository import UserRepository, CollegeRepository
from app.services import UserService, CollegeService
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, SecurityScopes
from app.core.token import decode_token
from app.exceptions import AuthorizationError

def get_user_service(db: AsyncSession = Depends(get_db)):
    user_repo = UserRepository(db)
    college_repo = CollegeRepository(db)
    return UserService(user_repo, college_repo)

security = HTTPBearer()
def get_user_info(scopes: SecurityScopes, credentials: HTTPAuthorizationCredentials = Depends(security)):
    payload = decode_token(credentials.credentials)
    if payload.get("role") not in scopes.scopes:
        raise AuthorizationError()
    return payload
            
def get_college_service(db: AsyncSession = Depends(get_db)):
    college_repo = CollegeRepository(db)
    user_repo = UserRepository(db)
    return CollegeService(college_repo, user_repo)


    
# token -> decode -> authorization karenge -> role match -> user data return (token vala vhi jo diye the)

# onboardinig