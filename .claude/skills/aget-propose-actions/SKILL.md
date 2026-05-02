---
name: aget-propose-actions
description: Propose ranked next-best actions with evidence grounding, time budgets, and execute-all default. Formalizes the fleet's highest-frequency interaction pattern.
---

# /aget-propose-actions

Propose ranked next-best actions with evidence grounding, time budgets, and execute-all default. Supersedes the informal "step back. N next-best actions" trigger phrase.

## Purpose

The principal's most frequent interaction pattern across the entire fleet (3-5x per session, every agent, every session) is: "step back. N next-best actions, in this session, within the next M mins." Currently each agent interprets this differently — varying in depth, format, evidence citation, and execution behavior. This skill standardizes input parsing, KB review trigger (L335), output format, evidence grounding, parameterization, and the execute-all default (AGENTS.md).

**Evidence**: 34+ agents use identical phrasing. L637 (Mid-Session Steering via NBAs), L677 (Divergent Proposal Mode), L693 (5-action default), L787 (interpretation variance across agents). #721 (prior issue). 10+ invocations across 6 agents in v3.12.0 lifecycle.

## Input

$ARGUMENTS

Parameters (parsed from natural language):

| Parameter | Source | Default | Grammar |
|-----------|--------|---------|---------|
| `count` | First number in prompt | 5 (per L693) | "N next-best actions" |
| `budget` | Time expression in prompt | 30 min | "within the next N mins/hr" |
| `focus` | Remainder of prompt | Session mandate | "focus on X" / "for Y" |

Examples:
- `/aget-propose-actions` — 5 actions, 30-min budget, session mandate focus
- `/aget-propose-actions 3 actions within 45 mins` — 3 actions, 45-min budget
- `/aget-propose-actions 7 actions focus on release prep` — 7 actions, 30-min default, release focus
- `step back. 5 next-best actions, in this session, within the next 1hr` — Natural language trigger

## Execution

### Step 1: Parse Parameters

Extract `count`, `budget`, and `focus` from $ARGUMENTS or conversation context. Apply defaults for omitted parameters.

### Step 2: KB Review (L335)

Before proposing, scan current state:

1. Read active PROJECT_PLANs in `planning/` — identify current gates and pending deliverables
2. Check git status for uncommitted work
3. Review conversation context for session mandate and progress so far
4. Surface any pending work from prior sessions (resume hints)

This is mandatory (R-PA-005). Proposals without current-state grounding are stale.

### Step 3: Generate Actions

For each proposed action:
1. Derive from KB review findings, session mandate, and focus area
2. Estimate duration (must fit within budget)
3. Cite evidence (L-doc, issue number, session finding, or PROJECT_PLAN reference)
4. Assess risk-if-skipped (what happens if this is deferred)

Rank by value-to-time ratio. Total estimated time MUST fit within budget.

### Step 4: Present

Output using standardized format:

```
**[Agent Name] -- [count] Next-Best Actions ([budget]-minute window):**

**Session goal**: [restate primary objective]
**Progress**: [key milestones reached]

| # | Action | Time | Value | Risk if Skipped |
|---|--------|:----:|-------|-----------------|
| 1 | ... | N min | ... | ... |

Execution default: all [count], priority order (per Execute-All Default).
```

### Step 5: Execute-All Default

After presenting, execute all actions in priority order unless the user explicitly selects a subset. Do NOT ask "which ones?" — the default is full execution. Pause only for destructive actions (file deletion, force-push, issue closure).

## Requirements

| ID | Requirement | Source |
|----|-------------|--------|
| REQ-PA-001 | Propose-actions SHALL include identity header (agent name + session goal) | #618, SP-011 |
| REQ-PA-002 | NBA count SHALL match requested count or explain shortfall | SP-011 |
| REQ-PA-003 | Each NBA SHALL cite evidence (L-doc, issue, or session finding) | SP-011, L335 |
| REQ-PA-004 | Total estimated time SHALL fit within budget parameter | SP-011 |
| REQ-PA-005 | KB review SHALL be performed before proposing (active plans, git status) | L335, SP-011 |
| REQ-PA-006 | Execute-all SHALL be the default behavior after presentation | AGENTS.md Execute-All Default |
| REQ-PA-007 | Focus parameter SHALL constrain all NBAs to the specified area | SP-011 |

## Constraints

- **C1**: This skill is NBA-only — do NOT include kb-review, kb-maintenance, or plan-revision modes (those are separate concerns)
- **C2**: MUST perform KB review before proposing — proposals without current-state grounding are prohibited
- **C3**: MUST cite evidence for every action — no unsupported suggestions
- **C4**: MUST NOT ask "which ones?" after presenting — execute-all is the default

## Traceability

| Link | Reference |
|------|-----------|
| Proposal | SP-011 (`planning/skill-proposals/PROPOSAL_aget-propose-actions.md`) |
| Supersedes | PROPOSAL_aget-step-back.md (scope narrowed to NBA-only) |
| Verb family | propose-skill (SP-NNN), propose-project (SP-NNN), propose-actions (SP-011) |
| Upstream issues | #721 (aget-next-actions), #618 (identity header), #865 (NBA rendering) |
| L-docs | L335 (Memory Architecture), L637 (Mid-Session Steering), L677 (Divergent Proposal), L693 (5-action default), L787 (interpretation variance) |

---

*aget-propose-actions v0.1.0*
*Category: Research*
*Verb family: propose-skill, propose-project, propose-actions*
