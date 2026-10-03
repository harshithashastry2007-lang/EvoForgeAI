"""Tests for safe, non-executing repository scanning."""

import hashlib
from pathlib import Path

import pytest

from engine.ingestion.exceptions import (
    InvalidRepositoryError,
    RepositoryLimitExceededError,
    RepositoryNotFoundError,
)
from engine.ingestion.models import RepositoryIngestionRequest
from engine.ingestion.scanner import RepositoryScanner


def test_scanner_collects_metadata_without_executing_code(tmp_path: Path) -> None:
    repository = tmp_path / "sample-repository"
    source_directory = repository / "src"
    source_directory.mkdir(parents=True)

    dangerous_file = source_directory / "dangerous.py"
    marker_file = repository / "executed.txt"
    dangerous_content = (
        "from pathlib import Path\n"
        f"Path({str(marker_file)!r}).write_text('executed')\n"
    )
    dangerous_file.write_text(dangerous_content, encoding="utf-8")
    (repository / "README.md").write_text("# Sample", encoding="utf-8")

    summary = RepositoryScanner(
        RepositoryIngestionRequest(repository_path=repository)
    ).scan()

    expected_digest = hashlib.sha256(dangerous_file.read_bytes()).hexdigest()

    assert summary.repository_name == "sample-repository"
    assert summary.total_files == 2
    assert summary.python_files == 1
    assert marker_file.exists() is False
    assert any(
        record.sha256 == expected_digest
        for record in summary.files
    )


def test_scanner_skips_sensitive_binary_and_excluded_files(
    tmp_path: Path,
) -> None:
    repository = tmp_path / "sample-repository"
    git_directory = repository / ".git"
    git_directory.mkdir(parents=True)

    (repository / ".env").write_text("SECRET=value", encoding="utf-8")
    (repository / "image.png").write_bytes(b"\x89PNG")
    (git_directory / "config").write_text("private", encoding="utf-8")

    summary = RepositoryScanner(
        RepositoryIngestionRequest(repository_path=repository)
    ).scan()

    assert summary.total_files == 0
    assert summary.skipped_files == 2
    assert len(summary.warnings) == 2


def test_scanner_rejects_missing_repository(tmp_path: Path) -> None:
    missing_repository = tmp_path / "missing"

    with pytest.raises(RepositoryNotFoundError):
        RepositoryScanner(
            RepositoryIngestionRequest(
                repository_path=missing_repository
            )
        ).scan()


def test_scanner_rejects_file_as_repository(tmp_path: Path) -> None:
    file_path = tmp_path / "not-a-repository.txt"
    file_path.write_text("content", encoding="utf-8")

    with pytest.raises(InvalidRepositoryError):
        RepositoryScanner(
            RepositoryIngestionRequest(repository_path=file_path)
        ).scan()


def test_scanner_enforces_file_count_limit(tmp_path: Path) -> None:
    repository = tmp_path / "sample-repository"
    repository.mkdir()
    (repository / "a.py").write_text("a = 1", encoding="utf-8")
    (repository / "b.py").write_text("b = 2", encoding="utf-8")

    with pytest.raises(RepositoryLimitExceededError):
        RepositoryScanner(
            RepositoryIngestionRequest(
                repository_path=repository,
                max_files=1,
            )
        ).scan()


def test_scanner_enforces_total_byte_limit(tmp_path: Path) -> None:
    repository = tmp_path / "sample-repository"
    repository.mkdir()
    (repository / "large.txt").write_text("12345", encoding="utf-8")

    with pytest.raises(RepositoryLimitExceededError):
        RepositoryScanner(
            RepositoryIngestionRequest(
                repository_path=repository,
                max_total_bytes=4,
            )
        ).scan()


def test_scanner_skips_oversized_individual_file(tmp_path: Path) -> None:
    repository = tmp_path / "sample-repository"
    repository.mkdir()
    (repository / "large.txt").write_text("12345", encoding="utf-8")

    summary = RepositoryScanner(
        RepositoryIngestionRequest(
            repository_path=repository,
            max_file_bytes=4,
        )
    ).scan()

    assert summary.total_files == 0
    assert summary.skipped_files == 1
    assert summary.warnings == ("Skipped oversized file: large.txt",)