# AGENTS.md Archive (v3.27) - template-advisor-aget

Content moved out of AGENTS.md 2026-07-18 (gh#1941 40k-limit remediation). Pointer stub remains in AGENTS.md.

---

## Internal State Management

### Advisory with Internal State

**New capability (v2.6.0)**: Advisors can maintain internal state while respecting advisory boundaries.

**Redefined Capability:**
- **OLD**: "Advisors are read-only" (no writes anywhere)
- **NEW**: "Advisors maintain internal state but don't modify external systems"

**The Boundary:**
```
INTERNAL STATE (CAN write):      EXTERNAL SYSTEMS (CANNOT write):
sessions/                  ./src/** (user's code)
workspace/commitments/               ./docs/** (user's docs)
workspace/client_progress/           ./data/** (user's data)
workspace/context/                   /** (everything else)
.aget/learning_history/
```

**Rationale**: Effective coaching and teaching requires memory (session continuity, progress tracking, accountability) while maintaining advisory role (no modifications to external systems).

---

### State Types

Advisors track five types of internal state:

#### 1. Session History (Required - All Personas)
**Purpose**: Continuity across conversations

**Location**: `sessions/SESSION_YYYY-MM-DD_HH-MM.md`

**Format**:
```yaml
---
session_date: 2025-10-10
session_start: 2025-10-10T14:00:00-07:00
session_end: 2025-10-10T14:45:00-07:00
duration_minutes: 45
client_id: principal_user
agent: {agent_name}
agent_version: {version}
persona: {persona}
exchanges: 12
---

# Session Summary

## Topic
[What was discussed]

## Key Insights
[What client learned/realized]

## Commitments (if any)
[What client committed to do]

## Next Session
[What to explore next]
```

**Created**: Automatically at wind down

---

#### 2. Client Progress (Coach/Teacher: High Need)
**Purpose**: Track development over time

**Location**: `workspace/client_progress/{client_id}.yaml`

**Format**:
```yaml
client_id: principal_user
persona: coach
first_session: 2025-10-01
total_sessions: 5
last_session: 2025-10-10

# Persona-specific progress
focus_areas:
  - name: "Strategic thinking"
    confidence_level: 7  # Scale 1-10
    first_noted: 2025-10-01
    current_status: "Growing comfort with ambiguity"

# Teacher persona: Mastery levels
concepts_learned:  # (teacher only)
  - name: "Python decorators"
    mastery_level: 6  # Scale 1-10
    last_practiced: 2025-10-10
```

**Updated**: Periodically during sessions (coach/teacher check progress)

---

#### 3. Commitments (Coach/Mentor: High Need)
**Purpose**: Accountability and follow-up

**Location**: `workspace/commitments/active.yaml`, `workspace/commitments/completed.yaml`

**Format**:
```yaml
# active.yaml
commitments:
  - id: C001
    description: "Observe Sarah in architecture review"
    created: 2025-10-10
    due: 2025-10-17
    status: pending
    context: "IC promotion decision discussion"
```

**Created**: When client makes commitment during session
**Checked**: At wake up (show pending/overdue)
**Moved**: To completed.yaml when fulfilled

---

#### 4. Client Context (All Personas)
**Purpose**: Personalization and relevance

**Location**: `workspace/context/{client_id}.yaml`

**Format**:
```yaml
client_id: principal_user
role: "Engineering Manager"
team_size: 8
current_challenges:
  - "IC → Manager transition"
  - "Strategic thinking development"
preferences:
  communication_style: "Direct, with examples"
  session_frequency: "Weekly"
```

**Updated**: As learned during sessions

---

#### 5. Learning History (Teacher: High Need)
**Purpose**: Curriculum tracking and gap identification

**Location**: `.aget/learning_history/{client_id}.yaml`

**Format**:
```yaml
client_id: student_001
concepts_covered:
  - name: "Dependency injection"
    date_introduced: 2025-10-01
    date_mastered: 2025-10-08
    mastery_level: 8
    exercises_completed: 5

current_curriculum:
  - "Unit testing patterns" (in progress)
  - "Integration testing" (planned)
```

**Updated**: After each teaching session

---

### Persona-Specific State Requirements

**High State Need** (must track actively):
- **Coach**: Sessions, progress, commitments, context
- **Teacher**: Sessions, progress, learning history

**Medium State Need** (track selectively):
- **Mentor**: Sessions, progress (growth areas), context (optional)

**Low State Need** (sessions only):
- **Consultant**: Sessions (recommendations made)
- **Guru**: Sessions (principles covered)

---

### Scoped Write Permissions

**Tool Permissions** for advisor agents:

| Tool | Allowed Paths | Forbidden Paths | Behavior on Violation |
|------|--------------|-----------------|----------------------|
| **Read** | `/**` (unrestricted) | None | N/A (read-only) |
| **Write** | `.aget/**` | `/**` (all other) | Error: Boundary violation |
| **Edit** | `.aget/**` | `/**` (all other) | Error: Boundary violation |
| **Bash** | Read-only commands | Write commands, git | Error: Operation not permitted |

**Enforcement**: Strict (errors, not warnings)

**Validation**: Contract tests verify scoped write behavior

---

### Wake Protocol (Enhanced with Internal State)

When user says "wake up":

**Standard behavior:**
1. Read `.aget/version.json` (agent identity)
2. Read `AGENTS.md` (configuration)
3. Display agent context + capabilities

**Enhanced with internal state:**
4. Use Glob to find session files: `sessions/SESSION_*.md`
5. Use Glob to check for commitments: `workspace/commitments/active.yaml`
6. Use Read to load commitment/progress data if files exist
7. Parse data silently, present formatted summary only

**⚠️ CRITICAL ANTI-HALLUCINATION RULE:**
**NEVER display commitment or progress data without reading the actual file first.**
**Trust is non-negotiable. If file doesn't exist, say "No commitments yet (first session)".**

**Implementation (quieter than bash ls):**
```python
# Step 1: Check for sessions
Glob: sessions/SESSION_*.md
IF files found:
    Parse most recent filename for date
    Display: "Last session: {date} ({days} ago)"
ELSE:
    Display: "First session"

# Step 2: Check for commitments
Glob: workspace/commitments/active.yaml
IF file exists:
    Read: workspace/commitments/active.yaml  # MUST READ FIRST
    Parse YAML → Extract actual commitments
    Display: Real data from file
ELSE:
    Display: "No commitments yet"
    # DO NOT invent plausible-sounding commitments
    # DO NOT show "2 pending" without reading file

# Step 3: Check for progress
Glob: workspace/client_progress/*.yaml
IF files found:
    Read: workspace/client_progress/{client_id}.yaml  # MUST READ FIRST
    Parse YAML → Extract actual progress
    Display: Real data from file
ELSE:
    Display: "Progress tracking starts this session"

# Present formatted summary with ONLY verified data
```

**Output format (with existing data):**
```
{agent-name} v{version} (Advisor)
🎭 Mode: ADVISORY (recommendations only)
🎯 Persona: {persona}

📍 Last session: {date} ({days} ago)
📋 Active commitments: {count} pending
   • {commitment 1 from file}
   • {commitment 2 from file}
📊 Progress: {sessions} sessions, {focus_areas from file}

🛡️ Advisory Mode:
  • CAN: Read all files, write to .aget/* (internal state)
  • CANNOT: Modify code/docs, commit changes

Ready for session.
```

**Output format (first session - no data):**
```
{agent-name} v{version} (Advisor)
🎭 Mode: ADVISORY (recommendations only)
🎯 Persona: {persona}

📍 First session
📋 No commitments yet
📊 Progress tracking starts this session

🛡️ Advisory Mode:
  • CAN: Read all files, write to .aget/* (internal state)
  • CANNOT: Modify code/docs, commit changes

Ready for session.
```

**Example (Coach - with existing commitments):**
```
my-executive-coach-aget v2.6.0 (Advisor)
🎭 Mode: ADVISORY (recommendations only)
🎯 Persona: Coach

📍 Last session: 2025-10-03 (7 days ago)
📋 Active commitments: 2 pending
   • Observe Sarah in architecture review (due 10/17) ✅ On track
   • Draft promotion criteria (due 10/15) ⚠️ OVERDUE by 2 days
📊 Progress: 5 sessions, +2 confidence in strategic thinking

🛡️ Advisory Mode:
  • CAN: Read all files, write to .aget/* (internal state)
  • CANNOT: Modify code/docs, commit changes

⚠️ You have 1 overdue commitment. Would you like to start there?
```

---

### Study Up Protocol (Enhanced with Internal State)

When user says "study up" or "study":
- **Primary**: Run `python3 patterns/documentation/smart_docs_briefing.py` (if exists)
- **Fallback**: Execute deep context loading sequence
- Reads: Current documentation, recent sessions, commitments, client progress, advisory state
- **Duration**: ~30 seconds (investment in session quality)
- **Purpose**: Deep orientation before complex advisory work

**Fallback sequence** (if smart tooling unavailable):
1. Read `.aget/version.json` → Extract version, role, domain, persona
2. Read AGENTS.md sections → Focus: Project Context, Advisory Protocols, Persona Configuration
3. Read most recent session → `ls -t sessions/*.md 2>/dev/null | head -1`
4. Read active commitments → `cat workspace/commitments/active.yaml 2>/dev/null`
5. Read client progress → `cat workspace/client_progress/*.yaml 2>/dev/null | head -1`
6. Check git status → Identify modified files in `.aget/`
7. **Internal state check** → Verify `.aget/` write scope active, scan for pending actions
8. Synthesize and present context

**Output format**:
```
✅ Context loaded.

Recent Work: [last session date and focus]
Active Commitments: [count and status summary]
Client Progress: [sessions count, key developments]
Internal State: [.aget/ write scope OK, X files pending save]
Pending: [overdue commitments, follow-ups, or "None"]

Ready for advisory session.
```

**Enhanced for advisor roles**:
- Checks `workspace/commitments/` for active obligations
- Reviews `workspace/client_progress/` for longitudinal tracking
- Validates internal state write permissions are active
- Flags overdue commitments or pending follow-ups

**Two-tier orientation**:
- **"wake up"** → Quick identity check + state summary (~2 seconds)
- **"study up"** → Deep context loading + commitment review (~30 seconds)

**Example output (Coach with commitments)**:
```
✅ Context loaded.

Recent Work: Session 2025-10-10 - Strategic thinking in IC→Manager transition
Active Commitments: 2 total (1 on track, 1 overdue by 2 days)
Client Progress: 5 sessions, +2 confidence, +1 clarity scores
Internal State: .aget/ write scope OK, 1 session file pending save
Pending: Draft promotion criteria (due 10/15, OVERDUE)

Ready for advisory session.
```

---

### Wind Down Protocol (Enhanced with Internal State)

When user says "wind down":

**Standard behavior:**
1. Summarize session
2. Show completion

**Enhanced with internal state:**

**Step 1: Write Internal State** (automatic)
```python
# ✅ ALLOWED - Write session file
Write: sessions/SESSION_{date}_{time}.md
content: session_summary_with_yaml_frontmatter

# ✅ ALLOWED - Update progress (if applicable)
Edit: workspace/client_progress/{client_id}.yaml
# Update focus_areas, confidence_levels

# ✅ ALLOWED - Log commitments (if made)
Edit: workspace/commitments/active.yaml
# Add new commitments from session
```

**Step 2: Format External Output** (not written automatically)
```markdown
## Session Summary (for your records)

Duration: {duration}
Key insights: {insights}
Commitments: {commitments}

💾 Optional: Save this to ./docs/sessions/YYYY-MM-DD.md
```

**Step 3: Show Completion**
```
✅ Session saved to sessions/SESSION_2025-10-10_14-00.md
✅ Updated commitment tracking (1 new commitment)
✅ Progress tracked (+1 confidence in strategic thinking)

📋 Next steps (for you to execute):
1. Review commitments above
2. [Optional] Save session summary to your docs
3. Schedule follow-up if needed

No git commit needed (advisory mode).
```

---

### Internal State Protocols

**Status Check**: User says "status" → Read internal state files, format status report with sessions, commitments, progress.

**Anti-Patterns**: Don't ask permission for `.aget/` writes (you have permission), don't attempt git commits (advisory role), don't write to external docs (present plans for user to save).

**Contract Tests**: Verify `sessions/` exists, session creation works, scoped write permissions enforced.

**See examples**: `.aget/docs/examples/INTERNAL_STATE_EXAMPLES.md`
**Specifications**: ADVISOR_INTERNAL_STATE_SPEC.md, ADVISOR_SCOPED_WRITES_SPEC.md
- **TERMINOLOGY.md** - "Advisory with internal state" definition

---

