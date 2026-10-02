# EvoForge AI - Development Roadmap



## Phase 0 - Research and Project Charter



Status: Completed



- Define the problem, users, scope, and exclusions

- Study existing automated program-repair systems

- Define research questions and hypotheses

- Select datasets and evaluation metrics

- Establish security, ethics, and safety boundaries

- Freeze the project charter and phased roadmap



## Phase 1 - Professional Project Foundation



Status: In progress



- Configure the repository and Python environment

- Establish professional directory structure

- Configure reproducible dependencies

- Create the FastAPI backend foundation

- Configure tests, linting, typing, and coverage

- Protect secrets and validate settings

- Add Docker and GitHub Actions configurations

- Create continuity documentation

- Create the first Git commit and GitHub repository



## Phase 2 - Repository Ingestion



Status: Planned



- Accept controlled Python repositories

- Validate repository paths and formats

- Inspect files, packages, dependencies, and tests

- Generate repository metadata

- Reject unsupported or unsafe inputs



## Phase 3 - Isolated Failure Reproduction



Status: Planned



- Build restricted execution sandboxes

- Apply CPU, memory, process, time, and storage limits

- Disable network access by default

- Reproduce failing tests and commands

- Capture structured execution evidence



## Phase 4 - Static Program Analysis



Status: Planned



- Parse Python abstract syntax trees

- Extract functions, classes, imports, and symbols

- Build dependency and call graphs

- Identify changed and failure-relevant code regions

- Produce explainable static-analysis evidence



## Phase 5 - Dynamic Analysis and Test Intelligence



Status: Planned



- Capture stack traces and failure context

- Measure test coverage

- Trace execution paths

- Identify suspicious runtime behavior

- Select relevant tests for targeted verification



## Phase 6 - AI-Assisted Fault Localization



Status: Planned



- Combine static and dynamic evidence

- Rank suspicious files and code locations

- Provide explanations for localization decisions

- Measure Top-1, Top-3, and Top-5 localization accuracy

- Abstain when localization evidence is weak



## Phase 7 - Retrieval-Augmented Repair Knowledge



Status: Planned



- Index repository documentation and code context

- Retrieve relevant functions, tests, and historical patterns

- Build grounded repair prompts

- Track evidence provenance

- Prevent unsupported context generation



## Phase 8 - Candidate Patch Generation



Status: Planned



- Generate a maximum of three patch candidates

- Enforce minimal and localized changes

- Reject malformed or unsafe patches

- Record model, prompt, evidence, and generation metadata

- Support multiple AI providers without provider lock-in



## Phase 9 - Patch Verification



Status: Planned



- Apply patches in disposable workspaces

- Run targeted tests

- Run regression tests

- Run static-analysis and security checks

- Capture reproducible verification evidence



## Phase 10 - Evidence-Based Ranking and Abstention



Status: Planned



- Rank candidates using correctness, regression, risk, and scope

- Calibrate confidence scores

- Explain ranking decisions

- Detect conflicting evidence

- Abstain instead of recommending unsafe repairs



## Phase 11 - Human Approval and Auditability



Status: Planned



- Present diffs and supporting evidence

- Require explicit human approval

- Record approvals and rejections

- Maintain immutable audit records

- Prevent silent repository modification



## Phase 12 - Workflow Orchestration and Persistence



Status: Planned



- Create end-to-end repair workflows

- Persist repositories, runs, evidence, candidates, and decisions

- Support resumable jobs

- Add failure recovery and idempotency

- Expose stable backend APIs



## Phase 13 - Professional Frontend Dashboard



Status: Planned



- Build repository and issue submission

- Display analysis progress and evidence

- Visualize fault-localization results

- Compare candidate patches

- Provide approval, rejection, and audit interfaces



## Phase 14 - Benchmark Evaluation and Hardening



Status: Planned



- Evaluate controlled bug cases

- Evaluate QuixBugs and BugsInPy

- Evaluate an appropriate SWE-bench subset

- Compare against defined baselines

- Measure correctness, safety, latency, cost, and abstention

- Perform security and adversarial testing



## Phase 15 - Deployment, Documentation and Portfolio Release



Status: Planned



- Complete Docker deployment

- Finalize CI/CD

- Publish architecture and evaluation reports

- Record a professional demonstration

- Create resume and LinkedIn descriptions

- Prepare interview explanations

- Publish a reproducible portfolio release



## Completion Standard



A phase is complete only when its implementation, tests, security checks, documentation, and measurable verification evidence are complete. A dashboard or generated output alone does not qualify as a completed capability.
