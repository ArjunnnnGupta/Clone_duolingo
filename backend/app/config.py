from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite:///data/app.db"
    # Comma-separated in the environment, e.g. "https://app.vercel.app,http://localhost:3000".
    cors_origins: str = "http://localhost:3000"
    enable_dev_tools: bool = True
    heart_regen_minutes: int = 30
    max_hearts: int = 5
    default_user_id: int = 1
    seed_on_startup: bool = True

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
