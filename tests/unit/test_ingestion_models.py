"""Tests for secure repository-ingestion models."""

from pathlib import Path

import pytest
from pydantic import ValidationError

from engine.ingestion.models import (
    RepositoryFileRecord,
    RepositoryIngestionRequest,
    RepositorySourceType,
)


def test_ingestion_request_accepts_absolute_path() -> None:
    request = RepositoryIngestionRequest(
        repository_path=Path(r"C:\Harshitha\EvoForgeAI")
    )

    assert request.source_type == RepositorySourceType.LOCAL_DIRECTORY
    assert request.max_files == 5_000
    assert request.max_total_bytes == 100 * 1024 * 1024
    assert request.max_file_bytes == 2 * 1024 * 1024


def test_ingestion_request_rejects_relative_path() -> None:
    with pytest.raises(
        ValidationError,
        match="repository_path must be an absolute path",
    ):
        RepositoryIngestionRequest(repository_path=Path("relative/repository"))


def test_file_record_requires_valid_sha256() -> None:
    with pytest.raises(ValidationError):
        RepositoryFileRecord(
            relative_path="backend/app/main.py",
            size_bytes=100,
            suffix=".py",
            is_python=True,
            sha256="invalid-hash",
        )


def test_file_record_accepts_valid_metadata() -> None:
    record = RepositoryFileRecord(
        relative_path="backend/app/main.py",
        size_bytes=100,
        suffix=".py",
        is_python=True,
        sha256="a" * 64,
    )

    assert record.is_python is True
    assert record.sha256 == "a" * 64