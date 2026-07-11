from sqlalchemy.ext.asyncio import AsyncSession
from app.models import College
from sqlalchemy import select, literal

class CollegeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def email_to_college(self, email: str) -> College | None:
        domain = email.split("@")[-1]
        result = await self.db.execute(
            select(College).where(
                (College.email_suffix == domain)| literal(domain).like("%." + College.email_suffix)
            )
        )
        return result.scalar_one_or_none()