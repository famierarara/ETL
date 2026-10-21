from fastapi import APIRouter

from app.services.data_service import transform_data

router = APIRouter(prefix="/data_transformation", tags=["data_transformation"])


@router.post("", summary="Transform staging data and load into spedia")
def data_transformation():
    """Read raw data from the Redshift staging schema, transform it, and write it to the spedia schema."""
    return transform_data()
