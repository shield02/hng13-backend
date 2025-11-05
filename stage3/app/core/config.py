from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Eco-Mind"
    app_env: str = "development"
    redis_url: str = "redis://redis:6379/0"
    nominatim_api: str = "https://nominatim.openstreetmap.org"
    overpass_api: str = "https://overpass-api.de/api/interpreter"
    earth911_api_key: str | None = None
    telex_webhook_url: str = "http://localhost:8000/webhook"

    chat_ttl_seconds: int = 3600

    class Config:
        env_file = ".env"

settings = Settings()
