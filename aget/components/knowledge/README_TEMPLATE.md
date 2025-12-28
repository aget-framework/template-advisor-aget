# Domain Knowledge

This directory contains domain-specific beliefs NOT portable to other agents (L296).

## Portability Test

> "Clone to different domain. Still useful?"
> - YES → `.aget/evolution/`
> - NO → `knowledge/`

## Structure

```
knowledge/
├── README.md           # This file
├── {domain}/           # Domain-specific patterns
│   ├── patterns/       # Workflow patterns (.md)
│   └── heuristics/     # Decision rules (.yaml)
└── thresholds/         # Environment-specific values (.yaml)
```

## Capture Protocol

**When to capture**:
1. **Session end**: "What did I learn specific to THIS domain?"
2. **Discovery**: "This pattern only works HERE"
3. **Decision**: "This threshold fits THIS environment"

## Validation States

Mark in frontmatter:
- `Status: Hypothesis` - Untested assumption
- `Status: Validated` - Tested 3+ times, works
- `Status: Established` - Proven pattern

## Format Reference

| Content Type | Format | Location |
|--------------|--------|----------|
| Patterns     | Markdown (.md) | `{domain}/patterns/` |
| Heuristics   | YAML (.yaml) | `{domain}/heuristics/` |
| Thresholds   | YAML (.yaml) | `thresholds/` |

## What Belongs Here

**Domain beliefs (NOT portable)**:
- "This workspace uses 30-day archive cycles"
- "Risk threshold of 5 uncommitted files works for this workflow"
- "This API rate limit of 100/min is calibrated for this environment"

**NOT domain beliefs (should be in .aget/evolution/)**:
- "Gate discipline prevents scope creep" → Framework (portable)
- "Commits should have descriptive messages" → Framework (portable)

---
*Template from AGET v3.0.0 - Replace {domain} with your agent's domain*
