from fastapi import FastAPI

from app.routers import data_pull, data_transformation, orchestrator

app = FastAPI(title="ETL Pipeline for CMAT data")

app.include_router(data_pull.router)
app.include_router(data_transformation.router)
app.include_router(orchestrator.router)


@app.get("/health", summary="Check API health")
def health_check():
    return {"status": "OK"}
