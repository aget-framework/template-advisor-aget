# .memory/ Directory - Advisor Memory Layer (Layer 4)

**Purpose**: Store advisor-specific relationship state, client context, and engagement history.

**Layer**: 4 (Memory) - Advisor instance state, not portable across domains

**Applies to**: Advisor agents only (advisor, consultant, coach, guru, mentor personas)

---

## Directory Structure

```
.memory/
├── clients/              # Client-specific context and relationship state
│   ├── {client_id}/     # Per-client directory
│   │   ├── context.yaml # Client background, preferences, goals
│   │   ├── history.md   # Interaction history, key insights
│   │   └── notes/       # Session notes, observations
│   └── .gitkeep
├── engagements/          # Engagement-specific state
│   ├── {engagement_id}/ # Per-engagement directory
│   │   ├── brief.yaml   # Engagement scope, objectives
│   │   ├── progress.md  # Status tracking, milestones
│   │   └── artifacts/   # Engagement-specific deliverables
│   └── .gitkeep
└── README.md            # This file
```

---

## Usage Examples

### Client Context (.memory/clients/)

**When to use**: Track ongoing relationships with specific clients

**Example**: `.memory/clients/alice_smith/context.yaml`
```yaml
client_id: alice_smith
name: Alice Smith
organization: TechCorp
role: Engineering Manager
preferences:
  communication_style: direct
  session_frequency: biweekly
  focus_areas: [leadership, delegation, strategic_thinking]
goals:
  - Transition from IC to engineering manager
  - Build effective 1:1 processes
  - Develop strategic planning skills
context:
  team_size: 8
  reports_to: Director of Engineering
  tenure: 6 months as manager
```

### Engagement State (.memory/engagements/)

**When to use**: Track specific projects or advisory engagements

**Example**: `.memory/engagements/leadership_transition_2025/brief.yaml`
```yaml
engagement_id: leadership_transition_2025
client_id: alice_smith
start_date: 2025-01-15
end_date: 2025-06-15
status: active
objectives:
  - Complete transition to managerial role
  - Establish team rhythm and processes
  - Deliver Q1 strategic plan
milestones:
  - name: Initial assessment
    due: 2025-01-31
    status: complete
  - name: 1:1 framework established
    due: 2025-02-28
    status: in_progress
```

---

## Layer 3/4 Boundary Rules

### ✅ Belongs in .memory/ (Layer 4)

**Relationship state** - ongoing client relationships, engagement tracking
**Client context** - background, preferences, goals, history
**Engagement artifacts** - project-specific deliverables, progress tracking
**Session continuity** - notes, insights, action items across multiple sessions

**Portability test**: Does this represent ongoing relationship state that wouldn't transfer to a different client/domain? → .memory/

### ❌ Belongs in .aget/ (Layer 3)

**Framework knowledge** - process learnings, methodology patterns
**Tool configuration** - agent capabilities, specifications
**Identity** - version, type, domain
**Operational state** - checkpoints, validation results

**Portability test**: Would this be useful if agent cloned to different domain? → .aget/

### ✅ Belongs in sessions/ (Layer 5)

**Session logs** - individual conversation records
**Work artifacts** - deliverables, analysis, recommendations
**Strategic sessions** - high-value interactions, key decisions

**Ownership test**: Is this the principal's work product? → sessions/

---

## Privacy & Security

**Classification**: .memory/ contains client-specific data
- **Never commit** sensitive personal information (PII, credentials)
- **Use placeholders** in examples ({client_id}, {engagement_id})
- **Respect boundaries**: Client data stays with advisor instance

**Git ignore recommendations** (add to .gitignore if needed):
```gitignore
.memory/clients/*/sensitive/
.memory/engagements/*/confidential/
```

---

## Initialization

**New advisor instances**: .memory/ structure created automatically
**Existing advisors**: Add .memory/ during v2.9 migration

**Initial state**:
- `.memory/clients/.gitkeep` (empty, ready for first client)
- `.memory/engagements/.gitkeep` (empty, ready for first engagement)

---

## FAQs

**Q: Do I need .memory/ if I have no ongoing clients?**
A: Yes, keep the structure. It's ready when you need it.

**Q: Can I use .memory/ for other types of state?**
A: Only relationship/engagement state. For other persistent state, use `.aget/` (framework) or `sessions/` (work product).

**Q: What's the difference between .memory/ and sessions/?**
A: `.memory/` = ongoing relationship state (client context, engagement tracking)
   `sessions/` = individual conversation logs (session-by-session work)

**Q: How long to retain .memory/ data?**
A: Client decision. Typical retention: active + 1 year post-engagement.

---

**Layer 4 Introduction**: v3.1.0 (2025-11-23)
**Related**: See AGENTS.md for complete 5-layer architecture
