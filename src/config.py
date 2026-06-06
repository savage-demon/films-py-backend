from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_TITLE: str = "Films API"
    APP_VERSION: str = "0.0.1"
    DEBUG: bool = False
    ENV: str = "prod" # prod, dev

    DB_URL: str = ""
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8",
        extra = "ignore"
    )


# Синглтон настроек
settings = Settings()
