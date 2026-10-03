"""Safe, non-executing scanner for local Python repositories."""

import hashlib
import os
from pathlib import Path

from engine.ingestion.exceptions import (
    InvalidRepositoryError,
    RepositoryLimitExceededError,
    RepositoryNotFoundError,
    UnsafeRepositoryPathError,
)
from engine.ingestion.models import (
    RepositoryFileRecord,
    RepositoryIngestionRequest,
    RepositoryIngestionSummary,
)

EXCLUDED_DIRECTORIES = frozenset(
    {
        ".git",
        ".hg",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".tox",
        ".venv",
        "__pycache__",
        "artifacts",
        "dist",
        "node_modules",
        "sandbox",
        "venv",
    }
)

SENSITIVE_FILE_NAMES = frozenset(
    {
        ".env",
        ".npmrc",
        ".pypirc",
        "credentials.json",
        "id_dsa",
        "id_ed25519",
        "id_rsa",
        "secrets.json",
    }
)

BINARY_SUFFIXES = frozenset(
    {
        ".7z",
        ".avi",
        ".bin",
        ".bmp",
        ".class",
        ".dll",
        ".doc",
        ".docx",
        ".exe",
        ".gif",
        ".gz",
        ".ico",
        ".jar",
        ".jpeg",
        ".jpg",
        ".mov",
        ".mp3",
        ".mp4",
        ".pdf",
        ".png",
        ".pyc",
        ".so",
        ".tar",
        ".webp",
        ".xls",
        ".xlsx",
        ".zip",
    }
)


class RepositoryScanner:
    """Collect repository metadata without importing or executing its code."""

    def __init__(self, request: RepositoryIngestionRequest) -> None:
        self._request = request

    def scan(self) -> RepositoryIngestionSummary:
        """Inspect repository files while enforcing configured safety limits."""

        supplied_path = self._request.repository_path

        if supplied_path.is_symlink():
            raise UnsafeRepositoryPathError(
                "repository root must not be a symbolic link"
            )

        repository_root = supplied_path.resolve()

        if not repository_root.exists():
            raise RepositoryNotFoundError(
                f"repository does not exist: {repository_root}"
            )

        if not repository_root.is_dir():
            raise InvalidRepositoryError(
                f"repository path is not a directory: {repository_root}"
            )

        records: list[RepositoryFileRecord] = []
        warnings: list[str] = []
        total_bytes = 0
        python_files = 0
        skipped_files = 0

        for current_root, directory_names, file_names in os.walk(
            repository_root,
            followlinks=False,
        ):
            current_path = Path(current_root)
            allowed_directories: list[str] = []

            for directory_name in sorted(directory_names):
                directory_path = current_path / directory_name

                if (
                    directory_name.lower() in EXCLUDED_DIRECTORIES
                    or directory_path.is_symlink()
                ):
                    continue

                allowed_directories.append(directory_name)

            directory_names[:] = allowed_directories

            for file_name in sorted(file_names):
                file_path = current_path / file_name
                relative_path = file_path.relative_to(repository_root).as_posix()

                if file_path.is_symlink():
                    skipped_files += 1
                    warnings.append(f"Skipped symbolic link: {relative_path}")
                    continue

                if self._is_sensitive(file_path):
                    skipped_files += 1
                    warnings.append(f"Skipped sensitive file: {relative_path}")
                    continue

                if file_path.suffix.lower() in BINARY_SUFFIXES:
                    skipped_files += 1
                    warnings.append(f"Skipped binary file: {relative_path}")
                    continue

                try:
                    size_bytes = file_path.stat().st_size
                except OSError as exc:
                    skipped_files += 1
                    warnings.append(
                        f"Could not inspect {relative_path}: {exc.__class__.__name__}"
                    )
                    continue

                if size_bytes > self._request.max_file_bytes:
                    skipped_files += 1
                    warnings.append(f"Skipped oversized file: {relative_path}")
                    continue

                if len(records) >= self._request.max_files:
                    raise RepositoryLimitExceededError(
                        f"repository exceeds the {self._request.max_files} file limit"
                    )

                if total_bytes + size_bytes > self._request.max_total_bytes:
                    raise RepositoryLimitExceededError(
                        "repository exceeds the configured total-byte limit"
                    )

                try:
                    digest = self._sha256(file_path)
                except OSError as exc:
                    skipped_files += 1
                    warnings.append(
                        f"Could not read {relative_path}: {exc.__class__.__name__}"
                    )
                    continue

                is_python = file_path.suffix.lower() == ".py"
                records.append(
                    RepositoryFileRecord(
                        relative_path=relative_path,
                        size_bytes=size_bytes,
                        suffix=file_path.suffix.lower(),
                        is_python=is_python,
                        sha256=digest,
                    )
                )
                total_bytes += size_bytes
                python_files += int(is_python)

        return RepositoryIngestionSummary(
            repository_name=repository_root.name,
            repository_path=repository_root,
            total_files=len(records),
            total_bytes=total_bytes,
            python_files=python_files,
            skipped_files=skipped_files,
            files=tuple(records),
            warnings=tuple(warnings),
        )

    @staticmethod
    def _is_sensitive(file_path: Path) -> bool:
        normalized_name = file_path.name.lower()
        return (
            normalized_name in SENSITIVE_FILE_NAMES
            or normalized_name.startswith(".env.")
            or file_path.suffix.lower() in {".key", ".pem"}
        )

    @staticmethod
    def _sha256(file_path: Path) -> str:
        digest = hashlib.sha256()

        with file_path.open("rb") as file_handle:
            while chunk := file_handle.read(64 * 1024):
                digest.update(chunk)

        return digest.hexdigest()