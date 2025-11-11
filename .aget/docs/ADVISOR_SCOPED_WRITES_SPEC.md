# Advisor Scoped Writes Specification

**Version**: 1.0
**Effective**: v2.5.0+
**Status**: NORMATIVE (contract-tested)
**Updated**: 2025-11-10 (L285 boundary clarification)

---

## Purpose

This specification defines what advisor agents can write to (internal state) vs what they cannot write to (external systems), establishing clear architectural boundaries to prevent:
- Privacy violations (personal data in framework directories)
- Deletion risks (user deletes `.aget/` loses critical domain data)
- Portability issues (domain data in framework layer)

---

## Core Principle

**Advisors maintain internal state but don't modify external systems**

```
INTERNAL STATE (CAN write):      EXTERNAL SYSTEMS (CANNOT write):
.aget/**                         ./** (everything else)
```

---

## Internal State vs Domain Data

### The Boundary Test

**For any data/knowledge, ask:**
> "If this agent gets cloned to a different domain/company, should this data come with it?"

- **YES** → `.aget/` (framework knowledge, portable)
- **NO** → Root level (domain data, project-specific)

### What is "Internal State"?

**Internal state** = Minimal data for session continuity and agent operations

✅ **Permitted in `.aget/`:**
- **Session snapshots** (`.aget/checkpoints/`) - Lightweight state for resumption
- **Minimal context** (`.aget/context/session.json`) - IDs only, no content
- **Framework patterns** (`.aget/evolution/L###.md`) - HOW to approach problems
- **Agent specs** (`.aget/specs/`) - Agent capability definitions
- **Helper tools** (`.aget/tools/`) - Scripts for agent operations
- **Intelligence patterns** (`.aget/intelligence/`) - Framework-level learning (e.g., ambiguity_corpus.yaml)

### What is "Domain Data"?

**Domain data** = Project-specific content that belongs to the user's work

❌ **Forbidden in `.aget/`:**
- **Case data** (cases/, claims/, policies/, contracts/) - Domain entities
- **Domain knowledge** (knowledge/) - Reference materials specific to this project
- **Work history** (sessions/) - Log of what agent did (belongs to project, not framework)
- **Domain decisions** (workspace/decisions/) - Project-specific choices
- **Client tracking** (workspace/client_progress/, workspace/commitments/) - User work state
- **Domain examples** (workspace/examples/) - Project-specific demonstrations
- **Work products** (products/, deliverables/) - Agent outputs for user

---

## Permitted Locations & Size Limits

### .aget/checkpoints/ (Session State)

**Purpose**: Session state snapshots for resumption
**Max size**: 50KB per file
**Format**: Markdown with YAML frontmatter
**Example**:
```markdown
---
session_id: sess_20251110_001
client_id: principal_user
status: paused
---

# Session State

- Active topic: Contract analysis
- Next action: Review clause 7.2
```

**Rationale**: Lightweight state enables session continuity without storing domain content

### .aget/context/ (Minimal Context)

**Purpose**: Minimal IDs for session context
**Max size**: 1KB per file
**Format**: JSON with IDs only (no content)
**Example**:
```json
{
  "session": {
    "client_id": "melissa",
    "active_case_id": "case_20251110"
  }
}
```

**Rationale**: IDs let agent resume work, actual content stays at root

### .aget/evolution/ (Process Learnings)

**Purpose**: HOW to approach problems (not WHAT the problem is)
**Max size**: No limit (process knowledge accumulates)
**Format**: Learning documents (L###_pattern_name.md)
**Example**: `L285_advisor_aget_boundary_violations.md`

**Rationale**: Process patterns are portable across domains

---

## Prohibited Patterns

### ❌ Anti-Pattern 1: Domain Entities in .aget/

**Wrong:**
```
.aget/cases/john_doe/medical_history.md           # Personal case data
.aget/policies/my_policy_account_123456.md         # Policy with account numbers
.aget/contracts/vendor_agreement_acme.pdf          # Contract document
```

**Why wrong:**
- Privacy: Personal identifiers in framework directory
- Deletion risk: User deletes `.aget/` → loses critical data
- Portability: These don't belong in portable framework layer

**Right:**
```
cases/john_doe/medical_history.md                  # At root
data/policies/my_policy.md                         # At root
contracts/vendor_agreement_acme.pdf                # At root

# Agent can still READ these via Read tool
# Agent just can't WRITE to them (advisory role)
```

### ❌ Anti-Pattern 2: Domain Knowledge Base in .aget/

**Wrong:**
```
.aget/knowledge/
├── vendor_profiles/acme_corp.md                   # Domain vendor info
├── market_intelligence/competitor_analysis.md     # Domain research
└── frameworks/our_evaluation_rubric.md            # Domain-specific rubric
```

**Why wrong:**
- This is CONTENT about domain, not PROCESS for agent
- Not portable to other domains/projects
- Belongs at root as reference materials

**Right:**
```
knowledge/                                         # At root
├── vendor_profiles/acme_corp.md
├── market_intelligence/competitor_analysis.md
└── frameworks/evaluation_rubric.md

.aget/evolution/L###_vendor_evaluation_patterns.md # Process learning (how to evaluate)
```

### ❌ Anti-Pattern 3: Work History in .aget/

**Wrong:**
```
.aget/sessions/SESSION_2025-11-10.md              # Work log
```

**Why wrong:**
- Sessions = work history (belongs to project, not framework)
- User deletes `.aget/` thinking it's "just framework" → loses entire work log
- Work history should survive framework changes/resets

**Right:**
```
sessions/SESSION_2025-11-10.md                     # At root

.aget/checkpoints/session_state_latest.md         # Lightweight resumption state
```

### ❌ Anti-Pattern 4: Client Work Tracking in .aget/

**Wrong:**
```
.aget/client_progress/melissa_development_plan.yaml   # Client-specific work state
.aget/commitments/active_obligations.yaml              # User's commitments
.aget/coverage_gaps/insurance_risk_assessment.md       # Domain analysis output
```

**Why wrong:**
- These are outputs of advisory work (belong to user)
- User might want to share/backup without framework
- Not portable (specific to this engagement/project)

**Right:**
```
workspace/client_progress/melissa_development_plan.yaml
workspace/commitments/active_obligations.yaml
workspace/coverage_gaps/insurance_risk_assessment.md

# Or at root if they're primary deliverables:
reports/insurance_risk_assessment_2025-11-10.md
```

---

## Enforcement

### Contract Tests

All advisor agents must pass boundary contract tests:

```python
# tests/test_aget_boundary.py

def test_no_domain_directories_in_aget():
    """Verify no domain-specific directories in .aget/"""
    forbidden = [
        'cases', 'claims', 'policies', 'contracts',
        'knowledge', 'client_progress', 'commitments',
        'decisions', 'examples', 'coverage_gaps', 'sessions',
        'learning', 'deliverables', 'products',
        'clients', 'customers', 'vendors'
    ]

    aget_dir = Path('.aget')
    violations = [d for d in aget_dir.iterdir()
                  if d.is_dir() and d.name in forbidden]

    assert len(violations) == 0, (
        f"Domain directories in .aget/: {violations}\n"
        f"Move to root level (see L285)"
    )
```

### Tool-Level Enforcement

| Tool | Allowed Paths | Forbidden Paths | Behavior on Violation |
|------|--------------|-----------------|----------------------|
| **Read** | `/**` (unrestricted) | None | N/A (read-only) |
| **Write** | `.aget/**` | `/**` (all other) | Error: Boundary violation |
| **Edit** | `.aget/**` | `/**` (all other) | Error: Boundary violation |
| **Bash** | Read-only commands | Write commands, git | Error: Operation not permitted |

---

## Migration Guide

**If you have domain data in `.aget/`** (discovered via audit):

1. **Move domain directories to root:**
   ```bash
   git mv .aget/cases cases/
   git mv .aget/knowledge knowledge/
   git mv .aget/sessions sessions/
   git mv .aget/policies data/policies/
   ```

2. **Update AGENTS.md path references:**
   - Change `.aget/cases/` → `cases/`
   - Change `.aget/knowledge/` → `knowledge/`
   - Change `.aget/sessions/` → `sessions/`

3. **Commit with rationale:**
   ```bash
   git commit -m "fix: Move domain data from .aget/ to root (L285 boundary violation)"
   ```

4. **Validate fix:**
   ```bash
   python3 -m pytest tests/test_aget_boundary.py -v
   ```

---

## Validation Checklist

Before declaring compliance:

- [ ] No personal/sensitive data in `.aget/`
- [ ] No domain-specific directories in `.aget/`
- [ ] `sessions/` at root (not `.aget/sessions/`)
- [ ] Domain data at root level (cases/, knowledge/, data/)
- [ ] `.aget/evolution/` contains PROCESS learnings (not CONTENT)
- [ ] `.aget/checkpoints/` contains minimal session state only (<50KB per file)
- [ ] Boundary test passes: "Clone to different domain → .aget/ still useful"

---

## Related Documentation

- **L285_advisor_aget_boundary_violations.md** - Discovery and remediation of fleet boundary violations
- **AGENTS.md** - Template configuration (references this spec)
- **test_aget_boundary.py** - Contract tests enforcing this spec

---

**Version History:**
- **v1.0** (2025-11-10): Initial specification (L285 boundary clarification)

---

**Normative Status**: This specification is contract-tested. All advisor agents must comply.
