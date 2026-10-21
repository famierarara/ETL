from sqlalchemy import create_engine

from app.core.config import settings

_oracle_engine = None
_redshift_engine = None


def get_oracle_engine():
    """Return a lazy-created SQLAlchemy engine for the Oracle source."""
    global _oracle_engine
    if _oracle_engine is None:
        if not settings.ORACLE_CONNECTION_STRING:
            raise ValueError("ORACLE_CONNECTION_STRING is not configured")
        _oracle_engine = create_engine(settings.ORACLE_CONNECTION_STRING)
    return _oracle_engine


def get_redshift_engine():
    """Return a lazy-created SQLAlchemy engine for the Redshift destination."""
    global _redshift_engine
    if _redshift_engine is None:
        if not settings.REDSHIFT_CONNECTION_STRING:
            raise ValueError("REDSHIFT_CONNECTION_STRING is not configured")
        _redshift_engine = create_engine(settings.REDSHIFT_CONNECTION_STRING)
    return _redshift_engine
