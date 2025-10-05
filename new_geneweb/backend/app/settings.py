from __future__ import annotations
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    app_env: str
    app_name: str
    app_host: str
    app_port: int

    database_url: str
    allowed_ips: str | list[str] = "127.0.0.1,::1"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="",
        case_sensitive=False,
    )

    @field_validator("allowed_ips", mode="before")
    @classmethod
    def parse_ips(cls, v: str | list[str]) -> list[str]:
        # Already a list (JSON)
        if isinstance(v, list):
            return v
        # CSV
        return [ip.strip() for ip in v.split(",")]


settings = Settings()
