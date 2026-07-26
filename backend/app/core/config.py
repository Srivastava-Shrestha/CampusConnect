from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    TEST_DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    FRONTEND_URL: str

    class Config:
        env_file = ".env"

settings = Settings()