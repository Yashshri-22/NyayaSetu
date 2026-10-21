from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.0-flash"
    jwt_secret: str = "development-only-change-me"
    database_url: str = "sqlite:///./nyayasetu.db"
    chroma_persist_dir: str = "./chroma_data"
    upload_dir: str = "./uploads"
    max_upload_mb: int = 20
    frontend_origin: str = "http://localhost:5173"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
settings = Settings()
