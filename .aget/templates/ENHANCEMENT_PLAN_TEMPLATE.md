# Enhancement Plan: [Enhancement Name]

**Enhancement ID**: [#123 or Feature N]
**Created**: [YYYY-MM-DD]
**Owner**: [Agent name]
**Estimated Effort**: [X-Y hours]
**Status**: [Planning | In Progress | Complete]

---

## Part 1: Problem & Discovery

### Problem Statement

[What friction or waste does this address? Quantify with metrics.]

**Current State**:
- [Concrete waste measurement]
- [Pain point with frequency]
- [Impact scope - how many agents/users]

**Discovery Context**:
- Discovered during: [Project, session, or learning]
- Related learnings: [L### references]
- Evidence: [Observations, data, user reports]

---

## Part 2: Proposed Solution

### Solution Overview

[High-level approach - what you'll build/change]

### Technical Approach

[Specific implementation details]
- Files/directories affected
- New components to create
- Existing components to modify
- Integration points

### Benefits & Impact

**Quantified Improvements**:
- [Metric]: [Before] → [After] ([% improvement])
- [Metric]: [Before] → [After] ([% improvement])

**Fleet Impact**:
- Scope: [Universal (28/28) | Common (X/28) | Narrow (Y/28)]
- Agent types: [Which agents benefit]

**Adoption**:
- [How agents discover/use this]
- [Learning curve estimate]

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
| Rollback strategy documented (if irreversible)? | — | [ ] | See Rollback Strategy below |
| Closure checklist present? | L463 | [ ] | Retrospective sections planned |

Mark N/A with rationale when a check doesn't apply.

---

## Part 3: Execution Plan

### Gate Structure

**Gate 1: [Objective]** ([X hours])
**Spec Basis**: {Spec references — CAP-PP-013}
- [ ] [Action 1]
- [ ] [Action 2]
- [ ] [Validation step]
- **Decision Point**: [Question?] [GO/NOGO]

**Gate 2: [Objective]** ([Y hours])
**Spec Basis**: {Spec references — CAP-PP-013}
- [ ] [Action 1]
- [ ] [Action 2]
- [ ] [Validation step]
- **Decision Point**: [Question?] [GO/NOGO]

[Add more gates as needed - typically 2-4 gates for enhancements]

### Out of Scope (CAP-PP-016)

| Item | Tracking | Owner |
|------|----------|-------|
| {Deferred item} | {Issue #N or follow-on plan} | {agent-name} |

**Anti-orphaning commitment (L274)**: Every out-of-scope item MUST have a tracking artifact before closure.

### Risk Assessment

**High Risks**:
- [Risk]: [Mitigation strategy]

**Medium Risks**:
- [Risk]: [Mitigation strategy]

**Dependencies**:
- [Dependency]: [Status/plan]

### Rollback Strategy

**REQUIRED for plans with irreversible operations.** Mark N/A if all operations are easily reversible.

| Gate | Risk Level | Rollback Procedure | Verification |
|------|-----------|-------------------|--------------|
| Gate {N} | High/Med/Low | {How to undo if gate fails} | {Command to verify rollback succeeded} |

---

## Part 4: Success Criteria

### Acceptance Criteria

- [ ] [Specific testable outcome]
- [ ] [Specific testable outcome]
- [ ] [Specific testable outcome]

### Validation Plan

**Testing Approach**:
- [How to verify it works]
- [Test scenarios]
- [Pilot validation if applicable]

**Rollout Strategy**:
- [How to deploy to fleet]
- [Pilot agents if applicable]
- [Full rollout plan]

---

## Pre-Submission Verification (CAP-PP-014)

**REQUIRED before presenting plan to principal.** Verify every factual claim against ground truth (L558).

| Claim | Source | Verified | Method |
|-------|--------|----------|--------|
| {Factual claim from plan} | {Where claimed} | [ ] | {How verified} |

---

## Part 5: Post-Implementation

### Learning Capture

[Create L### document if this reveals generalizable patterns]

**Patterns Discovered**:
- [What worked well]
- [What didn't work]
- [Lessons for future enhancements]

### Follow-Up Enhancements

[Related enhancements identified during implementation]

---

**Template Version**: 1.1 (v3.6)
**Based on**: L221 (Planning Taxonomy), L274 (OKR-Driven), L275 (Multi-Gate)
**v1.1 additions**: Spec Basis per gate (CAP-PP-013), Pre-Submission Verification (CAP-PP-014), Out-of-Scope table (CAP-PP-016)
