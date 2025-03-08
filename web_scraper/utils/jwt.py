from jose import jwt
from datetime import datetime, timedelta, timezone
from web_scraper.config import Config
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from web_scraper.db.database import get_db
from web_scraper.db.models import User
from sqlalchemy import select
from jose import JWTError, jwt
from web_scraper.config import Config
from sqlalchemy.ext.asyncio import AsyncSession


oauth2_scheme  = OAuth2PasswordBearer(tokenUrl="login")



def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)

def create_access_token(data: dict):
    return create_token(data, timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES))

def create_refresh_token(data: dict):
    return create_token(data, timedelta(days=Config.REFRESH_TOKEN_EXPIRE_DAYS))



# Function to verify JWT and extract user
async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception  = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Fetch user from database
    result = await db.execute(select(User).filter(User.username == username))
    user = result.scalars().first()
    if user is None:
        raise credentials_exception 
    
    return user