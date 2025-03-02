from jose import jwt
from datetime import datetime, timedelta, timezone
from web_scraper.config import ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)