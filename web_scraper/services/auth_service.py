import bcrypt
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from web_scraper.db.models import User
from web_scraper.utils.email_otp import generate_otp, send_email_otp
from fastapi import HTTPException, status
from sqlalchemy import select, or_



async def register_user(db: AsyncSession, username: str, password: str, email: str):
    # Check if the user already exists (username or email)
    result = await db.execute(select(User).filter(or_(User.username == username, User.email == email)))
    existing_user = result.scalars().first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists",
        )
    
    # Hash the password and decode it to a string
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode('utf-8')
    
    otp_code = generate_otp()
    
    # Create a new user with the decoded hashed password
    new_user = User(username=username, hashed_password=hashed_password, email=email, otp_code=otp_code)
    
    db.add(new_user)
    await db.commit()
    
    await send_email_otp(new_user.email, otp_code)
    return {"message": "Confirmation email sent"}


async def authenticate_user(db: AsyncSession, username: str, password: str):
    result = await db.execute(select(User).filter(User.username == username))
    user = result.scalars().first()

    if not user or not bcrypt.checkpw(password.encode(), user.hashed_password.encode("utf-8")):
        return None
    
    if not user.verified:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not verified")
    return user



async def verify_otp(db: AsyncSession, username: str, otp_code: str):
    # Fetch the user from the database
    result = await db.execute(select(User).filter(User.username == username))
    user = result.scalars().first()

    # Check if the user exists and the OTP code matches
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    if user.otp_code != otp_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP code",
        )

    # Check if the user is already verified
    if user.verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already verified",
        )

    # Mark the user as verified and clear the OTP code
    user.verified = True
    user.otp_code = None
    await db.commit()

    return {"message": "User verified successfully"}
