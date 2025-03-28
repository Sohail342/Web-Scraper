from fastapi import FastAPI
from web_scraper.routes import auth, scraper

    
app = FastAPI(title="Web Scraper API", version="0.1", description="API for web scraping")

# Include the auth router
app.include_router(auth.router)
app.include_router(scraper.router)