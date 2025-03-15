from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime


class User(SQLModel, table=True):
    username: str = Field(primary_key=True, index=True)
    hashed_password: str
    email: Optional[str] = Field(default=None, unique=True)
    otp_code: Optional[str] = None
    verified: bool = Field(default=False)

    # Relationship: One user has many scraper jobs
    scraper_jobs: List["ScraperJobs"] = Relationship(back_populates="user")
    
    class Config:
        from_attributes = True


class ScraperJobs(SQLModel, table=True):
    job_id: int = Field(default=None, primary_key=True, index=True)
    url: str
    status: str = Field(default="pending")
    completed_at: Optional[str] = None
    results: Optional[str] = None

    user_id: str = Field(foreign_key="user.username")

    # Relationship: Many scraper jobs belong to one user
    user: Optional[User] = Relationship(back_populates="scraper_jobs")

    class Config:
        from_attributes = True
    
