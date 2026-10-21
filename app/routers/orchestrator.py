from fastapi import APIRouter

from app.services.data_service import pull_data, transform_data

router = APIRouter(prefix="/orchestrator", tags=["orchestrator"])


@router.post("", summary="Run data pull and data transformation in sequence")
def orchestrator():
    """Run data pull and data transformation in sequence."""
    pull_result = pull_data()
    transform_result = transform_data()

    return {
        "status": "success",
        "steps": ["data_pull", "data_transformation"],
        "pull_result": pull_result,
        "transform_result": transform_result,
    }
