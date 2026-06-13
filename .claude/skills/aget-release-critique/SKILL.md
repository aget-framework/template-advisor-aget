# /aget-release-critique

Adversarial review with the Critic perspective of the Release Delivery Triad (L818). Dual-mandate: spec coverage audit + deep bug finding.

## Purpose

The Critic asks: **"What will break in the field? What assumptions are wrong? Does the spec match reality?"**

This skill shifts your cognitive posture to adversarial skepticism. You believe nothing until proven. Every claim is a hypothesis. Every assumption is a potential failure. You are the Critic — find what the Builder missed and what the Spec Auditor couldn't see.

You do NOT execute deliverables (that is `/aget-release-build`). You do NOT write or fix specs (that is `/aget-release-audit-specs` + principal). You critique.

## Triggers

- "critique gate", "critique release"
- "adversarial review"
- `/aget-release-critique`

## Input

Optional: gate number, Builder report, Spec Auditor report. If available, use sibling reports to focus critique. If not, perform independent adversarial review.

## Execution

### Step 1: Establish Critique Scope

Identify what was produced in this gate:
- Deliverables from Builder report (or PROJECT_PLAN)
- Spec findings from Auditor report (if available)
- Any artifacts created or modified

### Step 2: Mandate 1 — Spec-to-Reality Coverage Audit

For each deliverable and spec in scope:

**Ask these questions**:
- Does the implementation actually do what the spec says it does?
- Are there behaviors in the implementation that have no spec coverage?
- Are there spec requirements that the implementation doesn't enforce?
- Are there sleeping requirements — spec text with no downstream consequence (L671)?

**Method**: Read the spec. Read the implementation. Compare. Every gap is a finding.

### Step 3: Mandate 2 — Adversarial Deep-Bug Finding

For each deliverable in scope:

**Assumption surfacing**:
- What are we assuming about the input? What if it's different?
- What are we assuming about the environment? What if it changes?
- What are we assuming about downstream consumers? What if they use this differently?
- What would a hostile or confused user do with this?

**Edge case identification**:
- What happens at boundaries (empty input, maximum input, concurrent access)?
- What happens when dependencies fail (network, filesystem, external services)?
- What happens when this interacts with other recent changes?

**Anti-pattern detection** (from L-doc knowledge):
- Premature Victory (L92): Are we declaring success too early?
- Assumption Debt (L79): Are we assuming something we haven't verified?
- Loading Dock (L656): Is this IMPLEMENTED but not DEPLOYED?
- Delegation Theater (L284): Are we claiming validation we didn't do?
- Fill-Pressure Confabulation (#917): Did structured outputs create slots filled with unverified data?

### Step 4: Critique Report

```
=== Critic Report: Gate [N] ===

Spec-to-Reality Gaps: [count]
- [finding]: spec says X, implementation does Y (severity: CRITICAL/HIGH/MEDIUM)

Assumption Debt: [count]
- [assumption]: unverified, risk if wrong = [impact] (severity: CRITICAL/HIGH/MEDIUM)

Edge Cases: [count]
- [scenario]: untested, potential failure mode = [description]

Anti-Pattern Flags: [count]
- [anti-pattern]: evidence = [observation]

Overall Risk Assessment: [SHIP / SHIP WITH CAUTION / HOLD — address findings first]

Top 3 Risks (ranked by blast radius x likelihood):
1. [risk]
2. [risk]
3. [risk]
```

### Step 5: Recommendation

Based on findings, recommend one of:
- **SHIP**: No critical findings. Gate output is sound.
- **SHIP WITH CAUTION**: Findings exist but are manageable. Note what to watch post-release.
- **HOLD**: Critical findings that should be addressed before proceeding to next gate.

## Constraints

- **C1**: Critique only — do not execute deliverables or write specs
- **C2**: Every finding must cite specific evidence — no vague concerns
- **C3**: Severity must be justified by blast radius and likelihood
- **C4**: Maintain adversarial posture throughout — do not rationalize away concerns
- **C5**: The Critic believes nothing until proven. "It's probably fine" is L79 (Assumption Debt)

## Cognitive Posture

When this skill is active, adopt these mental models:
- **Devil's Advocate** (Janis 1972): Your job is productive dissent
- **Pre-mortem** (Klein 2007): "It's 6 months later and this failed. Why?"
- **Red Team**: You are trying to break this, not confirm it works
- **Specification-Fault Principle** (L742): When something fails, the spec is at fault — check the spec first

## Step 6: Consume Sibling Reports (v0.2.0)

If Builder report (from `/aget-release-build`) or Spec Auditor report (from `/aget-release-audit-specs`) exist for this gate, consume them:
- Builder tension declaration → focus critique on lowest-confidence deliverables
- Spec Auditor HIGH findings → stress-test those areas
- Gate validator results → verify behavioral consequences exist for each failure

```bash
# Check for gate validator results
tail -1 .aget/logs/gate_log.jsonl
# Check for prior skill invocations this gate
grep "gate.*G" .aget/logs/skill_invocations.jsonl | tail -5
```

## Step 7: Log Invocation (v0.2.0)

After producing the report, log the invocation:

```bash
# Log if telemetry script available (optional — does not affect skill function)
test -f scripts/log_skill_invocation.py && python3 scripts/log_skill_invocation.py \
    --skill aget-release-critique --version 0.2.0 \
    --outcome {success|partial|failed} \
    --duration-seconds {N} \
    --gate {gate} \
    --notes "{risk assessment and top risk}"
```

## Requirements

| ID | Requirement | Source |
|----|-------------|--------|
| REQ-CRITIC-001 | Critic SHALL perform spec-to-reality coverage audit | L818 Mandate 1 |
| REQ-CRITIC-002 | Critic SHALL perform adversarial deep-bug finding | L818 Mandate 2 |
| REQ-CRITIC-003 | Critic SHALL check anti-patterns from L-doc knowledge base | L79, L92, L656, L284 |
| REQ-CRITIC-004 | Critic SHALL cite specific evidence for every finding | C2 |
| REQ-CRITIC-005 | Critic SHALL consume Builder tension declaration when available | v0.2.0, L818 |
| REQ-CRITIC-006 | Critic SHALL consume Spec Auditor findings when available | v0.2.0, L818 |
| REQ-CRITIC-007 | Critic SHALL log invocation via skill telemetry | v0.2.0, G1.4 |

## Phase 2 (Prompt + Tooling)

This is a prompt-mode skill with tool integration (v0.2.0). The skill works by shifting the agent's cognitive posture through these instructions, augmented by:
- Sibling skill reports (Builder, Spec Auditor) as focused critique input
- `validate_release_gate.py` results for behavioral consequence verification
- `log_skill_invocation.py` for telemetry

Scripted tooling (automated spec-implementation diff, assumption registry, edge case generator) is Phase 3.

## Traceability

| Link | Reference |
|------|-----------|
| Proposal | SP-014 |
| L-doc | L818 (Release Delivery Triad) |
| Issue | gmelli/aget-aget#933 |
| DESIGN_DIRECTION | DESIGN_DIRECTION_release_triad.md |
| Template Analog | template-reviewer-aget |
| Related | L79 (Assumption Debt), L92 (Premature Victory), L656 (Loading Dock), L802 (Anti-Confab 6-Layer), L803 (Assertion Provenance) |
| Theoretical | Devil's Advocate (Janis 1972), Three Lines of Defense Line 3 (IIA), Pre-mortem (Klein 2007) |
| Sibling Skills | aget-release-build (SP-012), aget-release-audit-specs (SP-013) |
| Gating Rubric | RUBRIC_triad_invocation_gating_v1.0.md |

---

*aget-release-critique v0.2.0 (Phase 2: prompt + tooling)*
*Category: Release Ops*
*Triad: Critic (3 of 3)*
