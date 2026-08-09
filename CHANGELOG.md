# Changelog

All notable changes to AGET will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).




## [3.30.0] - 2026-08-09 - "Portable Skills, Continuous Cadence"

### Added
- Added a bounded, digest-addressed Agent Skills package with a shipped conformance validator and documented manual cross-client use.

### Changed
- Changed Agent Skills frontmatter to the current specification shape for the packaged subset.

### Documentation
- Documented that hooks, permissions, release gates, and structural enforcement do not travel with the package.

## [3.29.0] - 2026-08-01 - "Repair release truth and reduce principal decision work"

### Added
- Added Codex-native discovery for wake-up, study-topic, and save-state with explicit recovery.
- Added exact Claude Code and Codex CLI control-conformance evidence plus a one-view release decision contract.

### Changed
- Changed study-topic ranking so purpose weighting is effective and recency, searched surfaces, and external omissions are disclosed.

### Fixed
- Fixed distribution evidence so producer, distribution point, received state, and downstream behavior remain independent predicates.

## [3.28.0] - 2026-07-26 - "Make the gates fire"

**Release class**: governance-hardening — inward-facing. Expect changed *gate behaviour*, not new features.

### Changed
- Theme: enforcement that fires without being invoked. The release-gate battery gains a forced firing point at the irreversible act (tag / `push --tags` / `push --follow-tags`), and the Phase 7.1.5 release-quality score must carry a resolvable **independent** verification leg — a producer-run score no longer settles its own gate. Triage freshness becomes a measured SLO whose rollup detects *rollup-without-triage*, so measuring the queue cannot substitute for working it.

### Fixed
- Release metadata dates were never bumped: `version_bump.py` moved version strings but left `codemeta.json:dateModified` and `CITATION.cff:date-released` stale (3.27.0 shipped 07-18 carrying 07-11 dates).
- `study_topic.py` advertised the specification tier in its printed search contract while never searching it — every study reported zero specs (*manufactured absence*, not omission).
- Release-metric issue counts saturated at a page cap and recorded `0` on API failure, making a failed count indistinguishable from zero.
- The contract suite could not pass its own 60s pre-release timeout (528s, with 81% of runtime in three tests that re-ran the whole battery).

### Governance
- Test-requirement traceability: the 80% figure was a never-met pilot aspiration; replaced by a ratified floor at the measured **39%**, rising +5pp per minor release — a bar that blocks regression rather than blocking everything.
- Release-gate scope made explicit: **release-integrity** failures block a tag absolutely; **codebase-quality** debt is reported with a named owner and does not block.

## [3.27.0] - 2026-07-18 - "Finish & Verify"

### Changed
- Theme: the portfolio learns to FINISH (EC tick-state maintained signal CIS-010; CIS-008 Achieve-only re-spec; NASCENT typing backfill; L-doc ID injectivity remediation L1200-L1209 + tombstone registry) and the release learns to VERIFY what it shipped runs (migration Rung-4 behavioral verification + mandatory Behavioral Smoke; 3-axis tag-payload coherence [14 origins x tagged-tree paths x executed-surface]; single Corrections-since-tag surface; DoD ID-axis row-completeness ratchet; public-graph coherence joins computed DoD; verify-before-claim coverage matrix). Also: Transactional Execution doctrine + workspace convention in all template AGENTS.md; universal-skill conformance 14/14 (core + document-processor backfilled); single-slash permission-rule detector; dual-status mask scanner; wind-down double-fire guard; delegated-prompt date contract; Filing_Candidate L-doc marker standard.

## [3.26.0] - 2026-07-11

**Theme**: Signals & Contracts

- `wake_up.py` release-currency signal — session start reports when the local framework version is behind the latest release; silent when current (fail-soft).
- `health_check_ext.py` + `study_topic_ext.py` extension hooks — instance customization without forking Framework_Artifacts.
- `study_topic.py` search contract: surface manifest in output, keyword hygiene, token-boundary matching, ranking floor, `inbox/` surface joined.
- `/aget-close-project`: C-CLOSE-007 (closer mutates scaffold in place) + C-CLOSE-008 (has-it-run gate — executable deliverables need execution evidence pre-COMPLETE).
- Three-state check contract (PASS / FAIL / UNREACHABLE) + terminal-state vocabulary + verify-before-claim coverage matrix (canonical `docs/CONVENTION_*.md`).
- Fixes: `wake_up.py` session-glob case-fold; `check_skill_reliance_manifest.py` archetype-index paths; `close_gate_check.py` independence-WARN restore.

## [3.25.0] - 2026-07-04

**Theme**: Grounded Entities & Trusted Releases

- aget-ask production v1.0.0 (SKILL-045 + spec) — entropy-reducing clarification/followup with altitude filter.
- `study_topic.py`: active-plan detection fixed (case-insensitive, Plan_Status-first — live plans no longer render inactive) + knowledge/+ontology/ search areas.
- `capture_friction.py`: ledger entries carry a value-class (`owed` pending-triage default, CAP-FRIC-006).
- `wake_up.py`/`health_check.py`: reliance self-attestation (R-BND-001-03) + permission-accumulation gate.
- `close_gate_check.py`: closure-substance detection + release-close DoD guard wiring.
- Conformance model: reliance-only (D-1) — canonical-specs reference line added to AGENTS.md; no spec copies shipped.

## [3.22.0] - 2026-06-13

**Theme**: Skill-Support Delivery + Verify-at-Point-of-Use + Hygiene

- Framework version sync to 3.22.0. `/aget-propose-actions` skill updated to **v1.8.0** (Step 3.5 Self-Critique 10-point checklist + Type column; also clears accumulated v1.7.x propagation lag). New framework gates (`deploy_skill.py`, `check_claim_freshness.py`, `check_skill_coherence.py`, `validate_spec_binding.py`) are available in canonical `aget/scripts/` — copy as needed. No breaking changes.

## [3.21.0] - 2026-06-06

**Theme**: Always-On Fleet Operations (governance-scoped)

- Framework version sync to 3.21.0. No template content change (governance scaffolding for unattended operation lands in the canonical framework; see aget/CHANGELOG.md).

## [3.20.3] - 2026-05-31

- C-P3 health-check correctness fix (`check_structural_skill_frontmatter`) propagated to template consumer surface.

## [3.20.2] - 2026-05-31

- Consumer-surface delivery: C-F1/C-P1/C-P3 health & config checks delivered to templates.

## [3.20.0] - 2026-05-30

- Framework version sync to 3.20.0.

## [3.19.0] - 2026-05-23

- Framework version sync to 3.19.0.

## [3.18.0] - 2026-05-16

**Theme**: Aligned with framework v3.18.0 (Substrate Hygiene + Memory-Layer Self-Application; Hybrid A primary + B-tagged streams)

### Changed

- Version bump: 3.17.0 → 3.18.0 (framework alignment)
- `.aget/version.json` `aget_version` updated to 3.18.0

### Framework v3.18.0 Highlights

- `AGET_MEMORY_SURFACE_SPEC v0.2.0` canonical promotion (T1.16 + T2.37) — harness-vs-KB taxonomy formalized
- Verb Registry Currency (T1.9 = PP-021) — 37 Active + 4 Reserved verbs + 11 §Hierarchy Decisions pairs
- `/aget-create-initiative` Strict promotion (T2.46) — D71 verb-pair gap closed
- Homepage Fork C Hybrid (T1.12) — L941-L944 cluster closed structurally
- L908 family memory-layer closure (L960 + L963 + L964 graduated)

See [framework v3.18.0 release notes](https://github.com/aget-framework/aget/releases/tag/v3.18.0) for full details + DEFECT-2/4 acknowledgment.

---

## [3.17.0] - 2026-05-09

**Theme**: Aligned with framework v3.17.0 (Theme C3 — Canonical Coherence + Structural Self-Conformance)

### Changed

- Version bump: 3.16.0 → 3.17.0 (framework alignment)
- `AGENTS.md` `@aget-version` updated to 3.17.0
- Inherits framework v3.17.0 deliverables: framework-manager archetype formalization (Q4=A.2 disposition); T2.18 SOP_scope_lock_ceremony LANDED v1.0.0; T2.19 AGET_SKILL_LIFECYCLE_SPEC LANDED v1.0.0 with full V-test authoring; T2.20 AGET_FLEET_UPGRADE_SPEC v0.1 DRAFT; T2.23 AGET_TASK_ROUTING_SPEC v0.1 DRAFT.
- CAP-REL-030 + CAP-REL-031 (post-release CHANGELOG + tag validators) IMPLEMENTED (closes v3.16 sleeping CAPs); CAP-REL-032 + CAP-REL-033 grace-extended to v3.18.0 per Q1=B disposition.

### Compatibility

- **No breaking changes** in v3.17. Existing instances upgrade by version-bump only.
- Optional adoption: `framework-manager` archetype field in `.aget/identity.json`; existing `archetype` values continue to function.

---

## [3.16.0] - 2026-05-02

**Theme**: Aligned with framework v3.16.0 (Framework-Discipline Closure + Wave-1A Spec Contracts + /aget-go Production)

### Changed

- Version bump: 3.15.0 → 3.16.0 (framework alignment)
- `AGENTS.md` `@aget-version` updated to 3.16.0
- **Universal-skills migration (#1120)**: 15 missing universal skills added from worker baseline (advisor/analyst/architect/consultant/developer/executive/operator/researcher/reviewer/spec-engineer pre-bump count 19 → post-migration 34, then post-archetype-fit-revert 31 = 29 universal + 2 archetype-specific).
- **Release-triad revert (CAP-TPL-016-07 NEW)**: 3 release-triad skills (`aget-release-build`, `aget-release-audit-specs`, `aget-release-critique`) removed from this template — moved to release-execution archetype catalog (worker, supervisor only). Closes the "presence-not-fit" misfit surfaced by Gate 1 defects audit.

### Compatibility

- **No breaking changes** in v3.16. Existing instances upgrade by version-bump only.
- Optional adoption: `**Plan_Status**:` / `**Gate_Status:**` schema in new PROJECT_PLAN files (CAP-PP-003 disambiguation; backward-compatible).

---

## [3.15.0] - 2026-04-25

**Theme**: Aligned with framework v3.15.0 (Two-Level Model Coherence + Security Hardening)

### Changed

- Version bump: 3.14.0 → 3.15.0 (framework alignment)
- `AGENTS.md` `@aget-version` updated to 3.15.0

### Breaking

- **BC-001**: `.aget/version.json` old field names removed (e.g. `agent_name` → `aget_agent_name`). See `aget/docs/BREAKING_CHANGES_v3.15.md`.
- **BC-002**: `--fix` flag removed from `/aget-check-health` (SKILL-003). Use `/aget-enhance-health` instead.

---

## [3.14.1] - 2026-04-18

### Fixed

- `installer/install.py`: reference `scripts/health_check.py` (was stale `scripts/housekeeping_protocol.py` from partial #979 propagation). Restores CI green; `test_enhanced_installer.py` assertions satisfied. See `aget-framework/aget/CHANGELOG.md` v3.14.1 for framework-level context.

---
## [3.14.0] - 2026-04-18

**Theme**: Aligned with framework v3.14.0 (v3.13 Loop Closure + Scope-Lock Discipline)

### Changed

- Version bump: 3.13.0 → 3.14.0 (framework alignment)
- `AGENTS.md` `@aget-version` updated to 3.14.0

### Fixed

- Installer template: `housekeeping_protocol.py` → `health_check.py` rename propagation (#979)

### Notes

Per-template CHANGELOG entries for 3.12.0 and 3.13.0 were not individually maintained; template work in those cycles is captured in `aget-framework/aget/CHANGELOG.md`. Gap flagged for v3.14.x / v3.15 retrospective.

---

## [3.11.1] - 2026-04-04

### Changed

- Renamed `aget_housekeeping_protocol.py` → `health_check.py`
- Renamed `study_up.py` → `study_topic.py`
- Config key `skip_sanity` → `skip_health_check`

---
## [3.11.0] - 2026-03-28 - "Skill Conformance, Requirements & Hooks"

### Added

- **requirements/** directory scaffolded (L742 two-level model, #725)
- **.claude/hooks/** directory with README (ADR-008 Generator, #505)
- **governance_intensity** field in AGENTS.md (#732)

### Changed

- 17 skill SKILL.md files updated for L736 conformance (SICR, #678)
- "sanity check" → "health check" terminology (#658)
- RUBRIC.template.md v2.0 deployed

---

## [3.10.0] - 2026-03-21 - "Structural Enforcement"

### Added
- MUST-invoke directives for /aget-create-project and /aget-file-issue (D71)
- Gate Boundary Protocol: plan update + commit as structural proof of gate completion
- Skill Completion Signal pattern in /aget-create-project and /aget-enhance-spec
- SOP Phase -0.5: Content Sync governance (D69/GOV-040)
- SKILL_SPEC_TEMPLATE.yaml (#439)

### Changed
- Skill renames: aget-capture-observation → aget-record-observation, aget-capture-nugget → aget-record-nugget, aget-study-up → aget-study-topic (#480)
- `capture` verb retired from Learning family
- Gate Execution Discipline strengthened with MUST update + MUST commit

### Fixed
- Template hygiene: VERSION, classifier, SECURITY.md corrections (#574)

## [3.9.0] - 2026-03-15 - "Governance Enforcement"

### Added
- Gate 0: Spec Verification (MP-1) in project plan template
- Phase -1: Release Readiness governance in SOP

### Changed
- Version bump to v3.9.0 (5/5 artifact types)
- version_bump.py: extended to cover AGENTS.md, codemeta.json, CITATION.cff
- TEMPLATE_PROJECT_PLAN.md: mandatory Gate 0 added

### Fixed
- aget-enhance-spec: Phase 6 consistency (#418), phantom spec reference (#419)

 - 2026-03-08 - "Governance Maturation"

### Added
- AGENTS.md governance patterns: capability declarations, CLI feature adoption guidance
- `.claude/` scaffolding: settings.json, skills directory structure
- Skill: `aget-expand-ontology` v1.0.0 (optional, acquirable)
- Skill: `aget-enhance-spec` v1.1.0 (specification enhancement lifecycle)

### Changed
- Version bump to v3.8.0
- identity.json: `type` field added
- SOP headers: CAP-SOP-001 compliance
- Migration history entry added

### Notes
- See aget/CHANGELOG.md [3.8.0] for framework changes
- Part of Governance Maturation release (principle codification, deliverable conformance)

---

## [3.7.0] - 2026-03-05 - "Quality Reconciliation"

### Added
- AGENTS.md governance patterns backported (TEMPLATE_AGENTS_MD_SPEC v1.0.0)
- `.claude/` directory scaffolding for CLI feature adoption

### Changed
- Skill renames: `aget-studyup` → `aget-study-up`, `aget-healthcheck-*` → `aget-check-*`
- README positioning: evidence-based reframe, removed undemonstrated claims
- Version bump to v3.7.0
- Migration history entry added

### Notes
- See aget/CHANGELOG.md [3.7.0] for framework changes
- Part of Quality Reconciliation release (content integrity, SOP lifecycle, positioning reframe)

---

## [3.6.0] - 2026-02-21 - "Infrastructure Maturation"

### Added
- Universal skill: `aget-studyup` (focused KB research before implementation)
- Canonical script: `scripts/study_up.py`

### Changed
- Platform claims: "Claude Code, Codex CLI, Gemini CLI" (was "Claude Code, Cursor, Aider, Windsurf")
- Version bump to v3.6.0
- Migration history entry added

### Notes
- See aget/CHANGELOG.md [3.6.0] for framework changes
- Part of Infrastructure Maturation release (observability, content integrity, ontology)

---

## [3.5.0] - 2026-02-14 - "Archetype Customization"

### Added
- Archetype-specific skills: `aget-assess-risk`, `aget-recommend-action`
- Formal ontology: `ontology/ONTOLOGY_advisor.yaml` (6 concepts, 2 clusters)
- Universal skill: `aget-file-issue` (14th universal)
- Evaluator-focused README narrative

### Changed
- SKILL_VOCABULARY.md v1.2.0 with SKOS reference
- README structure: "Why Advisor?" value proposition

### Notes
- See aget/CHANGELOG.md [3.5.0] for framework changes
- Part of Archetype Customization release

---

## [3.4.0] - 2026-01-18 - "Session Skills Maturity"

### Added
- Session protocol enhancements (re-entrancy guard, calendar awareness)
- Template infrastructure: `sops/SOP_escalation.md`

### Changed
- Cross-CLI validation (Claude Code, Codex CLI, Gemini CLI)
- Governance formalization patterns

### Notes
- See aget/CHANGELOG.md [3.4.0] for framework changes

---

## [3.3.0] - 2026-01-11 - "Framework Alignment"

### Changed
- Updated to AGET framework v3.3.0
- Aligned with Shell Integration + Executable Knowledge Ontology release

### Notes
- See aget/CHANGELOG.md for framework changes
- L517 remediation: Template_Abandonment closure

---


## [3.2.1] - 2026-01-04 - "Version Inventory Coherence"

### Fixed
- **Version Consistency**: AGENTS.md, manifest.yaml, version.json now all show v3.2.1
- Part of L444 remediation (version inventory coherence)

### Notes
- Patch release to fix version inconsistencies from v3.2.0
- See aget-framework/aget CHANGELOG [3.2.1] for details

---

## [3.2.0] - 2026-01-04 - "Specification Architecture"

### Added
- Version sync with aget core v3.2.0

### Changed
- Version references updated across all files

### Notes
- Part of AGET v3.2.0 "Specification Architecture" coordinated release
- See aget-framework/aget CHANGELOG for full framework changes:
  - 7 new specifications
  - Naming conventions expanded (4 → 10 categories)
  - 6 new validators
  - INDEX.md + REQUIREMENTS_MATRIX.md

---

## [3.1.0] - 2026-01-04 - "Session Protocol Enhancements"

### Added
- **Complete Session Lifecycle Scripts**:
  - `wake_up.py`: Session initialization (R-WAKE-001 to R-WAKE-007)
  - `aget_housekeeping_protocol.py`: Mid-session sanity checks (R-SANITY-001 to R-SANITY-007)
  - `wind_down.py`: Session close with sanity gate (R-WIND-001 to R-WIND-006)
- **Cross-CLI Automation**: All scripts support `--json` output for Claude Code, Codex, Cursor

### Changed
- Version references updated across all files (manifest.yaml, identity.json, AGENTS.md)
- Scripts implement L038 (Agent-Agnostic) and L021 (Verify-Before-Modify)
- Pattern versions: session 1.2.0, housekeeping 1.1.0

### Notes
- Part of AGET v3.1.0 coordinated release
- See aget-framework/aget CHANGELOG for full framework changes

---

## [3.0.0] - 2025-12-28 - "5D Composition Architecture"

### Added
- **5D Directory Structure**: Organized agent composition
  - `.aget/persona/` - Identity and behavioral characteristics
  - `.aget/memory/` - Session handoffs and persistent state
  - `.aget/reasoning/` - Decision frameworks and policies
  - `.aget/skills/` - Patterns, SOPs, and automation scripts
  - `.aget/context/` - Environmental and domain information
- **v3.0 Contract Tests**: Updated test suite with SKIP_TEMPLATE_V2 pattern

### Changed
- `template` field replaces `roles` array
- `instance_type` field: `template` for templates, `aget`/`AGET` for instances
- `archetype` field: high-level classification
- Manifest version: 3.0

### Migration
- See `docs/FLEET_MIGRATION_GUIDE.md` in aget-framework/aget

---

## [Unreleased] - Knowledge Template Component

### Added
- **Knowledge Directory Template** (L296):
  - `aget/components/knowledge/README_TEMPLATE.md` - Canonical template for domain beliefs
  - `knowledge/README.md` - Pre-configured in template root
  - Placeholder structure with `{domain}/patterns/`, `{domain}/heuristics/`, `thresholds/`

- **Knowledge Capture Protocol**:
  - L296 portability test ("Clone to different domain. Still useful?")
  - Validation states: Hypothesis → Validated → Established
  - Capture triggers: session end, discovery, decision

- **Migration Guide**:
  - `docs/KNOWLEDGE_MIGRATION_GUIDE.md` - For existing agents
  - Detection, migration steps, verification checklist

### Changed
- Updated AGENTS.md Directory Structure to include `knowledge/`
- Added Knowledge Capture (L296) subsection to template configuration

---

## [2.10.0] - 2025-12-13 - "Capability Composition Architecture"

### Added
- **Capability Composition Architecture compatibility**
  - Framework now supports `capabilities[]` array in version.json
  - Agents can compose multiple capabilities onto base templates
  - See L330 (Capability Composition Architecture) for details

- **Theoretical Grounding Protocol** (L332)
  - Specifications should include `theoretical_basis:` sections
  - Maps AGET concepts to established theory (BDI, Actor Model, Cybernetics)

### Changed
- Version bump for v2.10.0 framework alignment

### Coming in v2.11.0
- CAPABILITY_SPEC_v1.0.yaml (formal capability schema)
- TEMPLATE_MANIFEST_SPEC_v1.0.yaml (composition declaration)
- capability-domain-knowledge implementation
- capability-structured-outputs implementation

### Notes
- **No structural changes required** for v2.10.0 compatibility
- Templates remain valid bases for capability composition
- v2.10.0 = Architecture defined | v2.11.0 = Architecture implemented

## [2.9.0] - 2025-11-23 - "Information Storage Standardization"

### Added
- **Layer 4 (.memory/) for Advisors**:
  - `.memory/` directory for advisor relationship state (Layer 4)
  - `.memory/clients/` for client context and relationship tracking
  - `.memory/engagements/` for engagement scope and progress tracking
  - `.memory/README.md` with comprehensive usage guidelines

- **Contract Tests (6 new tests)**:
  - `test_memory_directory_exists()` - Validates .memory/ structure
  - `test_memory_clients_directory_exists()` - Validates clients/ subdirectory
  - `test_memory_engagements_directory_exists()` - Validates engagements/ subdirectory
  - `test_sessions_at_root()` - Validates sessions/ location (not .aget/sessions/)
  - `test_agents_md_documents_memory()` - Validates .memory/ documentation
  - `test_memory_readme_exists()` - Validates usage guide presence

### Changed
- **AGENTS.md Updates**:
  - Added `.memory/` to Directory Structure (Layer 4 documentation)
  - Added `.memory/ Directory (Layer 4 - Advisors Only)` section
  - Documented .memory/ boundary rules and usage guidelines
  - Added `sessions/` to directory structure (v2.9 standard location)
  - Size: 31,854 → 34,719 characters (+2,865 bytes)

### Migration Notes
- **New instances**: .memory/ structure included by default
- **Existing instances**: Add .memory/ during v2.9 migration
  - Create `.memory/clients/` and `.memory/engagements/` directories
  - Add `.memory/README.md` from template
  - Update AGENTS.md with Layer 4 documentation
  - Run contract tests to validate compliance

### Related
- **Fleet Migration**: Part of v2.9 Final Release (Information Storage Standardization)
- **Specification**: 5-layer architecture (Framework, Agent Type, Instance, Memory, Domain)
- **Validation**: `validate_fleet_standards.py` checks Layer 4 compliance

## [2.8.0] - 2025-11-08 - "Planning & Infrastructure"

### Added
- **Planning Framework v1.0**:
  - Decision tree for choosing planning approach
  - 5 templates: Enhancement, Gate, Project, Checkpoint, Critique
  - Integration with L274 (OKR), L275 (Multi-Gate), L42 (Gate Discipline)

- **Enhancement Filing Protocol**:
  - Systematic protocol for filing framework improvements
  - 5-section structure (Problem, Context, Solution, Benefits, Estimate)
  - Generalizability criterion (3+ agents benefit)

- **GitHub Tooling Improvements**:
  - Interactive issue filing (`make issue`)
  - Type taxonomy error handling
  - --learning flag for automatic learning document creation

### Changed
- Feature 10: Framework artifact consolidation to .aget/docs/releases/
- Naming conventions: Prefix meanings (private-/public-/my-) formalized

### Documentation
- Planning Guide v1.0 (comprehensive planning decision support)
- Enhancement Filing Protocol v1.0
- Naming Prefix Convention v1.0
- Planning Protocol Examples (14 examples)

### Compatibility
- Fully backward compatible with v2.7
- New planning templates optional (existing approaches still work)

## [2.7.0] - 2025-10-13 - "Portfolio Governance"

### Added
- **Portfolio Governance System**:
  - Portfolio field in version.json for organizational grouping
  - Portfolio-aware advisory operations
  - Classification support for sensitive engagements
  - Security boundary enforcement for advisor agents

- **Organizational Memory Patterns**:
  - Enhanced learning document structure (L51)
  - Standardized session metadata (v1.0)
  - Cross-agent knowledge sharing for advisors

- **Learning Discovery Framework**:
  - Systematic learning capture from advisory sessions
  - Learning reference validation tools
  - Advisory insight documentation templates

### Changed
- Enhanced wake protocol with portfolio awareness
- Updated identity protocol to include portfolio field
- Improved advisory session documentation

### Documentation
- Portfolio manifests guide for advisor deployments
- Learning document standard (v1.0)
- Session metadata standard for advisory work

### Compatibility
- Backward compatible with v2.6
- New portfolio field optional (defaults to null)
- Existing advisor agents work without portfolio assignment

## [2.6.0] - 2025-10-11 - "Configuration Management"

### Added
- **Configuration Size Management**:
  - 40,000 character limit for AGENTS.md (L146)
  - Size monitoring for persona-rich configurations
  - Content extraction strategies for advisor configs

- **Framework Positioning**:
  - Clarified advisor role in AGET ecosystem
  - Updated positioning vs autonomous advisors
  - Landscape analysis for advisory agents

- **Contract Test Validation**:
  - Enhanced 30-test suite for advisor boundaries
  - Read-only validation improvements
  - Persona protocol compliance testing

### Documentation
- Configuration size management for advisors
- Framework positioning analysis
- Advisor-specific best practices

### Compatibility
- Fully backward compatible with v2.5
- No breaking changes to advisor contracts

## [2.5.0] - 2025-10-06 - "Validation"

### Added
- **Contract Testing Framework**:
  - 30 comprehensive contract tests (advisor-specific)
  - Automated validation of advisory boundaries
  - Persona protocol testing
  - Read-only enforcement validation

- **Identity Protocol**:
  - Standardized agent_name field (must match directory)
  - Fixed instance_type: "aget" (advisory agents)
  - Domain field for advisory specialization
  - Persona field (teacher/mentor/consultant/guru/coach)

- **Validation Framework**:
  - Advisory boundary verification
  - Version compliance checking
  - Persona configuration validation
  - Deployment verification standards (L93)

### Documentation
- Testing guide for advisor agents
- Contract test documentation (30 tests)
- Identity protocol standards
- Persona differentiation guide

### Compatibility
- Backward compatible with v2.4
- All new advisor agents must pass 30 contract tests
- v2.5.0 established as advisor version floor

## [2.4.0] - 2025-10-03 - "Naming Conventions"

### Added
- **Naming Convention Standard**:
  - Suffix-based capability signaling (advisor-aget pattern)
  - Template naming convention (template-advisor-aget)
  - Visual consistency with framework templates

- **Organizational Grouping**:
  - aget_group field in version.json
  - Organization migration to aget-framework
  - Repository standardization for advisors

### Changed
- Repository follows template-advisor-aget pattern
- Template organization moved to aget-framework
- Advisory template distinguished from worker template

### Documentation
- Naming convention guide for advisors
- Organization structure documentation
- Migration guide from v2.3

### Compatibility
- Backward compatible with v2.3
- Old repository URLs redirect automatically

## [2.3.0] - 2025-10-02 - "Collaboration"

### Added
- **Pattern Versioning System**:
  - `.aget/patterns/versions.yaml` - Semantic versioning for all 24 patterns
  - `.aget/tools/bump_pattern.py` - Version bump automation
  - `.aget/tools/check_pattern_compatibility.py` - Compatibility validation
  - `docs/PATTERN_VERSIONING.md` - Complete versioning guide

- **Session Metadata System**:
  - `.aget/schemas/session_metadata_v1.0.yaml` - YAML schema for session frontmatter
  - `.aget/schemas/session_metadata_v1.0.json` - JSON schema for validation
  - `.aget/tools/generate_session_metadata.py` - Metadata generation tool
  - `.aget/tools/validate_session_metadata.py` - Schema validation tool
  - `docs/SESSION_METADATA_MIGRATION_GUIDE.md` - Migration instructions

- **Specification Framework**:
  - `.aget/docs/SPEC_FORMAT_v1.1.md` - EARS-based specification format
  - Support for formal capability documentation with aerospace patterns
  - Four maturity levels: bootstrapping, minimal, standard, exemplary

### Changed
- Session pattern upgraded to v1.1.0 (session metadata support)
- Version file now tracks collaboration features

### Documentation
- Complete guides for all v2.3 features
- Migration path from v2.2 to v2.3
- Pattern versioning best practices

### Compatibility
- Not backward compatible with v2.2 (breaking changes)
- Requires pattern versioning system
- Requires session metadata schema v1.0
- AGETs must update to v2.3 for ecosystem compatibility

## [2.1.0] - 2025-09-28

### Added
- **Clear File Ownership Standard**:
  - Framework scripts now use `aget_` prefix for clear identification
  - Added `.aget/OWNERSHIP.md` guide for developers
  - Migration script `aget_v21_migration.py` for upgrading existing projects

- **Release Quality Tools**:
  - `aget_check_permissions.py` - Comprehensive file permission validator
  - `aget_pre_release.sh` - Pre-release checklist automation
  - Both tools ensure template quality before releases

### Changed
- Renamed framework scripts with `aget_` prefix:
  - `check_file_permissions.py` → `aget_check_permissions.py`
  - `pre-release.sh` → `aget_pre_release.sh`
  - Existing `housekeeping_protocol.py` and `session_protocol.py` already use prefix

### Documentation
- Added ownership standard documentation
- Created migration guide for v2.0 → v2.1
- Updated installer to respect new naming convention

### Compatibility
- Maintains backward compatibility with v2.0
- Symlinks preserved for legacy script names
- Non-breaking changes for existing agents

## [2.0.0-beta.1] - 2025-09-24

### Gate 3: Migration Tools - Scaffolding System

#### Added
- **Template-based Scaffolding System**:
  - Five templates: `minimal`, `standard` (default), `agent`, `tool`, `hybrid`
  - `aget init --template <type>` creates appropriate directory structure
  - Auto-generates README.md files in key directories
  - Template-specific .gitignore patterns
  - Version tracking includes template information

- **Directory Structure Improvements**:
  - Renamed `outputs/` → `workspace/` (private exploration)
  - Renamed `Outputs/` → `products/` (public products)
  - Fixes case-sensitivity issues on macOS/Windows
  - Clear vocabulary distinction between private and public

- **Template Features**:
  - **Minimal**: Basic .aget/ and AGENTS.md only
  - **Standard**: Adds workspace/ and data/ directories
  - **Agent**: Full structure with checkpoints, src, tests, docs
  - **Tool**: Focused on products/ without workspace/
  - **Hybrid**: Combines agent and tool with examples/

#### Testing
- 13 new scaffolding tests covering all templates
- Validates directory creation, README generation, and configuration

#### Documentation
- Added comprehensive [SCAFFOLDING.md](docs/SCAFFOLDING.md)
- Updated vocabulary throughout codebase
- Clear migration path from v1 naming conventions

## [2.0.0-alpha.2] - 2025-09-24

### Gate 2: Pattern Library Complete

#### Added
- **Pattern Library Foundation** with PatternRegistry for discovery and loading
- **8 Reusable Patterns**:
  - `session/wake` - Wake up protocol with git status and pattern detection
  - `session/wind_down` - Save work with commits, notes, and tests
  - `session/sign_off` - Quick save and exit without prompts
  - `housekeeping/cleanup` - Remove temp files, caches, build artifacts
  - `housekeeping/doc_check` - Assess documentation quality (A-F grades)
  - `bridge/extract_output` - Transform agent outputs to public products
  - `housekeeping/migration_cleanup` - Clean migration artifacts (existing)
  - `meta/project_scanner` - Scan projects for AGET readiness (existing)

#### Enhanced
- `aget init` now creates:
  - `outputs/` directory for agent workspace
  - `data/` directory for persistent storage
  - `.aget/evolution/` for tracking insights
  - Updated AGENTS.md template with vocabulary reference

- `aget apply` command:
  - Lists all available patterns
  - Applies patterns to projects
  - Provides helpful error messages
  - Performance <2 second requirement met

#### Testing
- Comprehensive test suites for all patterns
- 54 tests passing
- Test-first development approach
- Performance validation (<2s requirement)

## [2.0.0-alpha.1] - 2025-09-24

### Gate 1: Core CLI Foundation

#### Added
- `aget init` command with three-tier degradation (gh/git/filesystem)
- `aget rollback` command for safe configuration rollback
- Base command architecture for future expansion
- Test theater with quality agent architecture

#### Changed
- Unified v2 vision combining CLI tool with framework concepts
- Vocabulary distinction: outputs (private) vs Outputs (public)
- Naming convention: aget-* (framework), *-aget (agents)

## [1.0.0] - 2025-09-22

### Initial Release

#### Added
- Universal agent configuration via AGENTS.md
- Session management protocols (wake, wind down, sign off)
- Housekeeping protocols (cleanup, documentation check)
- Template installer with three tiers (minimal, standard, advanced)
- Support for multiple AI coding assistants
- Cross-platform compatibility (Mac, Linux, Windows)

---

*For detailed migration instructions from v1 to v2, see [UPGRADING.md](docs/UPGRADING.md)*