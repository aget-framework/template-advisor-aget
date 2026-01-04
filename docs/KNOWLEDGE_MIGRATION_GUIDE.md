# Migration Guide: Knowledge Directory Setup

This guide helps agents add the `knowledge/` directory structure for domain belief capture.

## Background

AGET v3.0 introduced the L296 taxonomy distinguishing:
- **Framework beliefs** (`.aget/evolution/`) - Portable to any domain
- **Domain beliefs** (`knowledge/`) - Specific to this agent's context

## Detection

Check if your agent needs migration:

```bash
# Does knowledge/README.md exist?
ls knowledge/README.md 2>/dev/null && echo "✅ Already configured" || echo "❌ Needs migration"
```

| Current State | Action |
|---------------|--------|
| No `knowledge/` directory | Full migration |
| `knowledge/` with `.gitkeep` only | Add README.md |
| `knowledge/README.md` exists | No action needed |

## Migration Steps

### Option 1: Copy from Template (Recommended)

```bash
# From your agent's root directory
curl -sL https://raw.githubusercontent.com/aget-framework/template-github-aget/main/knowledge/README.md \
  -o knowledge/README.md

# Create structure
mkdir -p knowledge/thresholds
touch knowledge/thresholds/.gitkeep
```

### Option 2: Copy from Components

If you have access to template-github-aget locally:

```bash
# Copy README template
cp ../template-github-aget/aget/components/knowledge/README_TEMPLATE.md knowledge/README.md

# Create structure
mkdir -p knowledge/thresholds
touch knowledge/thresholds/.gitkeep
```

### Option 3: Manual Creation

Create `knowledge/README.md` with this content:

```markdown
# Domain Knowledge

This directory contains domain-specific beliefs NOT portable to other agents (L296).

## Portability Test

> "Clone to different domain. Still useful?"
> - YES → `.aget/evolution/`
> - NO → `knowledge/`

## Structure

knowledge/
├── README.md           # This file
├── {domain}/           # Domain-specific patterns
│   ├── patterns/       # Workflow patterns (.md)
│   └── heuristics/     # Decision rules (.yaml)
└── thresholds/         # Environment-specific values (.yaml)

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
```

## Post-Migration

### 1. Customize Domain Structure

Replace `{domain}` with your agent's domain:

```bash
# Example for a healthcare agent
mkdir -p knowledge/healthcare/patterns
mkdir -p knowledge/healthcare/heuristics
```

### 2. Update AGENTS.md (Optional)

Add to your Directory Structure section:

```markdown
├── knowledge/                # Domain beliefs (NOT portable, L296)
│   ├── README.md             # Capture protocol and taxonomy
│   ├── {domain}/             # Domain-specific patterns
│   └── thresholds/           # Environment-specific values
```

### 3. Verify

```bash
# Check structure
find knowledge -type f

# Expected output:
# knowledge/README.md
# knowledge/thresholds/.gitkeep
# knowledge/{domain}/patterns/... (if created)
```

## Verification Checklist

- [ ] `knowledge/README.md` exists
- [ ] README contains L296 portability test
- [ ] README contains capture protocol
- [ ] README contains validation states
- [ ] `knowledge/thresholds/` directory exists
- [ ] AGENTS.md references knowledge/ (optional)

## Common Issues

### "I already have knowledge files scattered around"

Consolidate them:
```bash
# Move existing domain knowledge
mv docs/domain-patterns.md knowledge/{domain}/patterns/
mv config/thresholds.yaml knowledge/thresholds/
```

### "What's the difference from .aget/evolution/?"

| Content | Location | Portability |
|---------|----------|-------------|
| "Gate discipline prevents scope creep" | `.aget/evolution/` | ✅ Works anywhere |
| "This workspace uses 30-day cycles" | `knowledge/` | ❌ Only here |

---

*Migration guide from AGET v3.1.0*
