from contextlib import asynccontextmanager
from fastapi import FastAPI
from web_scraper.routes import auth
from web_scraper.db.database import create_tables

# Lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run on startup
    await create_tables()
    yield
    # Code to run on shutdown 
    
    
app = FastAPI(lifespan=lifespan, title="Web Scraper API", version="0.1", description="API for web scraping")

# Include the auth router
app.include_router(auth.router)