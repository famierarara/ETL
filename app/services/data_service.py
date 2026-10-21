from sqlalchemy import text

from app.core.config import settings
from app.db.session import get_oracle_engine, get_redshift_engine


def _rows_to_dicts(result) -> list[dict]:
    """Convert SQLAlchemy result rows into a list of dictionaries."""
    keys = result.keys()
    return [dict(zip(keys, row)) for row in result]


def pull_data() -> dict:
    """Pull data from Oracle and load it into the Redshift staging schema."""
    oracle_engine = get_oracle_engine()
    redshift_engine = get_redshift_engine()

    with oracle_engine.connect() as conn:
        query = f"SELECT * FROM {settings.ORACLE_SOURCE_TABLE}"
        result = conn.execute(text(query))
        rows = _rows_to_dicts(result)

    with redshift_engine.connect() as conn:
        staging_fqn = f'{settings.REDSHIFT_DB}.{settings.STAGING_SCHEMA}.{settings.STAGING_TABLE}'
        conn.execute(text(f"TRUNCATE TABLE {staging_fqn}"))

        if rows:
            columns = list(rows[0].keys())
            col_str = ", ".join(columns)
            placeholders = ", ".join(f":{col}" for col in columns)
            insert_sql = (
                f"INSERT INTO {staging_fqn} ({col_str}) VALUES ({placeholders})"
            )
            conn.execute(text(insert_sql), rows)

        conn.commit()

    return {
        "source": "oracle",
        "destination": "redshift",
        "database": settings.REDSHIFT_DB,
        "schema": settings.STAGING_SCHEMA,
        "table": settings.STAGING_TABLE,
        "records_loaded": len(rows),
    }


def transform_data() -> dict:
    """Read raw data from staging and write transformed data into the spedia schema."""
    redshift_engine = get_redshift_engine()

    with redshift_engine.connect() as conn:
        staging_fqn = f'{settings.REDSHIFT_DB}.{settings.STAGING_SCHEMA}.{settings.STAGING_TABLE}'
        result = conn.execute(text(f"SELECT * FROM {staging_fqn}"))
        rows = _rows_to_dicts(result)

    transformed_rows = [
        {
            "record_id": row.get("id"),
            "doubled_value": (row.get("value", 0) or 0) * 2,
        }
        for row in rows
    ]

    with redshift_engine.connect() as conn:
        spedia_fqn = f'{settings.REDSHIFT_DB}.{settings.SPEDIA_SCHEMA}.{settings.SPEDIA_TABLE}'
        conn.execute(text(f"TRUNCATE TABLE {spedia_fqn}"))

        if transformed_rows:
            columns = list(transformed_rows[0].keys())
            col_str = ", ".join(columns)
            placeholders = ", ".join(f":{col}" for col in columns)
            insert_sql = (
                f"INSERT INTO {spedia_fqn} ({col_str}) VALUES ({placeholders})"
            )
            conn.execute(text(insert_sql), transformed_rows)

        conn.commit()

    total = sum(row.get("value", 0) or 0 for row in rows)
    count = len(rows)

    return {
        "source": "redshift",
        "database": settings.REDSHIFT_DB,
        "schema": settings.SPEDIA_SCHEMA,
        "table": settings.SPEDIA_TABLE,
        "records_loaded": count,
        "summary": {
            "count": count,
            "total": total,
            "average": total / count if count else 0,
        },
    }
