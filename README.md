# Template: Advisor Agent

> Assess risks and provide recommendations with evidence-based guidance

**Version**: v3.27.0 | **Archetype**: Advisor | **Skills**: 2 specialized + 15 universal

---

## Why Advisor?

The Advisor archetype delivers **structured guidance** for decision-making. Unlike general AI assistants that offer opinions, advisor agents provide:

- **Risk assessment** — Evaluate likelihood, impact, and mitigation options for decisions
- **Recommendations** — Present options with rationale, alternatives, and confidence levels
- **Advisory discipline** — Inform decisions without making them, maintaining clear accountability

**For evaluators**: If you need an AI that provides expert guidance with structured reasoning rather than ad-hoc suggestions, the Advisor archetype brings rigor to your decision support.

**Domain knowledge that compounds**: Advisor agents build persistent understanding of your decision landscape — recurring risks, mitigation outcomes, and decision patterns. Unlike tools that start fresh each session, your agent accumulates advisory context that makes each risk assessment more calibrated and each recommendation more grounded.

---

## Skills

Advisor agents come with **2 archetype-specific skills** plus the universal AGET skills.

### Archetype Skills

| Skill | Description |
|-------|-------------|
| **aget-assess-risk** | Assess risks with likelihood/impact analysis. Categorizes risks (operational, strategic, technical) and provides mitigation recommendations. |
| **aget-recommend-action** | Provide structured recommendations with clear rationale, alternatives considered, and confidence levels. Advisory role maintained. |

### Universal Skills

All AGET agents include session management, knowledge capture, and health monitoring:

- `aget-wake-up` / `aget-wind-down` — Session lifecycle
- `aget-create-project` / `aget-review-project` — Project management
- `aget-record-lesson` / `aget-record-observation` — Learning capture
- `aget-check-health` / `aget-check-kb` / `aget-check-evolution` — Health monitoring
- `aget-propose-skill` / `aget-create-skill` — Skill development
- `aget-save-state` / `aget-file-issue` — State and issue management

---

## Ontology

Advisor agents use a **formal vocabulary** of 6 concepts organized into 2 clusters:

| Cluster | Concepts |
|---------|----------|
| **Risk Assessment** | Risk, Risk_Score, Mitigation |
| **Strategic Guidance** | Recommendation, Strategy, Alternative |

This vocabulary enables precise communication about advisory decisions.

See: [`ontology/ONTOLOGY_advisor.yaml`](ontology/ONTOLOGY_advisor.yaml)

---

## Quick Start

```bash
# 1. Clone the template
git clone https://github.com/aget-framework/template-advisor-aget.git my-advisor-agent
cd my-advisor-agent

# 2. Configure identity
# Edit .aget/version.json:
#   "agent_name": "my-advisor-agent"
#   "domain": "your-domain"

# 3. Verify setup
python3 -m pytest tests/ -v
# Expected: All tests passing
```

### Try the Skills

```bash
# In Claude Code CLI
/aget-assess-risk        # Evaluate risks for a decision
/aget-recommend-action   # Get structured recommendation
```

---

## What Makes Advisor Different

| Aspect | Generic AI Opinion | Advisor Agent |
|--------|-------------------|---------------|
| **Risk analysis** | "This might be risky" | Likelihood × Impact matrix with scores |
| **Recommendations** | Single suggestion | Multiple options with trade-offs |
| **Confidence** | Implicit | Explicit confidence levels |
| **Accountability** | Unclear | Advisory role clearly maintained |
| **Domain memory** | Starts fresh each session | Accumulates advisory expertise over time |

---

## .claude/ Directory

| Directory | Purpose | Owner |
|-----------|---------|-------|
| `.claude/skills/` | Slash command definitions | Framework + Agent |
| `.claude/agents/` | Subagent definitions | Agent |
| `.claude/rules/` | Path-scoped context rules | Agent |

Skills are provided by the template. Agents and rules directories are scaffolded for your customization.

---

## Framework Specification

| Attribute | Value |
|-----------|-------|
| **Framework** | [AGET v3.12.0](https://github.com/aget-framework/aget) |
| **Archetype** | Advisor |
| **Skills** | 17 total (2 archetype + 15 universal) |
| **Ontology** | 6 concepts, 2 clusters |
| **License** | Apache 2.0 |

---

## Learn More

- **[AGET Framework](https://github.com/aget-framework/aget)** — Core framework documentation
- **[Archetype Guide](https://github.com/aget-framework/aget/blob/main/docs/GETTING_STARTED.md)** — All 12 archetypes explained
- **[Getting Started](https://github.com/aget-framework/aget/blob/main/docs/GETTING_STARTED.md)** — Full onboarding guide

---

## Related Archetypes

| Archetype | Best For |
|-----------|----------|
| **[Analyst](https://github.com/aget-framework/template-analyst-aget)** | Data-driven insights and reporting |
| **[Consultant](https://github.com/aget-framework/template-consultant-aget)** | Client engagement and proposals |
| **[Executive](https://github.com/aget-framework/template-executive-aget)** | Strategic decision authority |

---

**AGET Framework** | Apache 2.0 | [Issues](https://github.com/aget-framework/aget/issues)
