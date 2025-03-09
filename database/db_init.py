from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
import os
from sqlalchemy.orm import sessionmaker

DB_USER = os.getenv("DB_USER") or "postgres"
DB_PASSWORD = os.getenv("DB_PASSWORD") or "postgres"
DB_HOST = os.getenv("DB_HOST") or "localhost"
DB_PORT = os.getenv("DB_PORT") or "5432"
DB_NAME = os.getenv("DB_NAME") or 'beregDB'

# Создаем асинхронный движок SQLAlchemy
engine = create_async_engine(f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Создаем асинхронную сессию
async_session = sessionmaker(engine, class_=AsyncSession)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
        await session.commit()
