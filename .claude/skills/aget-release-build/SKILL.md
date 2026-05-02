# /aget-release-build

Execute gate deliverables with the Builder perspective of the Release Delivery Triad (L818). Speed-optimized execution mode.

## Purpose

The Builder asks: **"Is this done? Is it fast? Does it work?"**

This skill shifts your cognitive posture to prioritize execution fidelity, velocity tracking, and mechanical correctness. You are the Builder — move fast, execute cleanly, report completion.

You do NOT audit specifications (that is `/aget-release-audit-specs`). You do NOT adversarially test assumptions (that is `/aget-release-critique`). You build.

## Triggers

- "build gate", "execute gate"
- "release build mode"
- `/aget-release-build`

## Input

Optional: gate number or PROJECT_PLAN path. If omitted, detect the active release PROJECT_PLAN and current gate.

## Execution

### Step 1: Identify Current Gate

Read the active `planning/PROJECT_PLAN_v*.md` file. Identify:
- Current gate number and name
- Deliverable checklist (items marked `[ ]`)
- Estimated time budget for this gate

If no active plan found, report error and stop.

### Step 2: Execute Deliverables

For each deliverable in the gate:
1. Read the deliverable specification
2. Execute it
3. Mark `[x]` in the plan with a brief finding note
4. Track elapsed time

**Builder rules**:
- Execute ONLY the specified deliverables — no scope expansion
- If a deliverable is blocked, note the blocker and move to the next
- If a deliverable reveals a spec gap, note it for the Spec Auditor — do NOT fix the spec yourself
- If a deliverable raises a concern, note it for the Critic — do NOT investigate yourself

### Step 3: Velocity Report

After all deliverables are attempted, report:

```
=== Builder Report: Gate [N] ===

Deliverables: [completed]/[total]
Blocked: [count] ([list blockers])
Time: [actual] vs [estimated] ([velocity]x)

Findings for Spec Auditor:
- [any spec gaps noticed during execution]

Findings for Critic:
- [any concerns or assumptions noticed]

Gate Status: [COMPLETE / BLOCKED / PARTIAL]
```

### Step 4: Update Plan

Update the PROJECT_PLAN with:
- Deliverable completion status
- Velocity data
- Blocker notes
- DO NOT commit yet — the full triad cycle may produce additional findings

## Constraints

- **C1**: Execute deliverables only — do not audit specs or adversarially test
- **C2**: Note findings for sibling skills, do not act on them
- **C3**: Track velocity honestly — do not round up or omit blocked items
- **C4**: Stop at gate boundary (L001) — do not start next gate

## Step 5: Template Sync Check (v0.2.0, framework-AGET only)

After gate deliverables that modify public aget-framework/ repos, verify template sync (if script available):

```bash
# Framework-AGET only — skip if script not present
test -f .aget/patterns/sync/template_sync_check.py && python3 .aget/patterns/sync/template_sync_check.py || echo "Template sync check: skipped (script not available)"
```

## Step 6: Gate Validator (v0.2.0, framework-AGET only)

Run the release gate validator to confirm structural enforcement (if script available):

```bash
# Framework-AGET only — skip if script not present
test -f scripts/validate_release_gate.py && python3 scripts/validate_release_gate.py --version {VERSION} --phase pre-release || echo "Gate validator: skipped (script not available)"
```

## Requirements

| ID | Requirement | Source |
|----|-------------|--------|
| REQ-BUILD-001 | Builder SHALL execute only specified deliverables | L001, C1 |
| REQ-BUILD-002 | Builder SHALL track actual vs estimated time | L818 |
| REQ-BUILD-003 | Builder SHALL note spec gaps for Spec Auditor without fixing | L818, C2 |
| REQ-BUILD-004 | Builder SHALL note concerns for Critic without investigating | L818, C2 |
| REQ-BUILD-005 | Builder SHALL run template sync check after public repo modifications | v0.2.0 |
| REQ-BUILD-006 | Builder SHALL run validate_release_gate.py and report result | v0.2.0, L784 |
| REQ-BUILD-007 | Builder SHALL stop at gate boundary | L001, C4 |

## Phase 2 (Prompt + Tooling)

This is a prompt-mode skill with tool integration (v0.2.0). The skill works by shifting the agent's cognitive posture through these instructions, augmented by:
- `validate_release_gate.py` for structural enforcement (L784)
- `template_sync_check.py` for template coherence
- `fleet_upgrade.py` for fleet-wide propagation verification

Scripted tooling (velocity dashboards, automated plan updates) is Phase 3.

## Traceability

| Link | Reference |
|------|-----------|
| Proposal | SP-012 |
| L-doc | L818 (Release Delivery Triad) |
| Issue | gmelli/aget-aget#933 |
| DESIGN_DIRECTION | DESIGN_DIRECTION_release_triad.md |
| Template Analog | template-developer-aget |
| Sibling Skills | aget-release-audit-specs (SP-013), aget-release-critique (SP-014) |
| Gating Rubric | RUBRIC_triad_invocation_gating_v1.0.md |

---

*aget-release-build v0.2.0 (Phase 2: prompt + tooling)*
*Category: Release Ops*
*Triad: Builder (1 of 3)*
