# EvoForge AI - Next Steps



Last updated: 2 October 2026



## Current Position



Phase 0 is completed.



Phase 1 is in its final documentation and repository-verification stage.



## Immediate Tasks



1. Create `CHANGELOG.md`.

2. Create `SECURITY.md`.

3. Add placeholder files to preserve empty directories.

4. Run all quality, testing, and security checks.

5. Review every file using `git status`.

6. Create the first professional Git commit.

7. Create and connect the GitHub repository.

8. Push the `main` branch.

9. Confirm that GitHub Actions passes.

10. Install Docker Desktop and WSL2 later.

11. Build and test the backend container.

12. Begin Phase 2 repository ingestion.



## Next Development Feature



The first Phase 2 feature will be a safe repository-ingestion component that:



- Accepts only a controlled local Python repository

- Validates the repository path

- Rejects dangerous or unsupported input

- Enumerates source files and tests

- Extracts dependency metadata

- Produces a structured repository manifest

- Does not execute repository code



## Before Every Commit



```cmd

python -m ruff check backend tests

python -m mypy backend tests

python -m pytest --cov=backend --cov-report=term-missing

python -m bandit -r backend

python -m pip\_audit

git status
