# Week 8 — CI/CD for Versioned AI + MCP Health

## Overview

This project extends the AfyaPlus work from Weeks 6 and 7 with a controlled CI/CD process for AI application changes.

The pipeline versions the triage prompt, application configuration, and logistics MCP integration, then applies automated gates before allowing a Docker build/deployment step.

The pipeline sequence is:

`lint_test -> eval -> mcp_health -> build_deploy`

A failure in an earlier stage prevents later deployment stages from running.

The project demonstrates:

- versioned AI prompts
- prompt SHA integrity checks
- aligned release/config/MCP versions
- automated tests
- golden-set regression evaluation
- MCP health checks
- Docker image creation
- rollback procedures
- human review and governance controls

---

# Versions

## Current Stable Release

Release version:

`1.2.0`

Prompt version:

`1.2.0`

Prompt file:

`prompts/triage_system_v1.2.0.txt`

MCP version:

`1.2.0`

Model:

`gpt-4o-mini`

Docker release image:

`afyaplus-week8:v1.2.0`

Git release tag:

`v1.2.0`

---

## Candidate Prompt

Candidate version:

`1.3.0-candidate`

File:

`prompts/triage_system_v1.3.0-candidate.txt`

The candidate does not replace the stable prompt until all automated gates and required human reviews pass.

---

# Prompt Version and Integrity

The active prompt is selected through:

`prompts/pin.json`

The pin contains:

- prompt version
- prompt filename
- SHA-256 fingerprint

The prompt SHA is generated using:

```bash
python scripts/update_prompt_pin.py
```

It is verified using:

```bash
python check_prompt_pin.py
```

Line endings are normalized before hashing so the same prompt produces the same fingerprint on Windows and Linux/GitHub Actions.

The API `/health` endpoint reports:

- release version
- model
- prompt version
- prompt file
- expected prompt SHA
- actual prompt SHA
- SHA match status
- MCP version

Example:

```json
{
  "status": "ok",
  "service": "afyaplus-triage",
  "release_version": "1.2.0",
  "model": "gpt-4o-mini",
  "prompt_version": "1.2.0",
  "prompt_sha_match": true,
  "mcp_version": "1.2.0"
}
```

---

# Configuration

Main configuration:

`config/triage.yaml`

It records:

- service name
- release version
- model
- temperature
- maximum tokens
- prompt version
- MCP version
- allowed urgency classes

The automated tests verify that:

`release version = prompt version = MCP version`

for the current stable release.

---

# GitHub Actions Pipeline

Workflow:

`.github/workflows/ci.yml`

The workflow runs on:

- pull requests
- pushes to `main`
- manual `workflow_dispatch`

The workflow contains four gated jobs.

## 1. Lint and Test

Runs:

- dependency installation
- Python syntax check
- prompt pin validation
- pytest

Local equivalent:

```bash
python check_prompt_pin.py
pytest -v
```

Current local test result:

`3 passed`

---

## 2. Golden Set Eval

Runs:

```bash
python eval_prompts.py
```

The fixture set is:

`evals/golden.jsonl`

Metric:

**Urgency agreement**

Threshold:

`0.85`

Healthy result:

```text
Correct: 10/10
Eval score: 1.00
Required threshold: 0.85

REGRESSION GATE: PASSED
```

A score below the threshold returns exit code `1` and prevents downstream jobs from running.

---

## Regression Failure Evidence

A deliberate regression was introduced during testing.

Result:

```text
Correct: 7/10
Eval score: 0.70
Required threshold: 0.85

REGRESSION GATE: FAILED
Deployment must not continue.
```

Process exit code:

`1`

This demonstrates that the regression gate fails closed rather than always returning success.

The correct implementation was restored after the test.

---

# MCP Health

Health script:

`scripts/check_mcp_health.py`

MCP implementation:

`logistics_mcp_versioned.py`

Required tools:

- `check_stock`
- `plan_delivery_route`
- `get_delivery_eta`

Run locally:

```bash
python scripts/check_mcp_health.py
```

Healthy result:

```text
MCP HEALTH: PASSED
All required tools are available.
```

A missing tool produces:

`exit code 1`

and deployment is not allowed to continue.

The MCP version expected by the current release is:

`1.2.0`

---

# Build and Deploy

The final pipeline job builds the Docker image only after all previous gates pass.

Local release build:

```bash
docker build -t afyaplus-week8:v1.2.0 .
```

The local Docker build completed successfully.

The GitHub Actions workflow also builds an image associated with the source commit.

The current capstone uses a deployment stub rather than a paid cloud deployment.

---

# CI Dependency Chain

The workflow is intentionally ordered:

```text
Lint + Tests
     |
     v
Golden Set Eval
     |
     v
MCP Health
     |
     v
Docker Build / Deploy Stub
```

If evaluation fails:

```text
Lint + Tests      PASS
Eval              FAIL
MCP Health        SKIPPED
Build / Deploy    SKIPPED
```

If MCP health fails:

```text
Lint + Tests      PASS
Eval              PASS
MCP Health        FAIL
Build / Deploy    SKIPPED
```

This ensures deployment fails closed.

---

# CODEOWNERS and Review

Review policy is documented in:

`.github/CODEOWNERS`

Clinical-adjacent prompt changes require clinical review.

The intended review responsibilities are:

- `clinical_ops` — clinical meaning and safety
- `ml-eng` — prompt/model behaviour
- `platform` — MCP and deployment concerns

Automated checks provide evidence but do not replace human approval for clinical-adjacent changes.

---

# LLMOps Runbook

Operational procedures are documented in:

`runbook.md`

The runbook includes:

- release procedure
- prompt change procedure
- evaluation failure response
- MCP failure response
- prompt integrity checks
- roll forward
- rollback
- human review
- Definition of Done
- recommend-vs-decide governance

---

# clinical_ops Change-Control Brief

Non-technical change communication is documented in:

`clinical_ops_change_brief.md`

The brief explains:

- what changed
- what was tested
- evaluation results
- MCP health requirements
- rollback
- risks and mitigations
- required approval
- go/no-go conditions

---

# Rollback

The current last known good release is:

`v1.2.0`

Rollback includes:

1. restore prompt `1.2.0`
2. restore aligned configuration
3. verify prompt SHA
4. run pytest
5. run golden-set evaluation
6. run MCP health
7. redeploy the stable Docker image
8. verify `/health`

Example stable image:

```bash
docker run --rm -p 8000:8000 afyaplus-week8:v1.2.0
```

---

# Sprint Definition of Done

The complete Definition of Done is maintained in:

`runbook.md`

A prompt or MCP change is not complete unless:

- versions are aligned
- prompt SHA is valid
- tests pass
- eval score meets threshold
- MCP health passes
- CI is green
- required human review is complete
- rollback is known
- no secrets are committed

---

# Weeks 6 and 7 Reuse

## Week 6

The project reuses concepts and artefacts from the AfyaPlus FastAPI and MCP work, including:

- FastAPI service structure
- `/health` endpoint
- triage urgency schema
- logistics MCP tools
- local fixture data
- recommend-not-decide governance

## Week 7

The project builds on deployment and operational practices from Week 7, including:

- Docker image creation
- reproducible application configuration
- cost-aware deployment thinking
- local stub/model fallback strategy
- keeping secrets out of Git
- measurement-first operational evidence

Week 8 adds versioning and CI/CD controls around these existing artefacts.

---

# Fallbacks Declared

## Paid OpenAI Calls

Fallback used:

**Deterministic local evaluation stub**

The golden-set CI evaluation does not require paid OpenAI calls.

It preserves the same urgency schema:

- routine
- urgent
- emergency

The gate still genuinely fails when agreement drops below the threshold.

---

## GPU / Retraining

Fallback used:

**No GPU retraining**

No model weights are trained in this capstone.

Prompt/config/version changes are evaluated through the CI pipeline.

If retraining were required, a stub retrain stage could version the model configuration and record the change without claiming that weights were trained.

---

## Cloud Deployment

Fallback used:

**Docker build + deploy stub**

No paid Azure or Kubernetes deployment is required.

The final pipeline stage demonstrates that an approved image can be produced only after all gates succeed.

---

## MCP Availability

A local versioned logistics MCP implementation is used.

The health gate verifies the expected MCP version and required tool list using the same pass/fail exit-code contract that CI uses.

---

# Reproducing the Checks

Run from the project root.

## Prompt integrity

```bash
python check_prompt_pin.py
```

## Unit tests

```bash
pytest -v
```

## Evaluation

```bash
python eval_prompts.py
```

## MCP health

```bash
python scripts/check_mcp_health.py
```

## Docker build

```bash
docker build -t afyaplus-week8:v1.2.0 .
```

## Run the API

```bash
uvicorn prompt_app:app --reload
```

## Health endpoint

```bash
curl http://127.0.0.1:8000/health
```

---

# Evidence

Submission evidence should include:

- successful GitHub Actions workflow
- prompt pin check pass
- pytest pass
- golden-set evaluation pass
- deliberate regression failure
- regression exit code `1`
- MCP health pass
- deliberate MCP health failure
- MCP failure exit code `1`
- successful Docker build
- `/health` version/SHA response
- Git tag `v1.2.0`

---

# Repository Structure

```text
wk8_capstone_project/
|
|-- .github/
|   |-- CODEOWNERS
|   `-- workflows/
|       `-- ci.yml
|
|-- config/
|   `-- triage.yaml
|
|-- evals/
|   `-- golden.jsonl
|
|-- fixtures/
|   `-- responses/
|
|-- prompts/
|   |-- triage_system_v1.2.0.txt
|   |-- triage_system_v1.3.0-candidate.txt
|   `-- pin.json
|
|-- scripts/
|   |-- check_mcp_health.py
|   `-- update_prompt_pin.py
|
|-- tests/
|   `-- test_prompt_loader.py
|
|-- CHANGELOG.md
|-- Dockerfile
|-- README.md
|-- check_prompt_pin.py
|-- clinical_ops_change_brief.md
|-- clinics.json
|-- eval_prompts.py
|-- logistics_mcp_versioned.py
|-- prompt_app.py
|-- requirements.txt
`-- runbook.md
```

---

# Submission Checklist

- [x] Versioned stable prompt
- [x] Candidate prompt
- [x] Prompt SHA pinning
- [x] Runtime SHA evidence
- [x] Versioned configuration
- [x] Versioned MCP
- [x] Release alignment tests
- [x] GitHub Actions workflow
- [x] Pull request/main triggers
- [x] Automated tests
- [x] Golden-set evaluation
- [x] Regression threshold documented
- [x] Deliberate failing evaluation demonstrated
- [x] MCP health gate
- [x] MCP pass demonstrated
- [x] MCP failure path implemented
- [x] Docker build
- [x] Successful GitHub Actions workflow
- [x] LLMOps runbook
- [x] Sprint Definition of Done
- [x] clinical_ops change-control brief
- [x] Recommend-vs-decide governance
- [x] Fallbacks declared
- [x] Weeks 6 and 7 reuse documented
- [x] Secrets excluded from Git

---

# Conclusion

AfyaPlus Week 8 demonstrates a controlled LLMOps release process rather than direct AI changes to production.

Prompts, configuration, MCP integration, tests, evaluation, health checks, Docker builds, review requirements, and rollback instructions are all tied into a reproducible release process.

The main safety principle is:

**A change is not deployable merely because the code runs. It must also pass evaluation, integration health checks, version controls, and required human review.**