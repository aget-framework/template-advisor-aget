"""
Configuration Size Contract Test

Validates that AGENTS.md remains under the 40,000 character limit
to ensure reliable Claude Code processing (L146).

Pattern: L146_configuration_size_management.md
"""

import pytest
import warnings
from pathlib import Path


def test_agents_md_size_under_limit():
    """AGENTS.md must be under 40,000 characters for Claude Code compatibility."""
    agents_file = Path(__file__).parent.parent / "AGENTS.md"

    assert agents_file.exists(), "AGENTS.md not found"

    file_size = agents_file.stat().st_size
    max_size = 40000  # 40k character limit

    assert file_size < max_size, \
        f"AGENTS.md too large: {file_size} chars (limit: {max_size}). " \
        f"Move detailed documentation to .aget/docs/ to reduce size."


def test_agents_md_reasonable_size():
    """AGENTS.md should ideally be under 30,000 characters for buffer."""
    agents_file = Path(__file__).parent.parent / "AGENTS.md"

    if not agents_file.exists():
        pytest.skip("AGENTS.md not found")

    file_size = agents_file.stat().st_size
    recommended_max = 30000  # Recommended limit with buffer

    if file_size >= recommended_max:
        warnings.warn(
            f"AGENTS.md approaching limit: {file_size} chars "
            f"(recommended max: {recommended_max}). "
            f"Consider refactoring to .aget/docs/ if adding more content.",
            UserWarning
        )


def test_documentation_exists_for_overflow():
    """.aget/docs/ directory should exist for detailed documentation."""
    docs_dir = Path(__file__).parent.parent / ".aget/docs"

    # If AGENTS.md is large, docs directory should exist for overflow
    agents_file = Path(__file__).parent.parent / "AGENTS.md"
    if agents_file.exists() and agents_file.stat().st_size > 25000:
        assert docs_dir.exists(), \
            ".aget/docs/ directory should exist for detailed documentation " \
            "when AGENTS.md exceeds 25k characters"
