from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from web_scraper.db.database import get_db
from web_scraper.db.schemas import UserCreate, UserLogin, MFAVerify, AccessToken, UpdateUser
from web_scraper.services.auth_service import register_user, authenticate_user, verify_otp, update_user
from web_scraper.utils.jwt import create_access_token, get_current_user, create_refresh_token
from web_scraper.db.models import User


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await register_user(db, user.username, user.password, user.email)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    
    
@router.post("/login", response_model=AccessToken)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    
    db_user = await authenticate_user(db, user.username_or_email, user.password)
    
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    # Create Access Token
    access_token = create_access_token({"sub": user.username_or_email})
    
    # Create Refresh Token
    refresh_token = create_refresh_token({"sub": user.username_or_email})
    
    from icecream import ic
    ic(access_token)
    ic(refresh_token)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }




@router.post("/verify-otp")
async def verify(data: MFAVerify, db: AsyncSession = Depends(get_db)):
    try:
        
        await verify_otp(db, data.username_or_email, data.otp_code)
        return {"message": "Successfully verified"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during OTP verification",
        )
        
        
@router.put("/update")
async def update(data: UpdateUser, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    
    try:
        await update_user(db, current_user.username, data.email)
        return {"message": "Confirmation email sent"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during update",
        )


