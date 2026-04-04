# Contributing to CLI Agent Template

Thank you for your interest in contributing! This project uses its own patterns - when you work on it, the patterns help you maintain it.

## Quick Start

1. Fork and clone the repository
2. Tell your CLI agent: "hey"
3. Make your changes
4. Tell your CLI agent: "save work"
5. Submit a pull request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/aget-cli-agent-template
cd aget-cli-agent-template

# Install the patterns in the project itself (dogfooding)
python3 installer/install.py . --template standard

# Start developing
# Tell your CLI agent: "hey"
```

## Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please:

- Be respectful and constructive
- Welcome newcomers and help them get started
- Focus on what is best for the community
- Show empathy towards other community members

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

1. **Clear title and description**
2. **Steps to reproduce**
3. **Expected vs actual behavior**
4. **System information** (OS, Python version, CLI agent used)
5. **Relevant logs or error messages**

### Suggesting Features

Feature requests are welcome! Please provide:

1. **Use case** - Why is this needed?
2. **Proposed solution** - How should it work?
3. **Alternatives considered** - What else did you think about?
4. **Additional context** - Screenshots, examples, etc.

### Pull Requests

1. **Create an issue first** - Discuss the change before implementing
2. **Fork and create a branch** - `feature/amazing-feature` or `fix/bug-description`
3. **Follow existing patterns** - Look at similar code in the repository
4. **Write clear commit messages** - Use conventional commits format
5. **Test your changes** - Run `python3 -m pytest tests/`
6. **Update documentation** - If you change behavior, update docs
7. **Submit PR** - Link to the issue and describe your changes

## Development Guidelines

### Code Style

- Python: Follow PEP 8
- Use type hints where appropriate
- Write docstrings for functions
- Keep functions focused and small

### Pattern Development

When creating new patterns:

```python
# patterns/category/pattern_name.py

def pattern_name():
    """
    Brief description of what this pattern does.

    Trigger: "pattern trigger phrase"
    Safety: dry-run/read-only/requires-confirmation
    """
    print("🔄 Running pattern_name...")

    # Implementation

    print("✅ Pattern completed")
```

### Testing

Write tests for new patterns:

```python
# tests/test_pattern_name.py

def test_pattern_name():
    """Test the pattern_name functionality."""
    result = pattern_name(dry_run=True)
    assert result.success
    assert "expected output" in result.output
```

Run tests before submitting:

```bash
python3 -m pytest tests/ -v
python3 scripts/health_check.py sanity-check
```

### Documentation

- Update README.md if adding major features
- Add pattern documentation to `patterns/category/README.md`
- Include usage examples
- Document any breaking changes

## Commit Message Format

We use conventional commits:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test additions or fixes
- `chore`: Maintenance tasks

Examples:
```
feat(patterns): Add database backup pattern
fix(session): Correct timezone handling in notes
docs: Update installation instructions
```

## Release Process

1. **Version bump** - Update VERSION file
2. **Update CHANGELOG** - Document all changes
3. **Run tests** - Ensure everything passes
4. **Create PR** - Target main branch
5. **Review** - Code review by maintainers
6. **Merge** - Squash and merge
7. **Tag** - Create release tag
8. **Publish** - Release notes on GitHub

## Pattern Contribution Guidelines

### Creating a New Pattern

1. **Identify the need** - What problem does it solve?
2. **Design the interface** - What's the trigger phrase?
3. **Consider safety** - Should it dry-run by default?
4. **Write the implementation** - Follow existing patterns
5. **Add to AGENTS.md** - Document the trigger
6. **Write tests** - Ensure it works correctly
7. **Document it** - Add to pattern README

### Pattern Standards

All patterns must:
- Have a clear trigger phrase
- Provide helpful output
- Handle errors gracefully
- Support dry-run where applicable
- Be idempotent (safe to run multiple times)
- Follow the progression: Read → Modify → Reorganize

## Questions?

- Open an issue for questions
- Check existing documentation
- Look at similar patterns for examples
- Ask in pull request comments

## Recognition

Contributors are recognized in:
- CHANGELOG.md (per release)
- GitHub contributors page
- Release notes

Thank you for contributing to make CLI agents more powerful and developer-friendly!