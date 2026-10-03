"""Safe parsing of verified Python dependency manifests."""

import hashlib
import tomllib
from pathlib import PurePosixPath
from typing import Any

from engine.ingestion.dependency_models import (
    DependencyAnalysisReport,
    DependencyDeclaration,
    DependencyManifestEvidence,
    DependencyManifestType,
)
from engine.ingestion.models import (
    RepositoryFileRecord,
    RepositoryIngestionSummary,
)


class DependencyManifestParser:
    """Extract dependency evidence without installing or importing packages."""

    def analyze(
        self,
        summary: RepositoryIngestionSummary,
    ) -> DependencyAnalysisReport:
        """Parse supported manifests after verifying path and file hash."""

        repository_root = summary.repository_path.resolve()
        manifests: list[DependencyManifestEvidence] = []
        warnings: list[str] = []

        for record in summary.files:
            manifest_type = self._manifest_type(record)

            if manifest_type is None:
                continue

            manifest_path = repository_root.joinpath(
                *PurePosixPath(record.relative_path).parts
            ).resolve()

            if not manifest_path.is_relative_to(repository_root):
                warnings.append(
                    f"Rejected path outside repository: {record.relative_path}"
                )
                continue

            try:
                content = manifest_path.read_bytes()
            except OSError as exc:
                warnings.append(
                    f"Could not read {record.relative_path}: "
                    f"{exc.__class__.__name__}"
                )
                continue

            actual_sha256 = hashlib.sha256(content).hexdigest()

            if actual_sha256 != record.sha256:
                warnings.append(
                    f"File changed after ingestion: {record.relative_path}"
                )
                continue

            try:
                text = content.decode("utf-8")
            except UnicodeDecodeError:
                warnings.append(
                    f"Manifest is not valid UTF-8: {record.relative_path}"
                )
                continue

            if manifest_type == DependencyManifestType.PYPROJECT:
                declarations, parse_warnings = self._parse_pyproject(
                    text,
                    record.relative_path,
                )
            else:
                declarations, parse_warnings = self._parse_requirements(
                    text,
                    record.relative_path,
                )

            manifests.append(
                DependencyManifestEvidence(
                    relative_path=record.relative_path,
                    manifest_type=manifest_type,
                    sha256=actual_sha256,
                    declarations=declarations,
                    parse_warnings=parse_warnings,
                )
            )

        return DependencyAnalysisReport(
            manifests=tuple(sorted(manifests, key=lambda item: item.relative_path)),
            total_declarations=sum(
                len(manifest.declarations) for manifest in manifests
            ),
            warnings=tuple(warnings),
        )

    @staticmethod
    def _manifest_type(
        record: RepositoryFileRecord,
    ) -> DependencyManifestType | None:
        name = PurePosixPath(record.relative_path).name.lower()

        if name == "pyproject.toml":
            return DependencyManifestType.PYPROJECT

        if name.startswith("requirements") and name.endswith(".txt"):
            return DependencyManifestType.REQUIREMENTS

        return None

    @staticmethod
    def _parse_pyproject(
        text: str,
        source_file: str,
    ) -> tuple[tuple[DependencyDeclaration, ...], tuple[str, ...]]:
        try:
            document: dict[str, Any] = tomllib.loads(text)
        except tomllib.TOMLDecodeError as exc:
            return (), (f"Invalid TOML: {exc}",)

        declarations: list[DependencyDeclaration] = []
        warnings: list[str] = []
        project = document.get("project")

        if not isinstance(project, dict):
            return (), ("Missing [project] table",)

        dependencies = project.get("dependencies", [])

        if isinstance(dependencies, list):
            for dependency in dependencies:
                if isinstance(dependency, str) and dependency.strip():
                    declarations.append(
                        DependencyDeclaration(
                            declaration=dependency.strip(),
                            group="runtime",
                            source_file=source_file,
                        )
                    )
                else:
                    warnings.append("Ignored invalid runtime dependency")
        else:
            warnings.append("project.dependencies must be a list")

        optional_dependencies = project.get("optional-dependencies", {})

        if isinstance(optional_dependencies, dict):
            for group, group_dependencies in optional_dependencies.items():
                if not isinstance(group, str) or not isinstance(
                    group_dependencies,
                    list,
                ):
                    warnings.append("Ignored invalid optional dependency group")
                    continue

                for dependency in group_dependencies:
                    if isinstance(dependency, str) and dependency.strip():
                        declarations.append(
                            DependencyDeclaration(
                                declaration=dependency.strip(),
                                group=f"optional:{group}",
                                source_file=source_file,
                            )
                        )
                    else:
                        warnings.append(
                            f"Ignored invalid dependency in group {group}"
                        )
        else:
            warnings.append("project.optional-dependencies must be a table")

        return tuple(declarations), tuple(warnings)

    @staticmethod
    def _parse_requirements(
        text: str,
        source_file: str,
    ) -> tuple[tuple[DependencyDeclaration, ...], tuple[str, ...]]:
        declarations: list[DependencyDeclaration] = []
        warnings: list[str] = []

        for line_number, original_line in enumerate(text.splitlines(), start=1):
            line = original_line.strip()

            if not line or line.startswith("#"):
                continue

            if line.startswith("-"):
                warnings.append(
                    f"Ignored requirements directive on line {line_number}"
                )
                continue

            if len(line) > 2_000:
                warnings.append(
                    f"Ignored oversized declaration on line {line_number}"
                )
                continue

            declarations.append(
                DependencyDeclaration(
                    declaration=line,
                    group="runtime",
                    source_file=source_file,
                )
            )

        return tuple(declarations), tuple(warnings)