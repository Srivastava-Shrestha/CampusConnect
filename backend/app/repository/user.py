from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User, UserRole, Student, CampusAdmin
from sqlalchemy import select, exists

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def is_email_exist(self, email: str) -> bool:
        result = await self.db.execute(select(exists().where(User.email==email)))
        return result.scalar()
    
    async def create_user(self, full_name: str, hashed_password: str, email: str, role: UserRole, college_id: int | None) -> User:
        new_user = User(
            email=email, 
            full_name=full_name, 
            hashed_password=hashed_password, 
            role=role, 
            college_id=college_id
        )
        self.db.add(new_user)
        await self.db.flush()
        return new_user
    
    async def create_student(self, user_id: int) -> Student:
        new_student = Student(user_id = user_id)
        self.db.add(new_student)
        return new_student
    
    async def create_campus_admin(self, user_id: int) -> CampusAdmin:
        new_campus_admin = CampusAdmin(user_id = user_id)
        self.db.add(new_campus_admin)
        return new_campus_admin


