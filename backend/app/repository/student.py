from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Student
from sqlalchemy import select


class StudentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_student_by_user_id(self, user_id: int) -> Student | None:
        result = await self.db.execute(select(Student).where(Student.user_id == user_id))
        return result.scalar_one_or_none()
