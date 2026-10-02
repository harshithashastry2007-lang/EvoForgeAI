# Changelog



All notable changes to EvoForge AI will be documented in this file.



The project follows the principles of Keep a Changelog and Semantic Versioning.



## Unreleased



### Added



- Professional repository structure

- Python 3.12 virtual environment

- Modern `pyproject.toml` configuration

- Reproducible `requirements.lock`

- FastAPI application foundation

- Root and health-check endpoints

- Swagger UI and ReDoc documentation

- Validated environment-based settings

- Restricted CORS configuration

- Secret-protection defaults

- Unit tests for initial API endpoints

- Minimum 80% test-coverage requirement

- Ruff linting configuration

- MyPy strict type checking

- Bandit source-code security scanning

- pip-audit dependency vulnerability scanning

- Secure non-root backend Dockerfile

- Resource-limited Docker Compose configuration

- GitHub Actions quality and security workflow

- Professional README

- Project-state and continuity documentation

- Fifteen-phase implementation roadmap after Phase 0



### Verification



- Unit tests: 2 passed

- Coverage: 100%

- Ruff: passed

- MyPy: passed

- Bandit: zero issues

- pip-audit: zero known vulnerabilities



### Known Issues



- FastAPI TestClient produces a dependency-level Starlette deprecation warning related to `httpx`.

- Docker execution has not yet been tested because Docker Desktop and WSL2 are not installed.
