from __future__ import annotations

from pydantic import field_validator, ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict
import warnings

class Settings(BaseSettings):
    app_env: str
    app_name: str
    app_host: str
    app_port: int

    database_url: str
    allowed_ips: str | list[str] = "127.0.0.1,::1"

    legacy_dns: str = "legacy-geneweb"
    backoffice_dns: str = "backoffice"
    frontend_dns: str = "frontend"
    new_backoffice_port: int = 5173
    old_backoffice_port: int = 2316
    new_frontend_port: int = 5174
    old_frontend_port: int = 2317



    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="",
        case_sensitive=False,
        extra='ignore'
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
