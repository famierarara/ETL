import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application configuration loaded from environment variables."""

    ORACLE_CONNECTION_STRING: str = os.getenv("ORACLE_CONNECTION_STRING", "")
    REDSHIFT_CONNECTION_STRING: str = os.getenv("REDSHIFT_CONNECTION_STRING", "")

    REDSHIFT_DB: str = os.getenv("REDSHIFT_DB", "scoaa")
    STAGING_SCHEMA: str = os.getenv("STAGING_SCHEMA", "staging")
    SPEDIA_SCHEMA: str = os.getenv("SPEDIA_SCHEMA", "spedia")

    ORACLE_SOURCE_TABLE: str = os.getenv("ORACLE_SOURCE_TABLE", "source_data")
    STAGING_TABLE: str = os.getenv("STAGING_TABLE", "raw_data")
    SPEDIA_TABLE: str = os.getenv("SPEDIA_TABLE", "transformed_data")


settings = Settings()
