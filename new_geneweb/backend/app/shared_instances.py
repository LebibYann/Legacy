from functools import lru_cache

from app.persistence.DBConnector import DBConnector


@lru_cache
def get_db_connector() -> DBConnector:
    return DBConnector()
