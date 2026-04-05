# {RUBRIC_NAME} Scoring Rubric

**Version**: 1.0
**Created**: YYYY-MM-DD
**Author**: {agent-name}
**Domain**: {what this rubric evaluates}
**Archetype**: {Compliance | Decision | Meta}
**Assessor**: {Human | Agent | Hybrid}
**Status**: Draft | Active | Deprecated

## Purpose

{Why this rubric exists. What decisions does it support? What subjects does it evaluate?}

## Scope

| In Scope | Out of Scope |
|----------|--------------|
| {what is evaluated} | {what is NOT evaluated} |

## Theoretical Basis

{Reference to established frameworks. Cite ONTOLOGY_scoring_rubric_v1.0.yaml concepts.}

| Framework | Application |
|-----------|-------------|
| {e.g., Dawson 2017} | {how it informs this rubric} |

---

## Rubric Archetype Selection

Select the archetype that matches this rubric's purpose. Each archetype has a distinct evaluation flow.

| Archetype | Pattern | Flow | When to Use |
|-----------|---------|------|-------------|
| **Compliance** | Gate-before-pass | Eligibility gates → threshold check → PASS/FAIL | Evaluating whether an artifact meets a specification |
| **Decision** | Score-before-act | Dimension scoring → weighted composite → verdict bands → action | Supporting a decision (send/revise/reject) based on multi-dimensional quality |
| **Meta** | Assess-the-assessor | Evidence gathering → assessment quality scoring → calibration check | Evaluating the quality of an evaluation process itself |

**This rubric uses**: {Compliance | Decision | Meta}

**Reference**: Brookhart 2013 (analytic vs. holistic); Dawson 2017 (users and uses); #647

---

## Domain Adaptation

The L0-L3 numeric scale (0-3) is stable across all domains. **Label semantics** should match the evaluation domain. Select the label set that fits, or define custom labels appropriate to the domain.

| Domain | L0 | L1 | L2 | L3 |
|--------|----|----|----|----|
| **Conformance** (default) | Non-Conformant | Baseline | Compliant | Exemplary |
| **Creative Quality** | Unrecognizable | Emerging | Achieved | Transcendent |
| **Maturity** | Initial | Developing | Defined | Optimizing |
| **Process Quality** | Ad-hoc | Repeatable | Measured | Optimizing |
| **Decision Quality** | Unsupported | Partial | Grounded | Decisive |

**This rubric uses**: {label set name or "Custom: L0={}, L1={}, L2={}, L3={}"}

**Construction method** (Mertler 2001): Write L3 descriptors first, then L0 descriptors, then interpolate L1 and L2. Anchoring at extremes prevents vague intermediate levels.

**Reference**: L730 (domain-fit gap); CMMI/ISO 33000 (scale adaptation); Mertler 2001 (anchor at extremes)

---

## Eligibility Gates

Binary prerequisites evaluated BEFORE dimension scoring. If any gate fails, the subject is ineligible for assessment — do not proceed to dimension scoring.

| Gate ID | Requirement | Pass/Fail |
|---------|-------------|-----------|
| EG-1 | {binary prerequisite} | {Pass / Fail} |
| EG-2 | {binary prerequisite} | {Pass / Fail} |

**Design principle**: Eligibility gates check structural prerequisites that cannot be compensated by high dimension scores. A subject that fails EG-1 should not receive a quality assessment at all — the gate prevents wasted assessment effort and avoids masking fundamental deficiencies.

**Reference**: CMMI Level 1 (prerequisite gate); CLEAR framework (assurance gates); L689 (rubric-as-adversary); #651

---

## Dimension Classification

Each dimension must be classified as **Quality** or **Maturity**. Score quality and maturity dimensions in separate passes with separate evidence.

| Classification | Measures | Evidence Type | Example |
|----------------|----------|---------------|---------|
| **Quality** (capability) | How good is this specific output? | Per-output observation | "Voice-spirit alignment in this episode" |
| **Maturity** (consistency) | How consistently does this process work? | Cross-output pattern | "Assessment follows structured method across sessions" |

**Separation principle**: Quality and maturity dimensions answer different questions and should not be collapsed into a single composite unless explicitly justified. Consider producing separate quality and maturity scores.

**Reference**: CMMI capability vs. maturity levels; ISO 33000 process vs. capability dimensions; internal research (inter-rater agreement improved 50% → 87.5% after separation); #652

---

## Behavioral Anchoring

Performance level descriptors must describe **observable behavior**, not abstract achievements.

| Approach | Example | Problem |
|----------|---------|---------|
| **Achievement-framed** (avoid) | "Produces high-quality analysis" | Invites Goodhart gaming — what counts as "high-quality"? |
| **Behaviorally-anchored** (use) | "Analysis cites 3+ evidence sources, identifies root cause, and proposes testable remediation" | Observable, verifiable, non-gameable |

**Test**: For each performance level descriptor, ask: "Would a plausibly defective artifact PASS this criterion?" If yes, the criterion lacks discriminative power (L689).

**Reference**: BARS (Behaviorally Anchored Rating Scales); internal research (rubric-as-adversary); Anthropic "Demystifying Evals" 2026 (grade what was produced, not the path)

---

## Dimensions

### D1: {Dimension Name}

**Weight**: {percentage, e.g., 25%}
**Definition**: {what this dimension measures}

#### Criteria

| ID | Criterion | Weight | Critical? |
|----|-----------|--------|-----------|
| D1.1 | {criterion name} | {relative weight} | {Yes/No} |
| D1.2 | {criterion name} | {relative weight} | {Yes/No} |

#### Performance Levels

| Level | Score | Criteria |
|-------|-------|----------|
| L3: Exemplary | 3 | {specific observable criteria for this level} |
| L2: Compliant | 2 | {specific observable criteria for this level} |
| L1: Baseline | 1 | {specific observable criteria for this level} |
| L0: Non-Conformant | 0 | {specific observable criteria for this level} |

---

### D2: {Dimension Name}

**Weight**: {percentage}
**Definition**: {what this dimension measures}

#### Criteria

| ID | Criterion | Weight | Critical? |
|----|-----------|--------|-----------|
| D2.1 | {criterion name} | {relative weight} | {Yes/No} |

#### Performance Levels

| Level | Score | Criteria |
|-------|-------|----------|
| L3: Exemplary | 3 | {criteria} |
| L2: Compliant | 2 | {criteria} |
| L1: Baseline | 1 | {criteria} |
| L0: Non-Conformant | 0 | {criteria} |

---

{Add more dimensions as needed (D3, D4, etc.)}

---

## Critical Requirements

Items that cause automatic L0 regardless of other scores:

| ID | Requirement | Rationale |
|----|-------------|-----------|
| CR1 | {requirement} | {why this is blocking} |
| CR2 | {requirement} | {why this is blocking} |

## Scoring Method

**Method**: {WeightedAverage | Minimum | Additive | GatewayFirst}

### Calculation

```
1. Check Critical Requirements (if any CR fails → L0)
2. Score each criterion against performance levels
3. Calculate dimension scores: {formula}
4. Calculate composite score: {formula}
5. Map composite to overall level
```

### Score to Level Mapping

| Composite Score | Overall Level |
|-----------------|---------------|
| 2.5 - 3.0 | L3: Exemplary |
| 1.5 - 2.49 | L2: Compliant |
| 0.5 - 1.49 | L1: Baseline |
| 0.0 - 0.49 | L0: Non-Conformant |

---

## Evidence Requirements

| Dimension | Required Evidence |
|-----------|-------------------|
| D1 | {what evidence supports scoring} |
| D2 | {what evidence supports scoring} |

## Remediation Guidance

### From L0 to L1 (Baseline)

| Gap | Remediation Steps | Effort |
|-----|-------------------|--------|
| {common L0 issue} | {steps to reach L1} | {estimate} |

### From L1 to L2 (Compliant)

| Gap | Remediation Steps | Effort |
|-----|-------------------|--------|
| {common L1 issue} | {steps to reach L2} | {estimate} |

### From L2 to L3 (Exemplary)

| Gap | Remediation Steps | Effort |
|-----|-------------------|--------|
| {common L2 issue} | {steps to reach L3} | {estimate} |

---

## Usage

### When to Apply

{Conditions that trigger use of this rubric}

### How to Apply

1. Gather evidence per Evidence Requirements
2. Check Critical Requirements first
3. Score each criterion against performance levels
4. Calculate composite using Scoring Method
5. Document in Assessment Record

### Assessment Record Template

```markdown
## Assessment: {Subject} against {Rubric Name} v{version}

**Date**: YYYY-MM-DD
**Assessor**: {agent or human}
**Subject**: {what was assessed}

### Scores

| Dimension | Score | Notes |
|-----------|-------|-------|
| D1 | {0-3} | {observations} |
| D2 | {0-3} | {observations} |

### Composite

**Score**: {X.XX}/3.0 ({percentage}%)
**Level**: {L0|L1|L2|L3}

### Critical Requirements

| CR | Pass/Fail |
|----|-----------|
| CR1 | {status} |

### Gaps Identified

{list of gaps for remediation}

### Recommendations

{next steps}
```

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | YYYY-MM-DD | {author} | Initial rubric |

## Related Artifacts

| Artifact | Relationship |
|----------|--------------|
| {spec or SOP} | {what this rubric evaluates} |
| {L-doc} | {background or rationale} |

---

*Rubric created following SOP_RUBRIC_CREATION.md v2.0*
*Template: RUBRIC.template.md v2.0 (archetype-aware, domain-adaptive)*
*Ontology: ONTOLOGY_scoring_rubric_v1.0.yaml (C048-C093)*
