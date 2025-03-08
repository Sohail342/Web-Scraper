from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import urlparse
from web_scraper.config import Config
from sqlmodel import SQLModel

# Parse the database URL
tmpPostgres = urlparse(Config.DATABASE_URL)

# Create the async engine
engine = create_async_engine(
    f"postgresql+asyncpg://{tmpPostgres.username}:{tmpPostgres.password}@{tmpPostgres.hostname}{tmpPostgres.path}",
    echo=True
)

# Create a session factory
SessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

# Dependency to get a database session
async def get_db():
    async with SessionLocal() as session:
        yield session
        
# Function to create tables
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)