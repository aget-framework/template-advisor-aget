#!/usr/bin/env python3
"""v2.5/v2.6/v3.0 Advisor Contract Tests

Tests that advisor agents maintain read-only boundaries and proper persona configuration.
Enforces hybrid enforcement model: declarations + automated validation.

v2.5.0: Global read-only (boolean values)
v2.6.0: Scoped write permissions (string "scoped" with write_scope section)
v3.0.0: Template-based architecture with capabilities list

Part of AGET framework advisor template validation.

v2.10.0: Added template context detection - instance-only tests skipped on templates
v3.0.0-beta: Added v3.0 schema compatibility for templates
"""

import pytest
import json
from pathlib import Path
from conftest import is_template_context


# Skip reason for instance-only tests (memory layer tests)
SKIP_TEMPLATE = pytest.mark.skipif(
    is_template_context(),
    reason="Instance-only test: .memory/ directory is created at instantiation"
)

# Skip reason for v2.x-specific tests
SKIP_TEMPLATE_V2 = pytest.mark.skipif(
    is_template_context(),
    reason="v2.x instance test: v3.0 templates use template field instead of persona/roles"
)


def test_instance_type_valid():
    """Advisor agents/templates must have valid instance_type.

    v2.x: instance_type == 'aget'
    v3.0: instance_type == 'template' with template field
    """
    version_file = Path(__file__).parent.parent / ".aget/version.json"
    assert version_file.exists(), "version.json not found"

    with open(version_file) as f:
        data = json.load(f)
        assert "instance_type" in data, "version.json missing instance_type field"

        instance_type = data["instance_type"]
        manifest_version = data.get("manifest_version", "2.0")

        # v3.0 templates use instance_type: "template"
        if manifest_version.startswith("3."):
            assert instance_type == "template", \
                f"v3.0 templates must have instance_type='template', got '{instance_type}'"
            assert "template" in data, "v3.0 templates must have 'template' field"
            assert data["template"] == "advisor", \
                f"Expected template='advisor', got '{data.get('template')}'"
        else:
            # v2.x instances
            assert instance_type == "aget", \
                f"v2.x advisors must have instance_type='aget', got '{instance_type}'"


def test_role_includes_advisor():
    """Advisor agents must include 'advisor' in roles array."""
    version_file = Path(__file__).parent.parent / ".aget/version.json"
    assert version_file.exists(), "version.json not found"

    with open(version_file) as f:
        data = json.load(f)

        # Roles can be string or array, handle both
        if "roles" in data:
            roles = data["roles"]
            if isinstance(roles, str):
                roles = [roles]
            assert isinstance(roles, list), "roles must be a list or string"
            assert "advisor" in roles, \
                f"Advisor agents must include 'advisor' in roles, got: {roles}"


def test_persona_or_template_declared():
    """Advisor agents must declare a persona (v2.x) or template (v3.0)."""
    version_file = Path(__file__).parent.parent / ".aget/version.json"
    assert version_file.exists(), "version.json not found"

    with open(version_file) as f:
        data = json.load(f)
        manifest_version = data.get("manifest_version", "2.0")

        # v3.0 uses template field instead of persona
        if manifest_version.startswith("3."):
            assert "template" in data, "v3.0 requires 'template' field"
            template = data["template"]
            assert template == "advisor", f"Expected template='advisor', got '{template}'"
        else:
            # v2.x uses persona field
            assert "persona" in data, "version.json missing persona field"
            persona = data["persona"]
            if persona is not None:
                assert isinstance(persona, str), f"persona must be string or null, got {type(persona)}"


def test_advisory_capabilities_read_only():
    """Advisor agents must declare read_only capability as true or 'scoped'."""
    version_file = Path(__file__).parent.parent / ".aget/version.json"
    assert version_file.exists(), "version.json not found"

    with open(version_file) as f:
        data = json.load(f)

        assert "advisory_capabilities" in data, \
            "version.json missing advisory_capabilities section"

        capabilities = data["advisory_capabilities"]
        assert isinstance(capabilities, dict), \
            "advisory_capabilities must be a dictionary"

        assert "read_only" in capabilities, \
            "advisory_capabilities missing read_only field"

        read_only = capabilities["read_only"]
        # v2.5.0: boolean true, v2.6.0: string "scoped"
        assert read_only is True or read_only == "scoped", \
            f"Advisors must be read-only: advisory_capabilities.read_only must be true or 'scoped', got {read_only}"


def test_no_action_capabilities():
    """Advisor agents must not have unrestricted action capabilities."""
    version_file = Path(__file__).parent.parent / ".aget/version.json"
    assert version_file.exists(), "version.json not found"

    with open(version_file) as f:
        data = json.load(f)

        assert "advisory_capabilities" in data, \
            "version.json missing advisory_capabilities section"

        capabilities = data["advisory_capabilities"]

        # can_execute must always be false (no scoped execution)
        if "can_execute" in capabilities:
            assert capabilities["can_execute"] is False, \
                f"Advisor cannot execute commands: can_execute must be false, got {capabilities['can_execute']}"

        # can_modify_files and can_create_files: false (v2.5.0) or "scoped" (v2.6.0)
        write_capabilities = ["can_modify_files", "can_create_files"]
        for cap in write_capabilities:
            if cap in capabilities:
                value = capabilities[cap]
                assert value is False or value == "scoped", \
                    f"Advisor {cap} must be false or 'scoped', got {value}"


def test_persona_is_valid():
    """If persona declared (not null), must be from allowed set."""
    version_file = Path(__file__).parent.parent / ".aget/version.json"
    assert version_file.exists(), "version.json not found"

    with open(version_file) as f:
        data = json.load(f)

        # Get supported personas list
        assert "advisory_capabilities" in data, \
            "version.json missing advisory_capabilities section"

        capabilities = data["advisory_capabilities"]
        assert "supported_personas" in capabilities, \
            "advisory_capabilities missing supported_personas list"

        supported = capabilities["supported_personas"]
        assert isinstance(supported, list), "supported_personas must be a list"

        # Expected personas
        expected_personas = ["teacher", "mentor", "consultant", "guru", "coach"]
        assert set(supported) == set(expected_personas), \
            f"supported_personas must be {expected_personas}, got {supported}"

        # Check actual persona (if not null)
        if "persona" in data and data["persona"] is not None:
            persona = data["persona"]
            assert persona in supported, \
                f"persona '{persona}' not in supported_personas {supported}"


def test_supported_personas_list():
    """Advisory capabilities must list all 5 supported personas."""
    version_file = Path(__file__).parent.parent / ".aget/version.json"
    assert version_file.exists(), "version.json not found"

    with open(version_file) as f:
        data = json.load(f)

        assert "advisory_capabilities" in data, \
            "version.json missing advisory_capabilities section"

        capabilities = data["advisory_capabilities"]
        assert "supported_personas" in capabilities, \
            "advisory_capabilities missing supported_personas field"

        supported = capabilities["supported_personas"]
        assert isinstance(supported, list), "supported_personas must be a list"
        assert len(supported) == 5, \
            f"Must support exactly 5 personas, got {len(supported)}: {supported}"

        # Verify all expected personas present
        expected = {"teacher", "mentor", "consultant", "guru", "coach"}
        actual = set(supported)
        assert actual == expected, \
            f"Missing personas: {expected - actual}, Unexpected: {actual - expected}"


# --- v2.6.0+ Scoped Write Permission Tests ---

@SKIP_TEMPLATE_V2
def test_write_scope_declared_if_scoped():
    """Advisors with 'scoped' permissions must declare write_scope section (v2.6.0+ instances).

    Note: v3.0 templates may not have complete write_scope configuration.
    Full write_scope is configured at instantiation time.
    """
    version_file = Path(__file__).parent.parent / ".aget/version.json"
    assert version_file.exists(), "version.json not found"

    with open(version_file) as f:
        data = json.load(f)

        capabilities = data.get("advisory_capabilities", {})

        # Check if using scoped permissions
        read_only = capabilities.get("read_only")
        can_modify = capabilities.get("can_modify_files")
        can_create = capabilities.get("can_create_files")

        uses_scoped = (read_only == "scoped" or
                       can_modify == "scoped" or
                       can_create == "scoped")

        if uses_scoped:
            assert "write_scope" in capabilities, \
                "Advisors using 'scoped' permissions must declare write_scope section"

            write_scope = capabilities["write_scope"]
            assert isinstance(write_scope, dict), \
                "write_scope must be a dictionary"

            # Required fields
            assert "allowed_paths" in write_scope, \
                "write_scope missing allowed_paths"
            assert "forbidden_paths" in write_scope, \
                "write_scope missing forbidden_paths"


def test_write_scope_paths_valid():
    """Write scope allowed_paths must be internal (.aget/* only) (v2.6.0+)."""
    version_file = Path(__file__).parent.parent / ".aget/version.json"
    assert version_file.exists(), "version.json not found"

    with open(version_file) as f:
        data = json.load(f)

        capabilities = data.get("advisory_capabilities", {})

        # Only check if write_scope exists
        if "write_scope" not in capabilities:
            pytest.skip("write_scope not declared (v2.5.0 agent)")

        write_scope = capabilities["write_scope"]
        allowed = write_scope.get("allowed_paths", [])

        assert isinstance(allowed, list), \
            "write_scope.allowed_paths must be a list"

        # All allowed paths must be internal (.aget/*)
        for path in allowed:
            assert path.startswith(".aget/"), \
                f"Allowed path '{path}' must be internal (.aget/* only) - external writes forbidden"


def test_scoped_write_maintains_external_readonly():
    """Scoped writes must explicitly forbid external file modification (v2.6.0+)."""
    version_file = Path(__file__).parent.parent / ".aget/version.json"
    assert version_file.exists(), "version.json not found"

    with open(version_file) as f:
        data = json.load(f)

        capabilities = data.get("advisory_capabilities", {})

        # Only check if write_scope exists
        if "write_scope" not in capabilities:
            pytest.skip("write_scope not declared (v2.5.0 agent)")

        write_scope = capabilities["write_scope"]
        forbidden = write_scope.get("forbidden_paths", [])

        assert isinstance(forbidden, list), \
            "write_scope.forbidden_paths must be a list"

        # Critical external paths must be forbidden
        required_forbidden = ["AGENTS.md", "README.md", "version.json", "src/", "tests/"]

        # Check if wildcard (*) is present (forbids everything not explicitly allowed)
        has_wildcard = "*" in forbidden

        if not has_wildcard:
            # If no wildcard, must explicitly list critical paths
            for path in required_forbidden:
                assert path in forbidden, \
                    f"External path '{path}' must be in forbidden_paths (or use '*' wildcard)"


@SKIP_TEMPLATE
def test_memory_directory_exists():
    """Advisor agents must have .memory/ directory for Layer 4 relationship state (v2.9+)."""
    memory_dir = Path(".memory")
    assert memory_dir.exists(), \
        "Advisor agents must have .memory/ directory at root (Layer 4 - v2.9 standard)"
    assert memory_dir.is_dir(), ".memory/ must be a directory"


@SKIP_TEMPLATE
def test_memory_clients_directory_exists():
    """Advisor agents must have .memory/clients/ for client relationship tracking (v2.9+)."""
    clients_dir = Path(".memory/clients")
    assert clients_dir.exists(), \
        ".memory/clients/ directory must exist for client relationship state"
    assert clients_dir.is_dir(), ".memory/clients/ must be a directory"


@SKIP_TEMPLATE
def test_memory_engagements_directory_exists():
    """Advisor agents must have .memory/engagements/ for engagement tracking (v2.9+)."""
    engagements_dir = Path(".memory/engagements")
    assert engagements_dir.exists(), \
        ".memory/engagements/ directory must exist for engagement state"
    assert engagements_dir.is_dir(), ".memory/engagements/ must be a directory"


def test_sessions_at_root():
    """Sessions must be at root (sessions/), not in .aget/sessions/ (v2.9 standard)."""
    sessions_root = Path(__file__).parent.parent / "sessions"
    sessions_aget = Path(__file__).parent.parent / ".aget/sessions"
    
    # sessions/ at root is recommended (not strictly required for new templates)
    # This is more of a migration check, templates start fresh
    # But we document it as the standard location
    
    # If .aget/sessions/ exists with files, that's non-compliant
    if sessions_aget.exists() and sessions_aget.is_dir():
        session_files = list(sessions_aget.glob("SESSION_*.md"))
        assert len(session_files) == 0, \
            "Sessions must be in sessions/ at root, not .aget/sessions/ (v2.9 standard)"


@SKIP_TEMPLATE
def test_agents_md_documents_memory():
    """AGENTS.md must document .memory/ usage for advisors (v2.9+)."""
    agents_md = Path("AGENTS.md")
    assert agents_md.exists(), "AGENTS.md not found"
    
    with open(agents_md) as f:
        content = f.read()
        assert ".memory/" in content, \
            "AGENTS.md must document .memory/ directory (Layer 4 advisor state)"
        assert "clients/" in content or "engagements/" in content, \
            "AGENTS.md must document .memory/clients/ and .memory/engagements/ subdirectories"


@SKIP_TEMPLATE
def test_memory_readme_exists():
    """Advisor agents must have .memory/README.md with usage guidelines (v2.9+)."""
    memory_readme = Path(".memory/README.md")
    assert memory_readme.exists(), \
        ".memory/README.md must exist with usage guidelines"
    
    # Verify it has some content
    with open(memory_readme) as f:
        content = f.read()
        assert len(content) > 500, \
            ".memory/README.md must have substantial usage documentation (≥500 chars)"
        assert "clients/" in content, \
            ".memory/README.md must document clients/ subdirectory"
        assert "engagements/" in content, \
            ".memory/README.md must document engagements/ subdirectory"
