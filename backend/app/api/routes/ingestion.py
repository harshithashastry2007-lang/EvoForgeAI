"""API routes for safe repository ingestion."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.core.config import Settings, get_settings
from engine.ingestion.exceptions import (
    InvalidRepositoryError,
    RepositoryLimitExceededError,
    RepositoryNotFoundError,
    UnsafeRepositoryPathError,
)
from engine.ingestion.models import RepositoryIngestionRequest
from engine.ingestion.pipeline import (
    RepositoryIngestionPipeline,
    RepositoryIngestionReport,
)

router = APIRouter(
    prefix="/api/v1/ingestion",
    tags=["Repository Ingestion"],
)


@router.post(
    "/analyze",
    response_model=RepositoryIngestionReport,
    status_code=status.HTTP_200_OK,
)
def analyze_repository(
    request: RepositoryIngestionRequest,
    settings: Annotated[Settings, Depends(get_settings)],
) -> RepositoryIngestionReport:
    """Analyze a repository inside the configured controlled directory."""

    allowed_root = settings.ingestion_allowed_root.resolve()
    requested_path = request.repository_path.resolve()

    if not requested_path.is_relative_to(allowed_root):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Repository path is outside the allowed ingestion root",
        )

    try:
        return RepositoryIngestionPipeline().run(request)
    except RepositoryNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except (InvalidRepositoryError, UnsafeRepositoryPathError) as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except RepositoryLimitExceededError as exc:
        raise HTTPException(
            status.HTTP_413_CONTENT_TOO_LARGE,
            detail=str(exc),
        ) from exc