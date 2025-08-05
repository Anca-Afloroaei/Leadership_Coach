from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    SUPABASE_PASSWORD: str
    DATABASE_URL: str
    SUPABASE_URL: str
    OPENAI_API_KEY: str
    
    

settings = Settings()
