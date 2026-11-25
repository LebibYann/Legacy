from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "geneweb-backend"

    database_url: str

    backoffice_username: str
    backoffice_password: str

    legacy_dns: str = "legacy-geneweb"
    backoffice_dns: str = "backoffice"
    frontend_dns: str = "frontend"
    new_backoffice_port: int = 5173
    old_backoffice_port: int = 2316
    new_frontend_port: int = 5174
    old_frontend_port: int = 2317
    database_echo: bool = False  # Enable SQL query logging (useful for debugging)
    database_future: bool = True  # Use SQLAlchemy 2.0 style (recommended)

    gwb_path: str | None = "/app/geneweb/distribution/bases"
    gwb2ged_bin: str | None = "/app/geneweb/distribution/gw/gwb2ged"
    ged2gwb_bin: str | None = "/app/geneweb/distribution/gw/ged2gwb"
    gwc_bin: str | None = "/app/geneweb/distribution/gw/gwc"

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="", case_sensitive=False, extra="ignore"
    )


settings = Settings()
