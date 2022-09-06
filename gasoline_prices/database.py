import databases
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./db/gasoline.db"

database = databases.Database(DATABASE_URL)
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSess = sessionmaker(bind=engine, class_=AsyncSession, autoflush=False)
Base = declarative_base()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    async with AsyncSess() as session:
        yield session
