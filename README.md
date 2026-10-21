# etl_spend

A FastAPI-based ETL pipeline for CMAT spend data.

This service extracts data from an Oracle source, loads it into an Amazon Redshift staging schema, applies lightweight transformations, and writes the results into a Redshift `spedia` schema. Each ETL step can be triggered through HTTP endpoints, either individually or as a single orchestrated run.

## Data flow

1. **Extract** (`POST /data_pull`)  
   Query all rows from the configured Oracle source table and load them into the Redshift staging table after truncating it.

2. **Transform** (`POST /data_transformation`)  
   Read the raw staging data, apply business transformations, and write the output into the Redshift `spedia` table after truncating it.

3. **Orchestrate** (`POST /orchestrator`)  
   Run the `data_pull` step followed by the `data_transformation` step in sequence.

## API endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST | `/data_pull` | Pull data from Oracle into Redshift staging |
| POST | `/data_transformation` | Transform staging data and load into `spedia` |
| POST | `/orchestrator` | Run pull and transform end-to-end |

## Configuration

Set these environment variables (or add them to a `.env` file):

- `ORACLE_CONNECTION_STRING`
- `REDSHIFT_CONNECTION_STRING`
- `REDSHIFT_DB` (default: `scoaa`)
- `STAGING_SCHEMA` (default: `staging`)
- `SPEDIA_SCHEMA` (default: `spedia`)
- `ORACLE_SOURCE_TABLE` (default: `source_data`)
- `STAGING_TABLE` (default: `raw_data`)
- `SPEDIA_TABLE` (default: `transformed_data`)

## Run locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```
