# Advisor Domain Vocabulary

**Version**: 1.0.0
**Status**: Active
**Owner**: template-advisor-aget
**Created**: 2026-01-10
**Scope**: Template vocabulary (DRIVES instance behavior per L481)
**Archetype**: Advisor

---

## Meta

```yaml
vocabulary:
  meta:
    domain: "advisory"
    version: "1.0.0"
    owner: "template-advisor-aget"
    created: "2026-01-10"
    theoretical_basis:
      - "L481: Ontology-Driven Agent Creation"
      - "L482: Executable Ontology - SKOS+EARS Grounding"
    archetype: "Advisor"
```

---

## Concept Scheme

```yaml
Advisor_Vocabulary:
  skos:prefLabel: "Advisor Vocabulary"
  skos:definition: "Vocabulary for advisor domain agents"
  skos:hasTopConcept:
    - Advisor_Core_Concepts
  rdf:type: skos:ConceptScheme
```

---

## Core Concepts

### Recommendation

```yaml
Recommendation:
  skos:prefLabel: "Recommendation"
  skos:definition: "A suggested course of action based on analysis"
  skos:broader: Advisor_Core_Concepts
  skos:inScheme: Advisor_Vocabulary
```

### Trade_Off

```yaml
Trade_Off:
  skos:prefLabel: "Trade Off"
  skos:definition: "Comparative evaluation of competing options"
  skos:broader: Advisor_Core_Concepts
  skos:inScheme: Advisor_Vocabulary
```

### Risk_Assessment

```yaml
Risk_Assessment:
  skos:prefLabel: "Risk Assessment"
  skos:definition: "Identification and evaluation of potential negative outcomes"
  skos:broader: Advisor_Core_Concepts
  skos:inScheme: Advisor_Vocabulary
```

### Best_Practice

```yaml
Best_Practice:
  skos:prefLabel: "Best Practice"
  skos:definition: "Proven approach that produces reliable results"
  skos:broader: Advisor_Core_Concepts
  skos:inScheme: Advisor_Vocabulary
```

### Stakeholder_Context

```yaml
Stakeholder_Context:
  skos:prefLabel: "Stakeholder Context"
  skos:definition: "Understanding of who is affected by decisions"
  skos:broader: Advisor_Core_Concepts
  skos:inScheme: Advisor_Vocabulary
```

---

## Extension Points

Instances extending this template vocabulary should:
1. Add domain-specific terms under appropriate broader concepts
2. Maintain SKOS compliance (prefLabel, definition, broader/narrower)
3. Reference foundation L-docs where applicable
4. Use `research_status` for terms under investigation

---

## References

- L481: Ontology-Driven Agent Creation
- L482: Executable Ontology - SKOS+EARS Grounding
- R-REL-015: Template Ontology Conformance
- AGET_VOCABULARY_SPEC.md

---

*Advisor_VOCABULARY.md v1.0.0 — SKOS-compliant template vocabulary*
*Generated: 2026-01-10*
