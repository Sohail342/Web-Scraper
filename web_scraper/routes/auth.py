from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from web_scraper.db.database import get_db
from web_scraper.db.schemas import UserCreate, UserLogin, MFAVerify, AccessToken
from web_scraper.services.auth_service import register_user, authenticate_user, verify_otp
from web_scraper.utils.jwt import create_access_token


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await register_user(db, user.username, user.password, user.email)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    
    
@router.post("/login", response_model=AccessToken)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    db_user = await authenticate_user(db, user.username, user.password)
    
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}




@router.post("/verify-otp")
async def verify_otp_route(data: MFAVerify, db: AsyncSession = Depends(get_db)):
    try:
        
        await verify_otp(db, data.username, data.otp_code)
        return {"message": "Successfully verified"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred during OTP verification",
        )


    