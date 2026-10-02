# Security Policy



## Project Status



EvoForge AI is currently under active development and is not ready for production use.



## Security Principles



EvoForge AI follows these mandatory principles:



- Never execute an untrusted repository directly on the host system.

- Use isolated containers with strict resource limits.

- Disable network access during repository execution unless explicitly required and approved.

- Run containers as non-root users.

- Drop unnecessary Linux capabilities.

- Prevent privilege escalation.

- Validate every repository path and uploaded file.

- Never expose secrets through source code, logs, prompts, reports, or generated patches.

- Require human approval before applying a patch.

- Maintain evidence and audit records for important decisions.

- Abstain when a repair cannot be verified safely.



## Protected Information



The following must never be committed:



- `.env` files

- API keys

- Authentication tokens

- Passwords

- Private keys

- User repositories containing confidential code

- Generated artifacts containing secrets

- Local databases containing sensitive information



Only `.env.example` with empty placeholder values may be committed.



## Reporting a Vulnerability



Do not disclose a suspected vulnerability through a public issue.



After the GitHub repository is created, use GitHub's private vulnerability-reporting or Security Advisory feature. Include:



- A clear description

- Affected component

- Reproduction steps

- Potential impact

- Suggested mitigation, if known



Do not include real credentials, private source code, or personal information in the report.



## Supported Versions



Before the first public release, only the latest commit on the `main` branch is supported for security fixes.



## Automated Security Checks



The project uses:



- Bandit for Python source-code security scanning

- pip-audit for known dependency vulnerabilities

- Ruff for code-quality enforcement

- MyPy strict mode for type-safety checks

- Pytest for automated verification

- GitHub Actions for continuous checking



## Known Limitation



Container configuration has been created but has not yet been executed locally because Docker Desktop and WSL2 are not installed. The container must not be considered verified until build, runtime, health-check, permission, and isolation tests pass.
