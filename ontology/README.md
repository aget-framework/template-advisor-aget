# Ontology Directory

Formal vocabulary definitions for this advisor agent.

## Purpose

This directory stores the agent's domain ontology — the formal vocabulary that defines **what concepts exist** and **how they relate**. This is distinct from:

| Directory | Purpose | Analogy |
|-----------|---------|---------|
| `ontology/` | Schema (concepts, relationships) | Database schema |
| `knowledge/` | Instances (curated content) | Database rows |
| `.aget/` | Framework config (AGET vX) | Operating system |
| `specs/` | Requirements, designs | Engineering docs |

## Format: YAML + SKOS + EARS

Per L482, ontology files use YAML with SKOS semantics and optional EARS requirements.

### SKOS: What Concepts Exist

```yaml
concepts:
  - id: C001
    uri: aget:concept/<ConceptName>
    prefLabel: "<Human Label>"
    definition: "<Formal definition>"
    broader: [<parents>]
    narrower: [<children>]
    related: [<siblings>]
```

### EARS: What Behaviors Are Required (Optional)

```yaml
requirements:
  - id: R-DOM-001
    type: event_driven  # ubiquitous | event_driven | state_driven | optional | unwanted
    trigger: "<condition>"
    system: <SystemName>
    response: "<system> SHALL <action>"
```

## Naming Convention

```
ONTOLOGY_<domain>_v<major>.<minor>.yaml
```

## Contents

| File | Description | Concepts |
|------|-------------|----------|
| *(empty — populate with domain ontology)* | | |

## Related

- `knowledge/` — Curated domain content (instances)
- `specs/` — Requirements and design specifications

## References

- [W3C SKOS Reference](https://www.w3.org/TR/skos-reference/)
- [EARS: Easy Approach to Requirements Syntax](https://alistairmavin.com/ears/)

---

*Per PROJECT_PLAN_ontology_directory_standard_v1.0*
*Format: YAML + SKOS + EARS (L482)*
