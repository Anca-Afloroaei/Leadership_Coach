from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SUPABASE_PASSWORD: str
    DATABASE_URL: str
    SUPABASE_URL: str


settings = Settings()
