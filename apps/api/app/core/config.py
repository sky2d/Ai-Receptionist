from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/aireceptionist"
    LLM_PROVIDER: str = "openai"
    LLM_API_KEY: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
