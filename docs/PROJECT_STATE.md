# EvoForge AI - Project State

```

## Environment

- Windows 11 Home, x64
- Python 3.12 virtual environment
- FastAPI backend
- Git and GitHub repository
- GitHub Actions CI
- Local Docker installation deferred because the computer has 6 GB RAM

## Phase 1 Verification Evidence

- Ruff linting passed
- MyPy strict type checking passed
- Pytest passed
- Backend test coverage reached 100%
- Bandit reported no security issues
- pip-audit reported no known dependency vulnerabilities
- Pre-commit hooks passed
- GitHub Actions workflow passed
- Docker image build and container security validation passed in GitHub Actions
- Container runs as a non-root user
- Container health endpoint was verified successfully

## Current API Endpoints

- `GET /` - service information
- `GET /health` - service health status
- `GET /docs` - interactive OpenAPI documentation

## Known Non-Blocking Issue

FastAPI currently produces a Starlette deprecation warning concerning `httpx` and `TestClient`. The tests still pass, so this warning will be handled during a future dependency-maintenance step.

## Deferred Local Infrastructure

Local Docker Desktop and WSL2 installation are deferred because this computer has 6 GB RAM, below the current Docker Desktop requirement.

Docker build, non-root execution, restricted runtime, and container health were validated successfully through GitHub Actions.

## Next Immediate Action

Begin Phase 2 by implementing safe, non-executing Python repository ingestion.

The ingestion system must inspect repository metadata and files without executing untrusted repository code.

## Standard Verification Commands

```cmd
python -m ruff check backend tests
python -m mypy backend tests
python -m pytest --cov=backend --cov-report=term-missing
python -m bandit -r backend
python -m pip_audit
```

## Safety Requirements

- Never execute an ingested repository during initial inspection.
- Reject unsafe paths and path traversal attempts.
- Enforce repository size and file-count limits.
- Ignore binary files and sensitive environment files.
- Record evidence for every analysis decision.
- Never modify a user repository without explicit human approval.



Last updated: 2 October 2026



## Project Identity



EvoForge AI is an autonomous, self-healing, and verifiable software engineering platform.



Its goal is to analyze Python repositories, reproduce bugs, localize root causes, generate up to three candidate patches, verify those patches in isolated environments, rank them using evidence, and require human approval before applying changes.



## Current Phase



Phase 0: Completed



Phase 1: Professional Project Foundation, Environment and Repository Setup - Completed



Current step: Phase 1 completed; ready to begin Phase 2



## Local Project Location



```text

C:\Harshitha\EvoForgeAI
