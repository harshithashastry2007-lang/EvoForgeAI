"""Validated data models for safe repository ingestion."""

from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, field_validator


class RepositorySourceType(StrEnum):
    """Supported repository input types."""

    LOCAL_DIRECTORY = "local_directory"


class RepositoryIngestionRequest(BaseModel):
    """Validated request for inspecting a local repository."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    source_type: RepositorySourceType = RepositorySourceType.LOCAL_DIRECTORY
    repository_path: Path
    max_files: int = Field(default=5_000, ge=1, le=50_000)
    max_total_bytes: int = Field(
        default=100 * 1024 * 1024,
        ge=1,
        le=1024 * 1024 * 1024,
    )
    max_file_bytes: int = Field(
        default=2 * 1024 * 1024,
        ge=1,
        le=20 * 1024 * 1024,
    )

    @field_validator("repository_path")
    @classmethod
    def validate_repository_path(cls, value: Path) -> Path:
        """Reject relative repository paths."""

        if not value.is_absolute():
            raise ValueError("repository_path must be an absolute path")

        return value


class RepositoryFileRecord(BaseModel):
    """Metadata collected for one file without executing it."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    relative_path: str
    size_bytes: int = Field(ge=0)
    suffix: str
    is_python: bool
    sha256: str = Field(pattern=r"^[a-f0-9]{64}$")


class RepositoryIngestionSummary(BaseModel):
    """Evidence produced after safe repository inspection."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    repository_name: str
    repository_path: Path
    total_files: int = Field(ge=0)
    total_bytes: int = Field(ge=0)
    python_files: int = Field(ge=0)
    skipped_files: int = Field(ge=0)
    files: tuple[RepositoryFileRecord, ...]
    warnings: tuple[str, ...] = ()