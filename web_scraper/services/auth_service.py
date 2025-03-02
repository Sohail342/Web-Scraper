import bcrypt
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from web_scraper.db.models import User
from web_scraper.utils.email_otp import generate_otp, send_email_otp
from web_scraper.utils.jwt import create_access_token



async def register_user(db: AsyncSession, username: str, password: str, email: str):
    # Check if the user already exists
    result = await db.execute(select(User).filter(User.username == username))
    existing_user = result.scalars().first()
    
    if existing_user:
        raise Exception("User already exists")
    
    # Hash the password and decode it to a string
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode('utf-8')
    
    
    # Create a new user with the decoded hashed password
    new_user = User(username=username, hashed_password=hashed_password, email=email)
    db.add(new_user)
    await db.commit()
    
    return {"message": "User registered successfully"}


async def authenticate_user(db: AsyncSession, username: str):
    result = await db.execute(select(User).filter(User.username == username))
    user = result.scalars().first()

    if not user:
        return None

    otp_code = generate_otp()
    send_email_otp(user.email, otp_code)

    # Store OTP in database
    user.otp_code = otp_code
    await db.commit()
    return {"message": "OTP sent to registered email"}


async def verify_otp(db: AsyncSession, username: str, otp_code: str):
    result = await db.execute(select(User).filter(User.username == username))
    user = result.scalars().first()

    if not user or user.otp_code != otp_code:
        return None

    token = create_access_token({"sub": username})
    return token
