from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    TEST_DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    FRONTEND_URL: str

    AWS_REGION: str
    S3_BUCKET_NAME: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str
    MAIL_FROM: str

    GOOGLE_CLIENT_ID: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
