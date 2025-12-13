"""
Contract tests for advisor internal state capability.

These tests verify that advisor agents correctly implement internal state management
per ADVISOR_INTERNAL_STATE_SPEC.md and ADVISOR_SCOPED_WRITES_SPEC.md.

Tests:
1. Internal state directories exist (instance-only)
2. README files document formats (instance-only)
3. version.json declares internal state features
4. Scoped write permissions configured correctly

v2.10.0: Added template context detection - instance-only tests are skipped on templates
"""

import json
from pathlib import Path
import pytest
from conftest import is_template_context


# Skip reason for instance-only tests
SKIP_TEMPLATE = pytest.mark.skipif(
    is_template_context(),
    reason="Instance-only test: internal state directories are created at instantiation"
)


@SKIP_TEMPLATE
class TestInternalStateDirectories:
    """Verify required directory structure exists."""

    def test_sessions_directory_exists(self):
        """Session history directory must exist."""
        sessions_dir = Path(__file__).parent.parent / ".aget/sessions"
        assert sessions_dir.exists(), ".aget/sessions/ directory must exist"
        assert sessions_dir.is_dir(), ".aget/sessions/ must be a directory"

    def test_client_progress_directory_exists(self):
        """Client progress tracking directory must exist."""
        progress_dir = Path(__file__).parent.parent / ".aget/client_progress"
        assert progress_dir.exists(), ".aget/client_progress/ directory must exist"
        assert progress_dir.is_dir(), ".aget/client_progress/ must be a directory"

    def test_commitments_directory_exists(self):
        """Commitment tracking directory must exist."""
        commitments_dir = Path(__file__).parent.parent / ".aget/commitments"
        assert commitments_dir.exists(), ".aget/commitments/ directory must exist"
        assert commitments_dir.is_dir(), ".aget/commitments/ must be a directory"

    def test_context_directory_exists(self):
        """Client context directory must exist."""
        context_dir = Path(__file__).parent.parent / ".aget/context"
        assert context_dir.exists(), ".aget/context/ directory must exist"
        assert context_dir.is_dir(), ".aget/context/ must be a directory"

    def test_learning_history_directory_exists(self):
        """Learning history directory must exist."""
        learning_dir = Path(__file__).parent.parent / ".aget/learning_history"
        assert learning_dir.exists(), ".aget/learning_history/ directory must exist"
        assert learning_dir.is_dir(), ".aget/learning_history/ must be a directory"


@SKIP_TEMPLATE
class TestInternalStateDocumentation:
    """Verify each directory has format documentation."""

    def test_sessions_readme_exists(self):
        """Sessions directory must have README with format documentation."""
        readme = Path(__file__).parent.parent / ".aget/sessions/README.md"
        assert readme.exists(), ".aget/sessions/README.md must exist"
        assert readme.is_file(), ".aget/sessions/README.md must be a file"

        # Verify README content includes key sections
        content = readme.read_text()
        assert "SESSION_YYYY-MM-DD" in content, "README must document file naming convention"
        assert "session_date" in content, "README must document YAML frontmatter format"

    def test_client_progress_readme_exists(self):
        """Client progress directory must have README."""
        readme = Path(__file__).parent.parent / ".aget/client_progress/README.md"
        assert readme.exists(), ".aget/client_progress/README.md must exist"
        assert readme.is_file(), ".aget/client_progress/README.md must be a file"

        content = readme.read_text()
        assert "mastery_level" in content or "confidence_level" in content, \
            "README must document progress tracking format"

    def test_commitments_readme_exists(self):
        """Commitments directory must have README."""
        readme = Path(__file__).parent.parent / ".aget/commitments/README.md"
        assert readme.exists(), ".aget/commitments/README.md must exist"
        assert readme.is_file(), ".aget/commitments/README.md must be a file"

        content = readme.read_text()
        assert "active.yaml" in content, "README must document active commitments file"
        assert "completed.yaml" in content, "README must document completed commitments file"

    def test_context_readme_exists(self):
        """Context directory must have README."""
        readme = Path(__file__).parent.parent / ".aget/context/README.md"
        assert readme.exists(), ".aget/context/README.md must exist"
        assert readme.is_file(), ".aget/context/README.md must be a file"

        content = readme.read_text()
        assert "client_id" in content, "README must document client context format"

    def test_learning_history_readme_exists(self):
        """Learning history directory must have README."""
        readme = Path(__file__).parent.parent / ".aget/learning_history/README.md"
        assert readme.exists(), ".aget/learning_history/README.md must exist"
        assert readme.is_file(), ".aget/learning_history/README.md must be a file"

        content = readme.read_text()
        assert "mastery_level" in content, "README must document mastery tracking format"


class TestInternalStateFeatureDeclaration:
    """Verify version.json declares internal state capabilities."""

    @pytest.fixture
    def version_config(self):
        """Load version.json."""
        version_file = Path(__file__).parent.parent / ".aget/version.json"
        assert version_file.exists(), ".aget/version.json must exist"

        with open(version_file) as f:
            return json.load(f)

    def test_internal_state_feature_enabled(self, version_config):
        """version.json must declare internal_state_enabled feature."""
        assert "features" in version_config, \
            "version.json must have 'features' section"

        features = version_config["features"]
        assert "internal_state_enabled" in features, \
            "features must include 'internal_state_enabled'"
        assert features["internal_state_enabled"] is True, \
            "internal_state_enabled must be true"

    def test_session_persistence_feature_enabled(self, version_config):
        """version.json must declare session_persistence feature."""
        features = version_config.get("features", {})
        assert "session_persistence" in features, \
            "features must include 'session_persistence'"
        assert features["session_persistence"] is True, \
            "session_persistence must be true"

    def test_progress_tracking_feature_declared(self, version_config):
        """version.json must declare progress_tracking feature."""
        features = version_config.get("features", {})
        assert "progress_tracking" in features, \
            "features must include 'progress_tracking'"

    def test_scoped_write_permissions_feature_enabled(self, version_config):
        """version.json must declare scoped_write_permissions feature."""
        features = version_config.get("features", {})
        assert "scoped_write_permissions" in features, \
            "features must include 'scoped_write_permissions'"
        assert features["scoped_write_permissions"] is True, \
            "scoped_write_permissions must be true"


class TestScopedWritePermissions:
    """Verify scoped write permissions are configured correctly."""

    @pytest.fixture
    def version_config(self):
        """Load version.json."""
        with open(".aget/version.json") as f:
            return json.load(f)

    def test_advisory_capabilities_present(self, version_config):
        """version.json must have advisory_capabilities section."""
        assert "advisory_capabilities" in version_config, \
            "version.json must have 'advisory_capabilities' section"

    def test_write_scope_configured(self, version_config):
        """advisory_capabilities must include write_scope configuration."""
        advisory = version_config.get("advisory_capabilities", {})
        assert "write_scope" in advisory, \
            "advisory_capabilities must have 'write_scope' section"

    def test_allowed_paths_include_internal_state(self, version_config):
        """write_scope must allow writing to internal state directories."""
        advisory = version_config.get("advisory_capabilities", {})
        write_scope = advisory.get("write_scope", {})
        allowed_paths = write_scope.get("allowed_paths", [])

        # Check each required internal state directory is in allowed paths
        required_paths = [
            ".aget/sessions",
            ".aget/client_progress",
            ".aget/commitments",
            ".aget/context",
            ".aget/learning_history"
        ]

        for required_path in required_paths:
            # Check if path or path/** is in allowed_paths
            path_allowed = any(
                required_path in allowed for allowed in allowed_paths
            )
            assert path_allowed, \
                f"{required_path} must be in write_scope.allowed_paths"

    def test_forbidden_paths_include_external_systems(self, version_config):
        """write_scope must forbid writing to external systems."""
        advisory = version_config.get("advisory_capabilities", {})
        write_scope = advisory.get("write_scope", {})
        forbidden_paths = write_scope.get("forbidden_paths", [])

        # Check key external paths are forbidden
        external_paths = [
            "src",
            "docs",
            "workspace",
            "AGENTS.md"
        ]

        for external_path in external_paths:
            # Check if path or path/** is in forbidden_paths
            path_forbidden = any(
                external_path in forbidden for forbidden in forbidden_paths
            )
            assert path_forbidden, \
                f"{external_path} must be in write_scope.forbidden_paths"

    def test_enforcement_mode_is_strict(self, version_config):
        """write_scope enforcement must be 'strict' (errors, not warnings)."""
        advisory = version_config.get("advisory_capabilities", {})
        write_scope = advisory.get("write_scope", {})
        enforcement = write_scope.get("enforcement")

        assert enforcement == "strict", \
            "write_scope.enforcement must be 'strict' (not 'warn' or 'contract_test')"

    def test_can_write_internal_state_declared(self, version_config):
        """advisory_capabilities must declare can_write_internal_state."""
        advisory = version_config.get("advisory_capabilities", {})
        assert "can_write_internal_state" in advisory, \
            "advisory_capabilities must declare 'can_write_internal_state'"
        assert advisory["can_write_internal_state"] is True, \
            "can_write_internal_state must be true"


class TestInstanceTypeConsistency:
    """Verify instance_type is consistent with advisor role."""

    @pytest.fixture
    def version_config(self):
        """Load version.json."""
        with open(".aget/version.json") as f:
            return json.load(f)

    def test_instance_type_is_aget(self, version_config):
        """Advisor agents must have instance_type: 'aget'."""
        assert "instance_type" in version_config, \
            "version.json must have 'instance_type' field"
        assert version_config["instance_type"] == "aget", \
            "Advisor agents must have instance_type: 'aget' (not 'AGET')"

    def test_roles_include_advisor(self, version_config):
        """roles array must include 'advisor'."""
        assert "roles" in version_config, \
            "version.json must have 'roles' field"
        roles = version_config["roles"]
        assert isinstance(roles, list), "roles must be an array"
        assert "advisor" in roles, "roles must include 'advisor'"


@SKIP_TEMPLATE
class TestProtocolDocumentation:
    """Verify AGENTS.md documents internal state protocols."""

    def test_agents_md_exists(self):
        """AGENTS.md must exist."""
        agents_md = Path(__file__).parent.parent / "AGENTS.md"
        assert agents_md.exists(), "AGENTS.md must exist"

    def test_internal_state_section_exists(self):
        """AGENTS.md must have Internal State Management section."""
        with open("AGENTS.md") as f:
            content = f.read()

        assert "Internal State Management" in content, \
            "AGENTS.md must have '## Internal State Management' section"

    def test_wake_protocol_mentions_internal_state(self):
        """Wake Protocol section must reference internal state."""
        with open("AGENTS.md") as f:
            content = f.read()

        # Check for enhanced wake protocol
        assert "Enhanced with internal state" in content or \
               "Check .aget/sessions/" in content or \
               "Last session" in content, \
            "Wake Protocol must reference internal state checking"

    def test_wind_down_protocol_mentions_internal_state(self):
        """Wind Down Protocol section must reference internal state writes."""
        with open("AGENTS.md") as f:
            content = f.read()

        # Check for enhanced wind down protocol
        assert "Write Internal State" in content or \
               ".aget/sessions/" in content, \
            "Wind Down Protocol must reference internal state writes"

    def test_scoped_write_permissions_documented(self):
        """AGENTS.md must document scoped write permissions."""
        with open("AGENTS.md") as f:
            content = f.read()

        assert "Scoped Write Permissions" in content or \
               "write_scope" in content or \
               "allowed_paths" in content, \
            "AGENTS.md must document scoped write permissions"


class TestBoundaryEnforcement:
    """Verify capability boundary declarations."""

    @pytest.fixture
    def version_config(self):
        """Load version.json."""
        with open(".aget/version.json") as f:
            return json.load(f)

    def test_cannot_execute(self, version_config):
        """Advisors must not have execution capability."""
        advisory = version_config.get("advisory_capabilities", {})
        assert "can_execute" in advisory, \
            "advisory_capabilities must declare 'can_execute'"
        assert advisory["can_execute"] is False, \
            "Advisors cannot execute (must be false)"

    def test_read_only_external_systems(self, version_config):
        """Advisors must be read-only for external systems."""
        advisory = version_config.get("advisory_capabilities", {})

        # Check that read_only clarifies "external systems"
        read_only_value = advisory.get("read_only")
        assert read_only_value in ["external_systems", "scoped"], \
            "read_only must clarify scope (external_systems or scoped)"

    def test_file_modifications_scoped(self, version_config):
        """File modification capabilities must be scoped to internal state."""
        advisory = version_config.get("advisory_capabilities", {})

        can_modify = advisory.get("can_modify_files")
        can_create = advisory.get("can_create_files")

        # Must indicate scoping
        assert can_modify in ["scoped", "scoped_to_internal_state"], \
            "can_modify_files must indicate scoping"
        assert can_create in ["scoped", "scoped_to_internal_state"], \
            "can_create_files must indicate scoping"


# Run tests with: python3 -m pytest tests/test_internal_state_contract.py -v
