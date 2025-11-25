from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Document Processing Service"

    # Database
    DATABASE_URL: PostgresDsn

    # RabbitMQ
    RABBITMQ_URL: str

    # MinIO/S3
    MINIO_ENDPOINT: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_BUCKET: str = "files"

    # Security
    MAX_BCRYPT_BYTES: int = 72
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    model_config = SettingsConfigDict(extra="ignore")
    # class Config:
    #     env_file = "/app/config/dev.env"


settings = Settings()
