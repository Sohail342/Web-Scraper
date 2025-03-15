from fastapi import APIRouter, Depends, HTTPException, status
from web_scraper.db.database import get_db
from web_scraper.db.schemas import ScrapTags, ScrapedData
from sqlalchemy.ext.asyncio import AsyncSession
from web_scraper.db.models import User
from web_scraper.utils.jwt import get_current_user
from web_scraper.services.scraper_service import scrap_tags, scraped_data, scraped_single_data


router = APIRouter(prefix="/api", tags=["Scraper"])


@router.post("/scraper")
async def scraper_job(
        data: ScrapTags, 
        current_user: User = Depends(get_current_user), 
        db: AsyncSession = Depends(get_db),
    ):
    
    try:
        html_content = await scrap_tags(data.url, data.target_tag, data.target_attribute, current_user.username, db)
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during update",
        )
    return html_content


@router.get("/scrapered/data", response_model=list[ScrapedData])
async def get_all_jobs(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    
    try:
        result = await scraped_data(current_user.username, db)
        
        # Convert result (list of ScraperJobs instances) into list of dictionaries
        response_data = [ScrapedData(**job.model_dump()) for job in result]
        
    except HTTPException as e:
        raise e
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during update. {e}",
        )
    return response_data



@router.get("/scrapered/data/{job_id}", response_model=ScrapedData)
async def get_job(job_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    
    try:
        result = await scraped_single_data(job_id, current_user.username, db)

    except HTTPException as e:
        raise e
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during update. {e}",
        )
    return result