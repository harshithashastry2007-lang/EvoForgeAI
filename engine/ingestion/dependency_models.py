"""Evidence models for safe dependency-manifest inspection."""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class DependencyManifestType(StrEnum):
    """Supported dependency-manifest formats."""

    PYPROJECT = "pyproject"
    REQUIREMENTS = "requirements"


class DependencyDeclaration(BaseModel):
    """One dependency declaration preserved as repository evidence."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    declaration: str = Field(min_length=1, max_length=2_000)
    group: str = Field(min_length=1, max_length=200)
    source_file: str = Field(min_length=1)


class DependencyManifestEvidence(BaseModel):
    """Dependencies extracted from one verified manifest file."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    relative_path: str = Field(min_length=1)
    manifest_type: DependencyManifestType
    sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    declarations: tuple[DependencyDeclaration, ...]
    parse_warnings: tuple[str, ...] = ()


class DependencyAnalysisReport(BaseModel):
    """Combined dependency evidence for an ingested repository."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    manifests: tuple[DependencyManifestEvidence, ...]
    total_declarations: int = Field(ge=0)
    warnings: tuple[str, ...] = ()