from sqlalchemy.ext.asyncio import AsyncSession
import httpx
from fastapi import HTTPException, status
from datetime import datetime, timezone
from sqlalchemy import select, or_
from web_scraper.db.models import User, ScraperJobs
from bs4 import BeautifulSoup




async def scrap_tags(
        target_url: str, 
        target_tag: str, 
        target_attribute: str, 
        user: str,
        db: AsyncSession, 
    ):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(target_url)
            response.raise_for_status()
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    
    attributes = []
    for tag in soup.find_all(target_tag): 
        attr_value = tag.get(target_attribute, "Attribute not found")
        attributes.append(attr_value)
        
    # Store in db with requested user
    result = await db.execute(select(User).filter(or_(User.username == user, User.email == user)))
    user_instance = result.scalars().first()
    
   
    # Create Job
    new_job = ScraperJobs(
        url=target_url,
        status="Completed",
        user=user_instance,
        completed_at=datetime.now(timezone.utc).isoformat(), 
        
        # Convert Nested list to string
        results = ", ".join(
            item if isinstance(item, str) else " ".join(item)
            for item in attributes
        )
    )
    
    db.add(new_job)
    await db.commit()
    await db.refresh(new_job)
    
    return attributes


async def scraped_data(user: str, db: AsyncSession):
    
    try:
        result = await db.execute(select(ScraperJobs).filter(ScraperJobs.user_id == user))
        scraped_data =  result.scalars().all()
        
    except Exception as e:
        raise e
    return scraped_data


async def scraped_single_data(job_id: int, user: str, db: AsyncSession):
    
    try:
        result = await db.execute(select(ScraperJobs).filter(ScraperJobs.job_id == job_id, ScraperJobs.user_id == user))
        scraped_data =  result.scalars().first()
        
        if not scraped_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
        
    except Exception as e:
        raise e
    return scraped_data
    