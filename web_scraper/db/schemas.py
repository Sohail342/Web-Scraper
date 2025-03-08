from pydantic import BaseModel, EmailStr, Field
from typing import Annotated


class UserCreate(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=20, example="username32", pattern="^[a-zA-Z0-9_]+$")]
    password: Annotated[str, Field(min_length=8, max_length=20, example="password123")]
    email: Annotated[EmailStr, Field(example="user@example.com")]
    
class UserLogin(BaseModel):
    username_or_email: Annotated[str, Field(example="Username or email")] 
    password: Annotated[str, Field(example="Password")]
    
    @classmethod
    def validate_one(cls, values):
        if not any([values.get("username"), values.get("email")]):
            raise ValueError("Either username or email must be provided")
        return values
        
        
    
class UpdateUser(BaseModel):
    email: Annotated[EmailStr, Field(example="user@example.com")]

class MFAVerify(BaseModel):
    username_or_email: Annotated[str, Field(example="Username or email")]
    otp_code: str
    
class AccessToken(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    