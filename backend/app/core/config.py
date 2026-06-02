from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # =========================
    # DATABASE
    # =========================

    DATABASE_URL: str
    DIRECT_URL: str

    # =========================
    # AUTH
    # =========================

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # =========================
    # OPENAI
    # =========================

    OPENAI_API_KEY: str | None = None

    # =========================
    # SETTINGS
    # =========================

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()