"""
Contract test: Verify .aget/ boundary compliance

Ensures no domain-specific directories exist in .aget/
See: L285_advisor_aget_boundary_violations.md

v2.10.0: Added SKIP_TEMPLATE - these are instance-only tests
         Templates may have example/demo content in .aget/
"""

import pytest
from pathlib import Path
from conftest import is_template_context


# Skip reason for instance-only tests (boundary validation)
SKIP_TEMPLATE = pytest.mark.skipif(
    is_template_context(),
    reason="Instance-only test: templates may have example domain content in .aget/"
)


@SKIP_TEMPLATE
def test_no_domain_directories_in_aget():
    """
    Verify no domain-specific directories in .aget/

    Domain data must be at root level, not in framework directory.
    This prevents:
    - Privacy risk (personal data in framework)
    - Deletion risk (user deletes .aget/ loses domain data)
    - Portability issues (domain data in portable layer)
    """
    # List of forbidden directory names in .aget/
    forbidden = [
        'cases', 'claims', 'policies', 'contracts',
        'knowledge', 'client_progress', 'commitments',
        'decisions', 'examples', 'coverage_gaps',
        'sessions',  # Should be at root
        'learning',  # Ambiguous with evolution/, should be at root
        'deliverables', 'products',  # Should be at root
        'clients', 'customers', 'vendors',  # Domain entities
    ]

    aget_dir = Path('.aget')
    if not aget_dir.exists():
        pytest.skip(".aget/ directory not found (not an AGET agent)")

    # Check for violations
    violations = []
    for item in aget_dir.iterdir():
        if item.is_dir() and item.name in forbidden:
            violations.append(item.name)

    # Report violations with helpful message
    if violations:
        violation_list = '\n  - .aget/' + '\n  - .aget/'.join(violations)
        pytest.fail(
            f"Domain directories found in .aget/ (boundary violation):\n"
            f"{violation_list}\n\n"
            f"Action: Move these to root level:\n"
            f"  git mv .aget/{violations[0]} {violations[0]}/\n\n"
            f"Rationale: .aget/ is for framework knowledge (portable),\n"
            f"not domain data (project-specific).\n\n"
            f"See: L285_advisor_aget_boundary_violations.md\n"
            f"Spec: .aget/docs/ADVISOR_SCOPED_WRITES_SPEC.md"
        )


@SKIP_TEMPLATE
def test_aget_directory_is_lean():
    """
    Verify .aget/ directory stays lean (not bloated with domain data)

    Target: <100 files in .aget/ (excluding evolution/)
    Warning: >100 files suggests domain data creep
    """
    aget_dir = Path('.aget')
    if not aget_dir.exists():
        pytest.skip(".aget/ directory not found")

    # Count files (excluding evolution/ which can be large)
    file_count = 0
    for item in aget_dir.rglob('*'):
        if item.is_file() and 'evolution' not in item.parts:
            file_count += 1

    # Warning threshold
    if file_count > 100:
        pytest.fail(
            f".aget/ has {file_count} files (excluding evolution/)\n"
            f"Target: <100 files\n\n"
            f"Likely cause: Domain data in .aget/ (should be at root)\n\n"
            f"Review .aget/ contents and move domain data to root:\n"
            f"  ls -la .aget/  # Identify domain directories\n"
            f"  git mv .aget/domain_dir domain_dir/\n\n"
            f"See: L285_advisor_aget_boundary_violations.md"
        )


@SKIP_TEMPLATE
def test_sessions_at_root():
    """
    Verify sessions/ is at root, not in .aget/

    Work history belongs to project (root), not framework (.aget/)
    """
    aget_sessions = Path('.aget/sessions')
    root_sessions = Path('sessions')

    if aget_sessions.exists():
        pytest.fail(
            "sessions/ found in .aget/ - should be at root\n\n"
            "Action:\n"
            "  git mv .aget/sessions sessions/\n\n"
            "Rationale: Work history belongs to project, not framework.\n"
            "User might delete .aget/ but wants to keep work log.\n\n"
            "See: L285_advisor_aget_boundary_violations.md"
        )

    # Optional: Warn if no sessions/ at all (not critical)
    if not root_sessions.exists():
        pytest.skip("No sessions/ directory found (optional)")
