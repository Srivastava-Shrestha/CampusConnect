from app.core.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.repository import UserRepository, CollegeRepository
from app.services import UserService

def get_user_service(db: AsyncSession = Depends(get_db)):
    user_repo = UserRepository(db)
    college_repo = CollegeRepository(db)
    return UserService(user_repo, college_repo)