# AfyaPlus LLMOps Runbook

## Purpose

This runbook explains how AfyaPlus prompt, configuration, MCP, and deployment changes are tested, approved, deployed, monitored, and rolled back.

It is intended to help an engineer or reviewer safely operate the system, including during an incident.

---

## Current Stable Release

- Release version: `1.2.0`
- Prompt version: `1.2.0`
- MCP version: `1.2.0`
- Model: `gpt-4o-mini`
- Docker image: `afyaplus-week8:v1.2.0`
- Golden-set regression threshold: `0.85`

The current prompt SHA is stored in:

`prompts/pin.json`

Runtime version information is available from:

`GET /health`

---

## Release Flow

All AI-related changes should follow this sequence:

1. Developer creates or edits a prompt, config, MCP tool, or application code.
2. The change is submitted through a pull request.
3. Required reviewers review the change.
4. CI runs automated tests.
5. The golden-set evaluation runs.
6. MCP health is checked.
7. Docker image is built.
8. Deployment proceeds only if all gates pass.
9. The release is monitored after deployment.

The intended CI sequence is:

`lint_test -> eval -> mcp_health -> build_deploy`

A failure in any earlier stage blocks later stages.

---

## Prompt Change Procedure

When changing the triage prompt:

1. Create a new versioned prompt file.

Example:

`triage_system_v1.3.0-candidate.txt`

2. Review the prompt with clinical_ops and ml-eng.

3. Update the active prompt only when the candidate is approved.

4. Update:

- `prompts/pin.json`
- `config/triage.yaml`
- `CHANGELOG.md`

5. Regenerate the prompt SHA:

```bash
python scripts/update_prompt_pin.py
```

6. Verify the prompt pin:

```bash
python check_prompt_pin.py
```

7. Run tests:

```bash
pytest -v
```

8. Run the golden-set evaluation:

```bash
python eval_prompts.py
```

9. Run MCP health:

```bash
python scripts/check_mcp_health.py
```

10. Open a pull request and wait for review and CI.

---

## Evaluation Gate

The evaluation dataset is:

`evals/golden.jsonl`

The current metric is:

**Urgency agreement**

The threshold is:

`0.85`

A score below `0.85` fails the evaluation job.

A failing evaluation exits with:

`exit code 1`

This prevents downstream deployment.

Do not lower the threshold simply to make the pipeline pass.

If the evaluation fails:

1. Review failed golden cases.
2. Identify whether the cause is prompt, model configuration, or application logic.
3. Fix the regression.
4. Re-run the evaluation.
5. Do not deploy until the gate passes.

---

## MCP Health Gate

The required MCP tools are:

- `check_stock`
- `plan_delivery_route`
- `get_delivery_eta`

The health check is:

```bash
python scripts/check_mcp_health.py
```

The check verifies:

- MCP server version
- required tool availability

If a required tool is missing, the script exits with code `1`.

Deployment must not continue when MCP health fails.

---

## Prompt Integrity Check

The active prompt is protected using a SHA-256 fingerprint.

The expected SHA is stored in:

`prompts/pin.json`

The actual SHA is recalculated from the prompt file.

The check runs:

```bash
python check_prompt_pin.py
```

If expected and actual SHA values differ, CI fails.

This prevents an unpinned prompt change from being deployed.

---

## Roll Forward

A new release may proceed when:

- prompt/config/MCP versions are aligned
- prompt SHA matches
- pytest passes
- golden-set evaluation is at least `0.85`
- MCP health passes
- required reviewers approve the change
- CHANGELOG is updated

After approval:

1. merge the pull request
2. build the release image
3. create the release tag
4. verify `/health`
5. monitor errors and evaluation results

---

## Rollback Procedure

If a deployment causes unacceptable behaviour:

### 1. Identify the last known good release

Current example:

`v1.2.0`

### 2. Restore the previous prompt version

Set:

`PROMPT_VERSION=1.2.0`

or restore:

`prompts/triage_system_v1.2.0.txt`

### 3. Restore configuration

Ensure:

- release version = `1.2.0`
- prompt version = `1.2.0`
- MCP version = `1.2.0`

### 4. Verify prompt SHA

Run:

```bash
python check_prompt_pin.py
```

### 5. Run safety gates

```bash
pytest -v
python eval_prompts.py
python scripts/check_mcp_health.py
```

### 6. Redeploy the last known good image

Example:

```bash
docker run --rm -p 8000:8000 afyaplus-week8:v1.2.0
```

### 7. Verify runtime state

Check:

`GET /health`

Confirm:

- correct release version
- correct prompt version
- correct MCP version
- `prompt_sha_match = true`

---

## Where to Investigate Failures

### Prompt/version failures

Check:

- `prompts/pin.json`
- `config/triage.yaml`
- `check_prompt_pin.py`
- `/health`

### Eval failures

Check:

- `evals/golden.jsonl`
- `eval_prompts.py`
- CI job: `Golden Set Eval`

### MCP failures

Check:

- `logistics_mcp_versioned.py`
- `scripts/check_mcp_health.py`
- CI job: `MCP Health`

### Build failures

Check:

- `Dockerfile`
- `requirements.txt`
- CI job: `Build and Deploy Stub`

---

## Human Review

Clinical-adjacent prompt changes must not be approved only by automation.

Required review should include:

- clinical_ops for clinical meaning and safety
- ml-eng for model/prompt behaviour
- platform engineering for deployment/MCP changes where relevant

Automation recommends whether a change is safe enough to progress.

Humans remain responsible for the final production decision.

---

## Recommend vs Decide Governance

The AfyaPlus AI system is designed to recommend, assist, and classify.

It must not independently make high-impact clinical decisions.

Examples of acceptable assistance:

- triage urgency suggestion
- logistics stock lookup
- routing support
- summarisation

Examples requiring human responsibility:

- final diagnosis
- treatment decision
- emergency clinical judgement
- policy override

The AI system informs decisions; qualified humans remain accountable for final clinical actions.

---

# Sprint Definition of Done

A prompt or MCP pull request is complete only when all applicable items below are satisfied.

## Versioning

- [ ] Prompt has an explicit version.
- [ ] Config version is updated.
- [ ] MCP version is updated when required.
- [ ] Release versions are aligned.
- [ ] Prompt SHA is regenerated.
- [ ] CHANGELOG is updated.

## Testing

- [ ] `pytest -v` passes.
- [ ] Prompt pin check passes.
- [ ] Golden-set evaluation passes.
- [ ] Evaluation score is at least `0.85`.
- [ ] MCP health check passes.

## Review

- [ ] Clinical-adjacent prompt changes reviewed by clinical_ops.
- [ ] ML behaviour reviewed by ml-eng.
- [ ] Platform-related changes reviewed where required.

## Deployment

- [ ] GitHub Actions pipeline is green.
- [ ] Docker image builds successfully.
- [ ] Image/release tag is recorded.
- [ ] `/health` reports the expected versions.
- [ ] Prompt SHA matches at runtime.

## Governance

- [ ] Rollback path is known.
- [ ] No secrets are committed.
- [ ] AI remains recommend-not-decide.
- [ ] Any fallback used is documented.

A change is not Done if any mandatory gate is bypassed.