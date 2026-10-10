"""Integration tests for the secure repository-ingestion API."""

from pathlib import Path

from fastapi.testclient import TestClient

from backend.app.core.config import Settings, get_settings
from backend.app.main import app


def test_ingestion_endpoint_analyzes_repository_inside_allowed_root(
    tmp_path: Path,
) -> None:
    controlled_root = tmp_path / "controlled"
    repository = controlled_root / "sample-repository"
    repository.mkdir(parents=True)
    (repository / "main.py").write_text("value = 1\n", encoding="utf-8")
    (repository / "pyproject.toml").write_text(
        (
            "[project]\n"
            'name = "sample"\n'
            'dependencies = ["fastapi>=0.115"]\n'
        ),
        encoding="utf-8",
    )

    settings = Settings(ingestion_allowed_root=controlled_root)
    app.dependency_overrides[get_settings] = lambda: settings

    try:
        with TestClient(app) as client:
            response = client.post(
                "/api/v1/ingestion/analyze",
                json={"repository_path": str(repository)},
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    payload = response.json()
    assert payload["schema_version"] == "1.0"
    assert len(payload["evidence_id"]) == 64
    assert payload["scan"]["total_files"] == 2
    assert payload["manifest"]["python_file_count"] == 1
    assert payload["dependencies"]["total_declarations"] == 1


def test_ingestion_endpoint_rejects_path_outside_allowed_root(
    tmp_path: Path,
) -> None:
    controlled_root = tmp_path / "controlled"
    controlled_root.mkdir()
    outside_repository = tmp_path / "outside"
    outside_repository.mkdir()

    settings = Settings(ingestion_allowed_root=controlled_root)
    app.dependency_overrides[get_settings] = lambda: settings

    try:
        with TestClient(app) as client:
            response = client.post(
                "/api/v1/ingestion/analyze",
                json={"repository_path": str(outside_repository)},
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 403
    assert response.json() == {
        "detail": "Repository path is outside the allowed ingestion root"
    }


def test_ingestion_endpoint_reports_missing_repository(
    tmp_path: Path,
) -> None:
    controlled_root = tmp_path / "controlled"
    controlled_root.mkdir()
    missing_repository = controlled_root / "missing"

    settings = Settings(ingestion_allowed_root=controlled_root)
    app.dependency_overrides[get_settings] = lambda: settings

    try:
        with TestClient(app) as client:
            response = client.post(
                "/api/v1/ingestion/analyze",
                json={"repository_path": str(missing_repository)},
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 404


def test_ingestion_endpoint_enforces_file_limit(tmp_path: Path) -> None:
    controlled_root = tmp_path / "controlled"
    repository = controlled_root / "large-repository"
    repository.mkdir(parents=True)
    (repository / "first.py").write_text("first = 1\n", encoding="utf-8")
    (repository / "second.py").write_text("second = 2\n", encoding="utf-8")

    settings = Settings(ingestion_allowed_root=controlled_root)
    app.dependency_overrides[get_settings] = lambda: settings

    try:
        with TestClient(app) as client:
            response = client.post(
                "/api/v1/ingestion/analyze",
                json={
                    "repository_path": str(repository),
                    "max_files": 1,
                },
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 413