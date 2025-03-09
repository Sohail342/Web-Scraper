from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import urlparse
from web_scraper.config import Config

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