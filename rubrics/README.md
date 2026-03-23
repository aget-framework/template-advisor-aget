# Rubrics

**Artifact Type**: Evaluation_Artifact (C092)
**Purpose**: Store scoring rubrics for assessing agents, artifacts, processes, and proposals.

## What Are Rubrics?

Rubrics are structured scoring frameworks that answer: **"HOW WELL does X meet Y?"**

| Artifact Type | Directory | Question |
|---------------|-----------|----------|
| Vocabulary_Artifact | `ontology/` | "What IS X?" |
| Specification_Artifact | `specs/` | "What MUST X do?" |
| Procedure_Artifact | `sops/` | "HOW to do X?" |
| **Evaluation_Artifact** | `rubrics/` | "HOW WELL?" |

## Creating Rubrics

See `sops/SOP_RUBRIC_CREATION.md` for the creation process.
Use `rubrics/RUBRIC.template.md` as the canonical template.

For fleet-wide rubric design lessons, see `docs/patterns/PATTERN_rubric_design_principles.md`.

## Rubric Structure

Each rubric includes:
- **Archetype**: Compliance, Decision, or Meta
- **Eligibility Gates**: Binary prerequisites before scoring
- **Dimensions**: Major evaluation categories (Quality or Maturity)
- **Performance Levels**: L0-L3 with domain-appropriate labels
- **Scoring Method**: How to aggregate scores

## Rubrics in This Directory

| Rubric | Domain | Version |
|--------|--------|---------|
| *(none yet — create your first rubric using the template)* | | |

---

*Evaluation_Artifacts: Measuring how well things meet standards.*
*Convention: C092 (ONTOLOGY_scoring_rubric_v1.0.yaml)*
