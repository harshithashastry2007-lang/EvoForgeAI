"""Integration tests for the unified repository-ingestion pipeline."""

from pathlib import Path

from engine.ingestion.models import RepositoryIngestionRequest
from engine.ingestion.pipeline import RepositoryIngestionPipeline


def test_pipeline_produces_complete_deterministic_report(
    tmp_path: Path,
) -> None:
    repository = tmp_path / "sample-repository"
    package_directory = repository / "src"
    tests_directory = repository / "tests"
    package_directory.mkdir(parents=True)
    tests_directory.mkdir()

    (package_directory / "__init__.py").write_text(
        '"""Sample package."""\n',
        encoding="utf-8",
    )
    (tests_directory / "test_sample.py").write_text(
        "def test_sample() -> None:\n"
        "    assert True\n",
        encoding="utf-8",
    )
    (repository / "pyproject.toml").write_text(
        (
            "[project]\n"
            'name = "sample"\n'
            'dependencies = ["fastapi>=0.115"]\n'
        ),
        encoding="utf-8",
    )

    request = RepositoryIngestionRequest(repository_path=repository)
    pipeline = RepositoryIngestionPipeline()

    first_report = pipeline.run(request)
    second_report = pipeline.run(request)

    assert first_report == second_report
    assert len(first_report.evidence_id) == 64
    assert first_report.schema_version == "1.0"
    assert first_report.scan.total_files == 3
    assert first_report.scan.python_files == 2
    assert first_report.manifest.package_directories == ("src",)
    assert first_report.manifest.has_tests is True
    assert first_report.dependencies.total_declarations == 1


def test_pipeline_evidence_changes_when_repository_changes(
    tmp_path: Path,
) -> None:
    repository = tmp_path / "sample-repository"
    repository.mkdir()
    source_file = repository / "main.py"
    source_file.write_text("value = 1\n", encoding="utf-8")

    request = RepositoryIngestionRequest(repository_path=repository)
    pipeline = RepositoryIngestionPipeline()
    first_report = pipeline.run(request)

    source_file.write_text("value = 2\n", encoding="utf-8")
    second_report = pipeline.run(request)

    assert first_report.evidence_id != second_report.evidence_id
    assert first_report.scan.files[0].sha256 != second_report.scan.files[0].sha256