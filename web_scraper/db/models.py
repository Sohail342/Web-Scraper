from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    username: str = Field(primary_key=True, index=True)
    hashed_password: str
    email: str | None = Field(default=None, unique=True)
    otp_code: str | None = None
    verified: bool = Field(default=False)
    
    class Config:
        from_attributes = True
