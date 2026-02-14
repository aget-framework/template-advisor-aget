# Aget Advisor Template

> **Read-only advisory agents with persona-based guidance**

Transform any domain into an AI advisor that provides expert guidance without modifying systems. Supports 5 distinct personas: teacher, mentor, consultant, guru, and coach.

**Current Version**: v3.5.0 "Archetype Customization"

---

## What This Is

**Not an action-taking agent** - Advisor agents operate in read-only mode, providing recommendations, analysis, and guidance without executing changes.

**Mental Model**:
```
You → Question → AI Advisor → Analyzes Context → Recommends (with confidence + assumptions)
```

Your advisor reads, analyzes, critiques, and recommends - but never modifies files, executes commands with side effects, or takes action on your behalf.

---

## Quick Start (3 Minutes)

### 1. Clone and Configure

```bash
# Create your advisor instance
git clone https://github.com/aget-framework/template-advisor-aget.git my-domain-advisor-aget
cd my-domain-advisor-aget
```

### 2. Choose Your Persona

Pick the persona that matches your advisory style:

| Persona | Focus | Best For |
|---------|-------|----------|
| **teacher** | Instruction & learning | Explaining concepts, structured education |
| **mentor** | Growth & development | Career guidance, reflective questions |
| **consultant** | Solutions & analysis | Trade-off analysis, decision support |
| **guru** | Expertise & principles | Best practices, authoritative guidance |
| **coach** | Performance & improvement | Code reviews, incremental feedback |

Edit `.aget/version.json`:
```json
{
  "agent_name": "my-domain-advisor-aget",
  "persona": "consultant",  // ← Set your persona here
  "domain": "system-architecture"  // ← Your specialty area
}
```

### 3. Start Advising

```bash
# Open with your AI assistant
claude .
```

```
You: hey

AI: my-domain-advisor-aget v2.5.0 (Advisor)
    🎭 Mode: ADVISORY (recommendations only)
    👤 Persona: consultant
    📖 Domain: system-architecture

    🚫 Read-only: Cannot modify files or execute commands
    ✅ Can: Analyze, recommend, critique, guide

    Ready for questions.

You: Should I use microservices or monolith for this project?

AI: As advisor: Let me understand your context first.

    **Clarifying questions**:
    - What's your team size and experience level?
    - What's your deployment cadence target?
    - What are your scaling requirements?
    - What's your operational maturity?

    [After your answers...]

    **Recommendation** (Confidence: Medium)

    Based on [team size: 5], [cadence: monthly], [maturity: low]:

    ➡️  Start with modular monolith

    **Reasoning**:
    - Simpler deployment model matches team capacity
    - Monthly cadence doesn't require independent service releases
    - Low operational maturity = microservices overhead risky

    **Trade-offs**:
    - ✅ Faster initial development
    - ✅ Lower operational burden
    - ⚠️  Will require refactoring if scaling becomes issue
    - ❌ Less independent team scaling

    **Assumptions**:
    - Team staying stable (<10 people) for next 12 months
    - Performance requirements met by vertical scaling
    - No regulatory requirements for service isolation

    **Would change recommendation if**:
    - Team growing rapidly (>15 people in 6 months)
    - Performance hotspots identified requiring independent scaling
    - Multiple products requiring independent release cycles

You: wind down

AI: [Commits session notes with advisory context]
```

---

## What Advisors Can Do

### ✅ Advisory Capabilities

- **Analyze** - Read files, examine codebases, assess quality
- **Recommend** - Suggest approaches with confidence levels and assumptions
- **Critique** - Provide specific, actionable feedback with evidence
- **Guide** - Walk through concepts, answer questions, provide resources
- **Compare** - Present options with trade-offs and context
- **Explain** - Break down complex topics with structured learning
- **Assess** - Evaluate quality, maturity, readiness

### 🚫 What Advisors Cannot Do

- **Modify files** - No Edit, Write, or file modification tools
- **Execute commands** - No Bash with side effects (can read-only inspect)
- **Create artifacts** - Cannot write code, configs, or documentation
- **Take action** - Cannot merge PRs, deploy systems, or change state

**Enforcement**: 4 layers
1. **Declarations** - `instance_type: "aget"` in version.json
2. **Contract tests** - 16 automated tests validate read-only boundaries
3. **Documentation** - AGENTS.md protocols guide behavior
4. **Human oversight** - You verify advisor stays in role

---

## Supported Personas

Each persona provides the same technical capabilities but with different communication styles:

### 🎓 Teacher
**Focus**: Instruction and structured learning
**Style**: Didactic, explanatory, comprehensive examples
**Best for**: Learning new concepts, understanding fundamentals

**Example interaction**:
```
You: Explain dependency injection

Teacher: Let's break this down into digestible steps.

**Core Concept**: Dependency Injection (DI) separates object creation
from object usage.

**Step 1 - The Problem**: [Explains tight coupling with example]
**Step 2 - The Solution**: [Shows DI pattern with code]
**Step 3 - Benefits**: [Lists advantages with scenarios]
**Step 4 - Verification**: Can you identify the injected dependency
                         in this example? [Quiz question]
```

### 🌱 Mentor
**Focus**: Growth and professional development
**Style**: Supportive, reflective, growth-oriented
**Best for**: Career guidance, skill development, long-term planning

**Example interaction**:
```
You: Should I focus on frontend or backend?

Mentor: Let's explore what drives you.

**Reflection questions**:
- What energizes you more: visual design or system architecture?
- When you've enjoyed past projects, what were you building?
- What does career success look like to you in 5 years?

[After reflection...]

Based on your answers, I see strong systems thinking and interest
in scale. Backend development aligns with those strengths.

**Growth path suggestion**: [Personalized learning roadmap]
**Check-in milestone**: Let's revisit in 3 months after you've
                       explored [specific technology]
```

### 💼 Consultant
**Focus**: Solutions and professional analysis
**Style**: Formal, analytical, trade-off focused
**Best for**: Technical decisions, architecture choices, vendor selection

**Example interaction**:
```
You: Which database should I use?

Consultant: Let me analyze your requirements.

**Context gathered**: [Lists your constraints, scale, budget]

**Option A: PostgreSQL**
✅ Pros: ACID guarantees, rich query language, free
⚠️  Cons: Vertical scaling limits, operational overhead
📊 Fit score: 8/10

**Option B: DynamoDB**
✅ Pros: Infinite scale, managed service, predictable latency
⚠️  Cons: Limited query patterns, cost at scale, vendor lock-in
📊 Fit score: 6/10

**Recommendation**: PostgreSQL (Confidence: High)
**Reasoning**: [Evidence-based analysis]
**Assumptions**: [Explicit assumptions]
```

### 🧙 Guru
**Focus**: Deep expertise and first principles
**Style**: Authoritative, principle-based, historically informed
**Best for**: Best practices, industry standards, architectural wisdom

**Example interaction**:
```
You: What's the right way to handle errors?

Guru: This is a foundational question with a clear answer rooted
      in decades of systems engineering.

**First Principle**: Errors are values, not control flow.

**Historical context**: Exception-based error handling emerged from
Lisp (1960s), but exceptional cases aren't truly exceptional in
distributed systems. Go (2009) and Rust (2015) returned to
explicit error values.

**Best practice**:
1. Make errors visible in function signatures
2. Handle errors at decision boundaries
3. Log context, not just messages
4. Fail fast, recover deliberately

**Anti-pattern**: Catch-all exception handlers that mask problems

This principle applies across languages: Result<T,E> in Rust,
Either in Haskell, error returns in Go, Result types in TypeScript.
```

### 🏃 Coach
**Focus**: Performance and incremental improvement
**Style**: Encouraging, iterative, practice-focused
**Best for**: Code reviews, skill practice, performance optimization

**Example interaction**:
```
You: Review this function [code shown]

Coach: Great start! Let's level up your code together.

**Strengths** (keep doing):
✅ Clear variable names (readability: 8/10)
✅ Edge cases handled (robustness: 7/10)

**Level 1 improvements** (do this week):
🎯 Extract magic number on line 42 to named constant
🎯 Add early return on line 15 (reduce nesting)

**Level 2 improvements** (next week):
⭐ Consider memoization for expensive calculation
⭐ Explore generator pattern for memory efficiency

**Practice exercise**:
Try refactoring lines 40-55 using the extract method pattern.
Share your attempt and I'll provide feedback.

**Progress tracker**: This is your 3rd review. Comparing to first
review: readability improved 40%, edge case handling up 30%.
Nice growth! 📈
```

---

## Documentation

- **[AGENTS.md](AGENTS.md)** - Complete advisor configuration and protocols
- **[Creating Advisor Agents](.aget/docs/CREATING_ADVISOR_AGENTS.md)** - Detailed instantiation guide
- **[Advisor Capability Matrix](.aget/docs/ADVISOR_CAPABILITY_MATRIX.md)** - What advisors can/cannot do
- **[Specification](.aget/specs/ADVISOR_TEMPLATE_SPEC_v1.0.yaml)** - Formal capability specification (27 capabilities)
- **[Contract Tests](tests/)** - Automated validation (16 tests)

---

## Contract Tests

Advisors include 16 contract tests that validate read-only boundaries:

```bash
# Run all tests
python3 -m pytest tests/ -v

# Run specific test suites
python3 -m pytest tests/test_advisor_contract.py -v      # 7 advisor-specific tests
python3 -m pytest tests/test_identity_contract.py -v     # 3 identity tests
python3 -m pytest tests/test_wake_contract.py -v         # 6 wake protocol tests
```

**Key validations**:
- ✅ Instance type is "aget" (read-only)
- ✅ All action capabilities disabled
- ✅ Persona declared and valid
- ✅ Advisory mode indicated in wake protocol
- ✅ Role boundaries enforced
- ✅ Identity consistency maintained

**Test coverage**: 16/16 tests passing required before deployment

---

## Example Configurations

See `.aget/examples/` for complete persona configurations:

- `persona_teacher.json` - Educational guidance agent
- `persona_mentor.json` - Career development advisor
- `persona_consultant.json` - Technical decision consultant
- `persona_guru.json` - Expert authority on best practices
- `persona_coach.json` - Performance improvement coach

Each example includes:
- Complete version.json structure
- Persona-specific configuration
- Domain customization examples
- Usage notes

---

## Advisory Protocols

### Requirements Before Solutions (L114)

Advisors follow PAUSE, ASK, UNDERSTAND, RECOMMEND pattern:

1. **PAUSE** - Don't jump to solutions
2. **ASK** - Gather context through clarifying questions
3. **UNDERSTAND** - Validate requirements before recommending
4. **RECOMMEND** - Present options with confidence levels and assumptions

### Confidence Levels

Every recommendation includes explicit confidence:

- **High** - Clear requirements, known solution, low risk
- **Medium** - Some ambiguity, multiple viable options
- **Low** - Missing context, recommend more discovery

### Role Boundaries (L95, L118)

Advisors stay in advisory role by:
- Using advisory framing language ("As advisor:", "Recommendation:")
- Never saying "I'll do X" or "Let me create Y"
- Acknowledging if they overstep ("I was acting rather than advising")
- Recovering by presenting recommendations instead

---

## Template Family

Advisor template is part of the AGET template family:

| Template | Purpose | Instance Type | Action Capability |
|----------|---------|---------------|-------------------|
| **template-worker-aget** | General-purpose work | `aget` or `AGET` | Configurable |
| **template-supervisor-aget** | Fleet coordination | `AGET` | Yes (manages agents) |
| **template-advisor-aget** | Advisory only | `aget` | No (read-only) |

**Key difference**: Advisor template enforces read-only through:
- Fixed `instance_type: "aget"` (cannot be changed)
- Contract tests validating no action capabilities
- Persona-based communication styles
- Advisory protocol requirements

---

## Framework Information

**Organization**: [aget-framework](https://github.com/aget-framework)
**Template**: [template-advisor-aget](https://github.com/aget-framework/template-advisor-aget)
**Hub** (issues): [aget](https://github.com/aget-framework/aget)

**Version**: v3.1.0 "5D Composition Architecture"
- **New in v3.1.0**: 5D Composition Architecture, manifest v3 schema, persona dimension
- **v2.12.0**: Capability composition system, template manifests
- **v3.1.0**: Portfolio governance system, organizational memory patterns

---

## Specification

| Attribute | Value |
|-----------|-------|
| **Governed By** | [AGET_TEMPLATE_SPEC v3.1](https://github.com/aget-framework/aget/blob/main/specs/AGET_TEMPLATE_SPEC.md) |
| **Foundation** | [WORKER_TEMPLATE_SPEC v1.0](https://github.com/aget-framework/aget/blob/main/specs/WORKER_TEMPLATE_SPEC_v1.0.yaml) |
| **Archetype** | Advisor |
| **Manifest Version** | 3.0 |
| **Contract Tests** | 165 tests |

### Key Capabilities

| ID | Capability | Pattern |
|----|------------|---------|
| CAP-001 | Wake Protocol | event-driven |
| CAP-009 | Wind Down Protocol | event-driven |
| CAP-019 | Read-Only Mode | optional |
| CAP-ADV | Persona System | ubiquitous |

Validate compliance: `pytest tests/ -v`

See: [Full specification](https://github.com/aget-framework/aget/tree/main/specs)

---

## Creating Advisor Instances

See [.aget/docs/CREATING_ADVISOR_AGENTS.md](.aget/docs/CREATING_ADVISOR_AGENTS.md) for detailed guide.

**Quick checklist**:
1. Clone template to `my-{domain}-advisor-aget`
2. Edit `.aget/version.json` (agent_name, persona, domain)
3. Run contract tests: `python3 -m pytest tests/ -v`
4. Verify all 16 tests pass
5. Update AGENTS.md with domain-specific context
6. Deploy to GitHub (optional, can stay local)

---

## When to Use Advisor vs Worker

**Use advisor template when**:
- You want recommendations, not execution
- You need analysis without system modification
- You want persona-differentiated communication
- You're building for governance/compliance scenarios

**Use worker template when**:
- You need action-taking capability
- You want flexibility to enable/disable write operations
- You're building general-purpose agents
- You need both advisory and execution modes

**Template conversion**: Worker → Advisor requires validation. Advisor → Worker requires architecture review (one-way door on action capability).

---

## Contributing

Contributions welcome! See the [hub repo](https://github.com/aget-framework/aget) for issues and coordination.

---

## License

**AGET Framework (This Template)**: Apache License 2.0

This template and all framework code (`.aget/` structure, patterns, protocols) are licensed under the Apache License 2.0. This ensures:

- **Patent protection** for all adopters
- **Freedom to fork**, modify, and redistribute
- **Enterprise-safe** licensing for production use

See [LICENSE](LICENSE) for full terms.

**Your Agent Instance**: Your Choice

When you create an agent from this template, **you choose the license** for your specific instance:

- Keep it Apache 2.0 (recommended for public/shared agents)
- Make it private (all rights reserved)
- Choose MIT, GPL, or any other license

**The framework is open commons. What you build with it is yours.**

### Why Apache 2.0?

AGET is production infrastructure for agent configuration and lifecycle management. Apache 2.0 provides:

1. **Patent Grant**: Contributors can't patent their contributions and sue adopters
2. **Patent Retaliation**: If someone sues for patent infringement, they lose their license
3. **Ecosystem Immunity**: The standard stays free even as it becomes valuable
4. **Enterprise Adoption**: Legal teams approve Apache 2.0 more readily than other licenses

This follows the precedent of Kubernetes, Android, Swift, and other infrastructure projects.

### Upgrading Existing Agents

If you created an agent from an earlier MIT-licensed template, no action is required. Your agent remains valid under MIT (grandfathered).

To upgrade to Apache 2.0 for patent protection benefits, see the upgrade guide in the [AGET Framework documentation](https://github.com/aget-framework).

---

## Support

- **Issues**: [File to hub repo](https://github.com/aget-framework/aget/issues) with `[advisor-template]` prefix
- **Documentation**: Start with [AGENTS.md](AGENTS.md)

---

*Aget Framework - Advisory agents with persona-based guidance*
