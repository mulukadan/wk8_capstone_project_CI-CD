# Changelog

All notable AfyaPlus AI deployment changes are recorded here.

---

## [1.2.0] - Current Stable

### Prompt

- Active triage prompt: `triage_system_v1.2.0.txt`
- Prompt SHA is pinned in `prompts/pin.json`

### Configuration

- Release version: `1.2.0`
- Prompt version: `1.2.0`
- MCP logistics version: `1.2.0`
- Model: `gpt-4o-mini`
- Temperature: `0`

### MCP

Required logistics tools:

- `check_stock`
- `plan_delivery_route`
- `get_delivery_eta`

### Evaluation

Golden-set regression threshold:

`0.85`

Current local result:

`1.00`

### Deployment

Docker image tag:

`afyaplus-week8:v1.2.0`

---

## [1.3.0-candidate] - Unreleased

### Prompt

Candidate prompt added:

`prompts/triage_system_v1.3.0-candidate.txt`

This prompt is not yet the active production prompt.

Before promotion it must pass:

1. prompt pin/version checks
2. pytest
3. golden-set evaluation
4. MCP health check
5. human review

### Release status

Not approved for production.