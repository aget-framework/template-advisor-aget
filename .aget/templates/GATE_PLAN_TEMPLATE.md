# Gate Plan: [Task Name]

**Created**: [YYYY-MM-DD]
**Owner**: [Agent name]
**Total Estimated Effort**: [X-Y hours]
**Status**: [Planning | Gate N In Progress | Complete]

---

## Planning Summary

### Task Overview

[What are you doing and why?]

### Scope Decision

[What's included and excluded in this plan]

**Included**:
- [Item 1]
- [Item 2]

**Out of Scope (CAP-PP-016):**

| Item | Tracking | Owner |
|------|----------|-------|
| {Excluded item 1} | {Issue #N or follow-on plan} | {agent-name} |

**Anti-orphaning commitment (L274)**: Every out-of-scope item MUST have a tracking artifact before plan closure.

### Gate Philosophy

**Why gates for this task?**:
- [Reason - e.g., irreversible operations, high risk, multi-step coordination]

**Gate sizing**: [Small (2-3) | Medium (4-6) | Large (7+)]
- Rationale: [Why this many gates]

---

## Gate Sequence

### Gate 0: Planning & Scope Decision ✅

**Objective**: Define scope and create gate structure

**Duration**: [X hours]

**Actions**:
- [X] Create this gate plan
- [X] Identify decision points
- [X] Size each gate

**Exit Criteria**: ✅ Scope locked, gates designed

---

### Gate 1: [Clear Objective]

**Objective**: [What this gate accomplishes - specific and measurable]
**Spec Basis**: {Spec references justifying this gate's deliverables — CAP-PP-013}

**Duration**: [X-Y hours]

**Actions**:
1. [ ] [Specific action with deliverable]
2. [ ] [Specific action with deliverable]
3. [ ] [Validation step]

**Validation Checklist**:
- [ ] [Specific verification item]
- [ ] [Specific verification item]
- [ ] [No regressions in existing functionality]

**Decision Point**: [Specific question needing answer] [GO/NOGO to Gate 2]

**Rationale**: [Why this gate comes first, what it enables]

---

### Gate 2: [Clear Objective]

**Objective**: [What this gate accomplishes]
**Spec Basis**: {Spec references — CAP-PP-013}

**Duration**: [X-Y hours]

**Blocking**: Gate 1 complete

**Actions**:
1. [ ] [Specific action with deliverable]
2. [ ] [Specific action with deliverable]
3. [ ] [Validation step]

**Validation Checklist**:
- [ ] [Specific verification item]
- [ ] [Specific verification item]

**Decision Point**: [Specific question] [GO/NOGO to Gate 3]

**Rationale**: [Why this gate sequencing]

---

### Gate 3: [Clear Objective]

[Repeat structure for each gate]

---

### Gate N: Validation & Completion

**Objective**: Verify complete system works and close out
**Spec Basis**: {Spec references — CAP-PP-013}

**Duration**: [X hours]

**Actions**:
1. [ ] End-to-end validation
2. [ ] Documentation update
3. [ ] Learning capture (if applicable)
4. [ ] Announce completion

**Validation Checklist**:
- [ ] All previous gate deliverables integrated
- [ ] No regressions
- [ ] Success criteria met

**Decision Point**: Task complete? [COMPLETE]

---

## Gate Execution Discipline (L42)

**Execute ONLY current gate** - Don't slip into next gate work
**Stop at gate boundary** - Even if "just one more thing" seems logical
**Run validation checks** - Every gate has explicit validation
**WAIT for explicit GO** - Don't assume continuation

**Red flag**: "While we're at it, let's also..." = likely next gate work

---

## Process Compliance Checklist (L551)

Verify this plan's gate structure against mandatory framework patterns:

| Check | Pattern | Verified | Notes |
|-------|---------|----------|-------|
| Spec precedes implementation? | L533 | [ ] | Which gate creates spec? Which implements? |
| Gate ordering follows Spec→Validate→Implement→Verify? | L546 | [ ] | No combined spec+implement deliverables |
| Propagation gate included (if fleet-wide)? | L541/L328 | [ ] | How do changes reach other agents/templates? |
| Cross-portfolio security assessed (if multi-agent)? | L155 | [ ] | Sensitivity review for cross-classification work |
| V-tests defined per gate? | L370 | [ ] | Specific commands, expected output, BLOCKER flags |
| Fleet agent coordination formalized (if cross-agent)? | L100 | [ ] | Checkpoint file, not conversational |
| Rollback strategy documented (if irreversible)? | — | [ ] | See Rollback Strategy section below |
| Closure checklist present? | L463 | [ ] | Retrospective sections planned |

Mark N/A with rationale when a check doesn't apply.

---

## Risk Assessment

### High Risks

**Risk**: [Description]
- **Impact**: [What happens if this occurs]
- **Mitigation**: [How to prevent/handle]
- **Contingency**: [Rollback plan if needed]

### Medium Risks

[Same structure]

### Dependencies

**External**: [Dependencies outside your control]
**Internal**: [Dependencies within your control]

### Rollback Strategy

**REQUIRED for plans with irreversible operations.** Mark N/A if all operations are easily reversible.

| Gate | Risk Level | Rollback Procedure | Verification |
|------|-----------|-------------------|--------------|
| Gate {N} | High/Med/Low | {How to undo if gate fails} | {Command to verify rollback succeeded} |

---

## Success Criteria

### Overall Objectives

- [ ] [Specific measurable outcome]
- [ ] [Specific measurable outcome]
- [ ] [Specific measurable outcome]

### Quality Bar

**Target**: [What "done well" looks like]
**Minimum**: [What "acceptable" looks like]

---

## Integration Points

**With other work**: [How this relates to parallel or dependent work]
**With existing systems**: [What existing functionality must continue working]

---

## Pre-Submission Verification (CAP-PP-014)

**REQUIRED before presenting plan to principal.** Verify every factual claim against ground truth. Template compliance ≠ factual accuracy (L558).

| Claim | Source | Verified | Method |
|-------|--------|----------|--------|
| {Factual claim from plan} | {Where claimed} | [ ] | {How verified} |

---

## Post-Completion

### Learning Capture

[If this reveals patterns, create L### document]

### Follow-Up Work

[Enhancements or tasks deferred for later]

---

**Template Version**: 1.1 (v3.6)
**Based on**: L42 (Gate Discipline), L275 (Multi-Gate Execution), L104 (Gate Sizing)
**v1.1 additions**: Spec Basis per gate (CAP-PP-013), Pre-Submission Verification (CAP-PP-014), Out-of-Scope table (CAP-PP-016)
