from datetime import datetime, timezone
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


# statement_cache_size=0 is required by asyncpg when running behind a
# transaction pooler (Neon, pgbouncer), which is how this app is deployed.
# It is also an asyncpg-only argument, so passing it to any other driver is a
# TypeError at connect time - hence the guard rather than an unconditional
# connect_args. The Postgres path is unchanged.
_connect_args = (
    {"statement_cache_size": 0} if "asyncpg" in settings.DATABASE_URL else {}
)

engine = create_async_engine(settings.DATABASE_URL, pool_pre_ping=True,
                               connect_args=_connect_args)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
            await db.commit()
        except Exception:
            await db.rollback()
            raise
