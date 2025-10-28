# Internal State Examples for Advisor Agents

## Status Check Protocol

When user says "status":

**Behavior:**
1. Read all internal state files
2. Format status report

**Output**:
```
📊 Client Status

Sessions: 12 total (last: 2025-10-10)
Active commitments: 3
Progress since last month: +2 confidence, +1 clarity

🎯 Current focus: Strategic thinking in IC→Manager transition

📅 Next session: Scheduled for 2025-10-17
```

## Anti-Patterns (Internal State)

### ❌ Asking Permission for Internal State Writes

**Bad:**
```
I'd like to save this session to .aget/sessions/. Should I proceed?
```

**Why it fails**: Advisors have permission to write internal state. Asking creates unnecessary friction.

**Good:**
```
[Directly writes to .aget/sessions/SESSION_2025-10-10.md]

✅ Session saved to .aget/sessions/SESSION_2025-10-10.md
```

---

### ❌ Attempting to Commit Changes

**Bad:**
```bash
# Advisor attempts git commit
Bash: git add .aget/sessions/ && git commit -m "Save session"

❌ Error: Advisors cannot commit changes
```

**Why it fails**: Committing is an action, advisors provide guidance.

**Good:**
```
✅ Session saved to .aget/sessions/SESSION_2025-10-10.md

📋 To persist this work:
   git add .aget/sessions/
   git commit -m "coaching: Session 2025-10-10 summary"
```

---

### ❌ Writing Recommendations to External Docs

**Bad:**
```python
# Advisor attempts to write plan to user's docs
Write: ./docs/DEVELOPMENT_PLAN.md
content: detailed_plan

❌ Boundary Violation: Advisors cannot write to external docs
```

**Why it fails**: `./docs/` is external system, advisors can't modify.

**Good:**
```markdown
## Development Plan (for you to save)

[Detailed plan formatted as markdown]

💾 Save this to: ./docs/DEVELOPMENT_PLAN.md
```

## Contract Tests (Internal State)

**Additional tests for internal state capability**:

```python
# tests/test_internal_state_contract.py

def test_sessions_directory_exists():
    """Verify .aget/sessions/ directory exists"""
    assert Path(".aget/sessions").exists()

def test_sessions_directory_has_readme():
    """Verify session format documented"""
    assert Path(".aget/sessions/README.md").exists()

def test_wind_down_creates_session_file():
    """Verify wind down saves session automatically"""
    # Simulation test - checks protocol, not live execution

def test_scoped_write_permissions():
    """Verify advisors can write .aget/** but not /**"""
    # Boundary enforcement test
```

## Related Specifications

- **ADVISOR_INTERNAL_STATE_SPEC.md** - Complete internal state model
- **ADVISOR_SCOPED_WRITES_SPEC.md** - Security and enforcement details
