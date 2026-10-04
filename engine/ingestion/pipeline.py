"""Unified, evidence-producing repository ingestion pipeline."""

import hashlib

from pydantic import BaseModel, ConfigDict, Field

from engine.ingestion.dependency_models import DependencyAnalysisReport
from engine.ingestion.dependency_parser import DependencyManifestParser
from engine.ingestion.manifest import (
    PythonRepositoryManifest,
    RepositoryManifestAnalyzer,
)
from engine.ingestion.models import (
    RepositoryIngestionRequest,
    RepositoryIngestionSummary,
)
from engine.ingestion.scanner import RepositoryScanner


class RepositoryIngestionReport(BaseModel):
    """Complete evidence report produced by safe repository ingestion."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: str = Field(default="1.0", pattern=r"^\d+\.\d+$")
    evidence_id: str = Field(pattern=r"^[a-f0-9]{64}$")
    scan: RepositoryIngestionSummary
    manifest: PythonRepositoryManifest
    dependencies: DependencyAnalysisReport


class RepositoryIngestionPipeline:
    """Coordinate scanning and static analysis without executing code."""

    def run(
        self,
        request: RepositoryIngestionRequest,
    ) -> RepositoryIngestionReport:
        """Produce a deterministic evidence report for one repository."""

        scan = RepositoryScanner(request).scan()
        manifest = RepositoryManifestAnalyzer().analyze(scan)
        dependencies = DependencyManifestParser().analyze(scan)
        evidence_id = self._create_evidence_id(
            scan,
            manifest,
            dependencies,
        )

        return RepositoryIngestionReport(
            evidence_id=evidence_id,
            scan=scan,
            manifest=manifest,
            dependencies=dependencies,
        )

    @staticmethod
    def _create_evidence_id(
        scan: RepositoryIngestionSummary,
        manifest: PythonRepositoryManifest,
        dependencies: DependencyAnalysisReport,
    ) -> str:
        canonical_evidence = "|".join(
            (
                scan.model_dump_json(),
                manifest.model_dump_json(),
                dependencies.model_dump_json(),
            )
        )
        return hashlib.sha256(canonical_evidence.encode("utf-8")).hexdigest()