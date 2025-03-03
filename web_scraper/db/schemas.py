from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    email: str
    
    
class UserLogin(BaseModel):
    username: str
    password: str
    
    
class MFAVerify(BaseModel):
    username: str
    otp_code: str
    
class AccessToken(BaseModel):
    access_token: str
    token_type: str
    