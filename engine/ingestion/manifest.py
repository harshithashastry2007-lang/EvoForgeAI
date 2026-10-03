"""Static repository-structure analysis using ingestion evidence."""

from pathlib import PurePosixPath

from pydantic import BaseModel, ConfigDict, Field

from engine.ingestion.models import RepositoryIngestionSummary

DEPENDENCY_FILE_NAMES = frozenset(
    {
        "pipfile",
        "pipfile.lock",
        "poetry.lock",
        "pyproject.toml",
        "requirements.txt",
        "setup.cfg",
        "setup.py",
        "uv.lock",
    }
)

CONFIG_FILE_NAMES = frozenset(
    {
        ".editorconfig",
        ".pre-commit-config.yaml",
        "docker-compose.yml",
        "mypy.ini",
        "pytest.ini",
        "ruff.toml",
        "tox.ini",
    }
)


class PythonRepositoryManifest(BaseModel):
    """Evidence-based description of a Python repository structure."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    python_files: tuple[str, ...]
    test_files: tuple[str, ...]
    package_directories: tuple[str, ...]
    dependency_files: tuple[str, ...]
    configuration_files: tuple[str, ...]
    has_pyproject: bool
    has_tests: bool
    python_file_count: int = Field(ge=0)


class RepositoryManifestAnalyzer:
    """Classify scanned paths without importing repository code."""

    def analyze(
        self,
        summary: RepositoryIngestionSummary,
    ) -> PythonRepositoryManifest:
        """Build a deterministic manifest from scanner evidence."""

        python_files: list[str] = []
        test_files: list[str] = []
        package_directories: set[str] = set()
        dependency_files: list[str] = []
        configuration_files: list[str] = []

        for record in summary.files:
            path = PurePosixPath(record.relative_path)
            normalized_name = path.name.lower()

            if record.is_python:
                python_files.append(record.relative_path)

                if (
                    "tests" in {part.lower() for part in path.parts}
                    or normalized_name.startswith("test_")
                    or normalized_name.endswith("_test.py")
                ):
                    test_files.append(record.relative_path)

                if normalized_name == "__init__.py":
                    parent = path.parent.as_posix()
                    if parent != ".":
                        package_directories.add(parent)

            if (
                normalized_name in DEPENDENCY_FILE_NAMES
                or (
                    normalized_name.startswith("requirements")
                    and normalized_name.endswith(".txt")
                )
            ):
                dependency_files.append(record.relative_path)

            if (
                normalized_name in CONFIG_FILE_NAMES
                or normalized_name.endswith((".yaml", ".yml", ".toml"))
            ):
                configuration_files.append(record.relative_path)

        sorted_python_files = tuple(sorted(python_files))
        sorted_test_files = tuple(sorted(test_files))
        sorted_dependency_files = tuple(sorted(dependency_files))
        sorted_configuration_files = tuple(sorted(configuration_files))

        return PythonRepositoryManifest(
            python_files=sorted_python_files,
            test_files=sorted_test_files,
            package_directories=tuple(sorted(package_directories)),
            dependency_files=sorted_dependency_files,
            configuration_files=sorted_configuration_files,
            has_pyproject="pyproject.toml" in sorted_dependency_files,
            has_tests=bool(sorted_test_files),
            python_file_count=len(sorted_python_files),
        )