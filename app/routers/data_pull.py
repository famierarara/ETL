from fastapi import APIRouter

from app.services.data_service import pull_data

router = APIRouter(prefix="/data_pull", tags=["data_pull"])


@router.post("", summary="Pull data from Oracle and load into Redshift staging")
def data_pull():
    """Pull data from Oracle and load it into the Redshift staging schema."""
    return pull_data()
