# EvoForge AI



**Autonomous, Self-Healing and Verifiable Software Engineering Platform**



EvoForge AI is an AI-assisted software engineering platform designed to analyze Python repositories, reproduce software failures, localize likely root causes, generate candidate repairs, verify them inside isolated environments, and present evidence-backed recommendations for human approval.



> Current status: Professional foundation and backend infrastructure under development.



## Core Workflow



1. Ingest a Python repository and issue description.

2. Inspect repository structure, dependencies, tests, and execution metadata.

3. Reproduce the reported failure in an isolated sandbox.

4. Analyze execution evidence and localize probable root causes.

5. Generate a maximum of three candidate patches.

6. Run targeted tests, regression tests, static analysis, and security checks.

7. Rank patches using evidence, risk, and confidence.

8. Abstain when evidence is insufficient or a repair is unsafe.

9. Require human approval before applying any patch.



## Key Principles



- Evidence before automation

- Human approval before repository modification

- Sandboxed execution of untrusted code

- Reproducible experiments and evaluations

- Explicit uncertainty and safe abstention

- No fabricated test results or confidence values

- Measurable performance against established bug benchmarks



## Planned Technical Areas



- Repository ingestion and program analysis

- Failure reproduction

- Static and dynamic analysis

- AI-assisted fault localization

- Retrieval-augmented repair

- Multi-candidate patch generation

- Test and regression verification

- Security scanning

- Evidence-based patch ranking

- Human-in-the-loop approval

- Benchmark evaluation and experiment tracking



## Technology Foundation



- Python 3.12

- FastAPI

- Pydantic

- SQLAlchemy and SQLite

- NetworkX

- Pytest

- Ruff

- MyPy

- Bandit

- pip-audit

- Docker

- GitHub Actions



## Local Setup



```cmd

cd /d C:\Harshitha\EvoForgeAI

py -3.12 -m venv .venv

.venv\Scripts\activate

python -m pip install --upgrade pip setuptools wheel

python -m pip install -e ".[dev]"

copy .env.example .env

```



## Run the Backend



```cmd

python -m uvicorn backend.app.main:app --reload

```



Open:



- API root: `http://127.0.0.1:8000/`

- Health check: `http://127.0.0.1:8000/health`

- Swagger documentation: `http://127.0.0.1:8000/docs`



## Quality Verification



```cmd

python -m ruff check backend tests

python -m mypy backend tests

python -m pytest --cov=backend --cov-report=term-missing

python -m bandit -r backend

python -m pip\_audit

```



## Current Verification Results



- Unit tests: 2 passed

- Test coverage: 100%

- Ruff: passed

- MyPy strict mode: passed

- Bandit issues: 0

- Known dependency vulnerabilities: 0



## Repository Structure



- `backend/` - FastAPI application and backend services

- `engine/` - analysis, localization, repair, retrieval, and verification engines

- `frontend/` - future user interface

- `sandbox/` - isolated execution workspace

- `evaluation/` - benchmarks, baselines, and metrics

- `data/` - controlled, raw, and processed datasets

- `tests/` - unit, integration, and security tests

- `docs/` - architecture, decisions, evaluation, and continuity documentation

- `infra/` - Docker and deployment configuration

- `artifacts/` - generated reports and experiment outputs



## Safety Notice



EvoForge AI must not execute untrusted repositories directly on the host system. Repository execution and patch verification will use restricted containers with resource limits, disabled privilege escalation, controlled networking, and explicit human approval.



## Project Stage



Phase 0 - Research, scope, safety, evaluation, and project charter: **Completed**



Phase 1 - Professional foundation, environment, repository, backend, testing, security, container, and CI setup: **In progress**



## License



A license will be selected before the first public release.
