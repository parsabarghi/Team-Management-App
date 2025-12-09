from config import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from models.base_class import Base


# pick a URL attribute from settings (handles common names)
_db_url = (
    settings.DATABASE_URL
    # or getattr(settings, "database_url", None)
    # or getattr(settings, "SQLALCHEMY_DATABASE_URL", None)
)

if not _db_url:
    raise RuntimeError("Database URL not found in settings (expected DATABASE_URL or database_url)")

engine = create_async_engine(_db_url, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

async def init_db():
    """create all tables in the database"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()