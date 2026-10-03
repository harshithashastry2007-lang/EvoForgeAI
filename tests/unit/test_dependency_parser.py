"""Tests for safe dependency-manifest parsing."""

import hashlib
from pathlib import Path

from engine.ingestion.dependency_models import DependencyManifestType
from engine.ingestion.dependency_parser import DependencyManifestParser
from engine.ingestion.models import (
    RepositoryFileRecord,
    RepositoryIngestionSummary,
)


def make_record(
    repository: Path,
    file_path: Path,
) -> RepositoryFileRecord:
    """Create scanner evidence matching a real test file."""

    content = file_path.read_bytes()
    return RepositoryFileRecord(
        relative_path=file_path.relative_to(repository).as_posix(),
        size_bytes=len(content),
        suffix=file_path.suffix.lower(),
        is_python=False,
        sha256=hashlib.sha256(content).hexdigest(),
    )


def make_summary(
    repository: Path,
    records: tuple[RepositoryFileRecord, ...],
) -> RepositoryIngestionSummary:
    """Create a repository summary for parser tests."""

    return RepositoryIngestionSummary(
        repository_name=repository.name,
        repository_path=repository,
        total_files=len(records),
        total_bytes=sum(record.size_bytes for record in records),
        python_files=0,
        skipped_files=0,
        files=records,
    )


def test_parser_extracts_pyproject_and_requirements(
    tmp_path: Path,
) -> None:
    repository = tmp_path / "repository"
    repository.mkdir()

    pyproject = repository / "pyproject.toml"
    pyproject.write_text(
        (
            "[project]\n"
            'name = "sample"\n'
            'dependencies = ["fastapi>=0.115", "pydantic>=2.9"]\n'
            "\n"
            "[project.optional-dependencies]\n"
            'dev = ["pytest>=8.3"]\n'
        ),
        encoding="utf-8",
    )

    requirements = repository / "requirements.txt"
    requirements.write_text(
        "httpx>=0.27\n-r unsafe-extra.txt\n# comment\n",
        encoding="utf-8",
    )

    summary = make_summary(
        repository,
        (
            make_record(repository, pyproject),
            make_record(repository, requirements),
        ),
    )

    report = DependencyManifestParser().analyze(summary)

    assert report.total_declarations == 4
    assert len(report.manifests) == 2
    assert report.manifests[0].manifest_type == DependencyManifestType.PYPROJECT
    assert report.manifests[1].manifest_type == DependencyManifestType.REQUIREMENTS
    assert report.manifests[1].parse_warnings == (
        "Ignored requirements directive on line 2",
    )


def test_parser_rejects_file_changed_after_ingestion(
    tmp_path: Path,
) -> None:
    repository = tmp_path / "repository"
    repository.mkdir()
    requirements = repository / "requirements.txt"
    requirements.write_text("fastapi\n", encoding="utf-8")

    record = make_record(repository, requirements)
    requirements.write_text("different-package\n", encoding="utf-8")

    report = DependencyManifestParser().analyze(
        make_summary(repository, (record,))
    )

    assert report.manifests == ()
    assert report.warnings == (
        "File changed after ingestion: requirements.txt",
    )


def test_parser_reports_invalid_pyproject_toml(tmp_path: Path) -> None:
    repository = tmp_path / "repository"
    repository.mkdir()
    pyproject = repository / "pyproject.toml"
    pyproject.write_text("[project\ninvalid", encoding="utf-8")

    report = DependencyManifestParser().analyze(
        make_summary(
            repository,
            (make_record(repository, pyproject),),
        )
    )

    assert report.total_declarations == 0
    assert len(report.manifests) == 1
    assert report.manifests[0].parse_warnings
    assert report.manifests[0].parse_warnings[0].startswith("Invalid TOML:")


def test_parser_rejects_path_outside_repository(tmp_path: Path) -> None:
    repository = tmp_path / "repository"
    repository.mkdir()
    outside_file = tmp_path / "requirements.txt"
    outside_file.write_text("unsafe-package\n", encoding="utf-8")
    content = outside_file.read_bytes()

    unsafe_record = RepositoryFileRecord(
        relative_path="../requirements.txt",
        size_bytes=len(content),
        suffix=".txt",
        is_python=False,
        sha256=hashlib.sha256(content).hexdigest(),
    )

    report = DependencyManifestParser().analyze(
        make_summary(repository, (unsafe_record,))
    )

    assert report.manifests == ()
    assert report.warnings == (
        "Rejected path outside repository: ../requirements.txt",
    )