from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str
    app_name: str
    app_host: str
    app_port: int

    database_url: str
    allowed_ips: list[str] = ["127.0.0.1", "::1"]

    model_config = SettingsConfigDict(
        env_file=".env",  # read a .env file at the root of the project
        env_prefix="",  # no prefix required
        case_sensitive=False,
    )


settings = Settings()
