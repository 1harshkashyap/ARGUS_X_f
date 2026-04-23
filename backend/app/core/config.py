from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # Environment
    ENV: str = Field(default="development")

    # Supabase
    SUPABASE_URL: str = Field(...)
    SUPABASE_SERVICE_KEY: str = Field(...)
    SUPABASE_ANON_KEY: str = Field(...)

    # Redis
    REDIS_URL: Optional[str] = Field(default=None)

    # LLM
    LLM_PROVIDER: str = Field(...)
    LLM_API_KEY: str = Field(...)

    # Hugging Face
    HF_MODEL_REPO: Optional[str] = Field(default=None)
    HF_TOKEN: Optional[str] = Field(default=None)

    # ML Thresholds
    ML_CLASSIFIER_THRESHOLD: float = Field(default=0.87)
    ML_SEMANTIC_THRESHOLD: float = Field(default=0.75)

    # Frontend
    FRONTEND_URL: str = Field(...)

    @property
    def is_production(self) -> bool:
        return self.ENV == "production"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings: Settings = get_settings()
