# Change-Control Brief — clinical_ops

## Proposed Change

The AfyaPlus triage prompt has a candidate update:

`1.2.0 -> 1.3.0-candidate`

The current stable release remains:

`1.2.0`

The candidate prompt adds clearer safety instructions and more explicit handling of severe warning signs.

It has not yet replaced the stable prompt.

---

## What Was Tested

The candidate change must pass the same automated controls used for AfyaPlus releases.

### Prompt integrity

The prompt is versioned and protected using a SHA-256 fingerprint.

A changed prompt cannot pass CI unless its pinned version and SHA are updated intentionally.

### Automated evaluation

The fixed test set is located at:

`evals/golden.jsonl`

The primary metric is:

**Urgency agreement**

Required score:

`0.85 or higher`

The current good-path evaluation produced:

`1.00`

A deliberate regression demonstration produced:

`0.70`

and correctly blocked the pipeline.

### MCP health

The logistics MCP health gate verifies that the following tools remain available:

- `check_stock`
- `plan_delivery_route`
- `get_delivery_eta`

A missing required tool causes the pipeline to fail.

---

## Deployment Controls

The CI/CD pipeline runs these stages in order:

1. lint and automated tests
2. golden-set evaluation
3. MCP health
4. Docker build and deploy stub

If evaluation or MCP health fails, deployment does not proceed.

---

## Rollback

If the candidate prompt causes unacceptable behaviour after release:

1. return the active prompt to `1.2.0`
2. restore the corresponding configuration
3. use the last known good release tag `v1.2.0`
4. rerun the automated safety gates
5. redeploy the stable image

The rollback does not require retraining model weights.

---

## Risk

The main risk is that a prompt change could alter urgency classifications or produce unsafe advice.

## Mitigation

The change is controlled using:

- versioned prompts
- fixed golden-set evaluation
- regression threshold
- prompt SHA validation
- clinical review
- MCP health checks
- rollback to the last known good release

---

## Approval

Required reviewers:

- clinical_ops
- ml-eng
- platform engineering where MCP/deployment changes are involved

Automation provides evidence, but does not replace human approval for clinical-adjacent changes.

---

## Go / No-Go Recommendation

**GO** only when:

- prompt pin check passes
- automated tests pass
- evaluation score is at least `0.85`
- MCP health passes
- required reviewers approve the change

**NO-GO** if any mandatory gate fails.

The stable `1.2.0` release should remain active until all conditions are satisfied.