from pydantic import BaseSettings


class Settings(BaseSettings):
    # Load these from .env
    OPENAI_API_KEY: str
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "flood_ai"
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: int = 5432

    class Config:
        env_file = ".env"


settings = Settings()
