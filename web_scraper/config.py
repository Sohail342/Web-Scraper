from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    
    # Database settings
    DATABASE_URL: str
    SECRET_KEY: str 
    
    # JWT settings
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Email settings
    EMAIL_HOST: str 
    EMAIL_USERNAME: str
    EMAIL_PASSWORD: str
    EMAIL_PORT: int = 587       
    
    model_config = SettingsConfigDict(
        env_file="web_scraper/.env",
        extra="ignore",
    )        
    

Config = Settings()           