from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGODB_URL: str = "mongodb://localhost:27017/coupon_db"
    # Add other settings as needed

    class Config:
        extra = "ignore"
        env_file = ".env"

settings = Settings()
