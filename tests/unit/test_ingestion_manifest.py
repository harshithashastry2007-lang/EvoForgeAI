"""Tests for static Python repository manifest analysis."""

from pathlib import Path, PurePosixPath

from engine.ingestion.manifest import RepositoryManifestAnalyzer
from engine.ingestion.models import (
    RepositoryFileRecord,
    RepositoryIngestionSummary,
)


def make_record(
    relative_path: str,
    *,
    is_python: bool,
) -> RepositoryFileRecord:
    """Create deterministic scanner evidence for a test file."""

    return RepositoryFileRecord(
        relative_path=relative_path,
        size_bytes=10,
        suffix=PurePosixPath(relative_path).suffix.lower(),
        is_python=is_python,
        sha256="a" * 64,
    )


def test_manifest_classifies_python_repository_structure() -> None:
    summary = RepositoryIngestionSummary(
        repository_name="sample",
        repository_path=Path(r"C:\sample"),
        total_files=6,
        total_bytes=60,
        python_files=3,
        skipped_files=0,
        files=(
            make_record("engine/__init__.py", is_python=True),
            make_record("engine/service.py", is_python=True),
            make_record("tests/test_service.py", is_python=True),
            make_record("pyproject.toml", is_python=False),
            make_record("requirements-dev.txt", is_python=False),
            make_record("docker-compose.yml", is_python=False),
        ),
    )

    manifest = RepositoryManifestAnalyzer().analyze(summary)

    assert manifest.python_files == (
        "engine/__init__.py",
        "engine/service.py",
        "tests/test_service.py",
    )
    assert manifest.test_files == ("tests/test_service.py",)
    assert manifest.package_directories == ("engine",)
    assert manifest.dependency_files == (
        "pyproject.toml",
        "requirements-dev.txt",
    )
    assert manifest.configuration_files == (
        "docker-compose.yml",
        "pyproject.toml",
    )
    assert manifest.has_pyproject is True
    assert manifest.has_tests is True
    assert manifest.python_file_count == 3


def test_manifest_handles_empty_repository() -> None:
    summary = RepositoryIngestionSummary(
        repository_name="empty",
        repository_path=Path(r"C:\empty"),
        total_files=0,
        total_bytes=0,
        python_files=0,
        skipped_files=0,
        files=(),
    )

    manifest = RepositoryManifestAnalyzer().analyze(summary)

    assert manifest.python_files == ()
    assert manifest.test_files == ()
    assert manifest.package_directories == ()
    assert manifest.dependency_files == ()
    assert manifest.configuration_files == ()
    assert manifest.has_pyproject is False
    assert manifest.has_tests is False
    assert manifest.python_file_count == 0