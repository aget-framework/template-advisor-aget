"""
Test suite for meta patterns (project scanner).
Tests multi-project scanning and migration assessment capabilities.
"""

import json
import pytest
import tempfile
import shutil
from pathlib import Path
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from patterns.meta.project_scanner import ProjectScanner, MigrationStatus


class TestProjectScanner:
    """Test project scanner pattern functionality."""

    @pytest.fixture
    def temp_workspace(self):
        """Create a temporary workspace with multiple projects."""
        workspace = tempfile.mkdtemp(prefix="test_scanner_")

        # Create fully migrated project
        migrated = Path(workspace) / "fully-migrated"
        migrated.mkdir()
        (migrated / "AGENTS.md").write_text("# AGET Agent Configuration\n@aget-version: 2.0.0\n")
        (migrated / ".aget").mkdir()
        (migrated / ".aget" / "version.json").write_text(json.dumps({
            "version": "2.0.0",
            "migration_date": "2025-09-24",
            "phase": "complete"
        }))
        (migrated / "scripts").mkdir()
        (migrated / "scripts" / "aget_session_protocol.py").write_text("# Session protocol")
        (migrated / "scripts" / "health_check.py").write_text("# Housekeeping")
        (migrated / "patterns").mkdir()
        (migrated / "patterns" / "session").mkdir()
        (migrated / ".git").mkdir()  # Mark as git repo

        # Create partially migrated project
        partial = Path(workspace) / "partial-migration"
        partial.mkdir()
        (partial / "AGENTS.md").write_text("# Agent Configuration\n")
        (partial / "scripts").mkdir()
        (partial / "scripts" / "session_protocol.py").write_text("# Old session")
        (partial / ".git").mkdir()

        # Create legacy project
        legacy = Path(workspace) / "legacy-project"
        legacy.mkdir()
        (legacy / "CLAUDE.md").write_text("# Claude configuration")
        (legacy / ".git").mkdir()

        # Create unmigrated project
        unmigrated = Path(workspace) / "unmigrated"
        unmigrated.mkdir()
        (unmigrated / "README.md").write_text("# Project")
        (unmigrated / ".git").mkdir()

        yield workspace

        # Cleanup
        shutil.rmtree(workspace)

    def test_scan_single_project(self, temp_workspace):
        """Test scanning a single project directory."""
        scanner = ProjectScanner(temp_workspace)

        # Scan fully migrated project
        status = scanner.scan_directory(Path(temp_workspace) / "fully-migrated")

        assert status is not None
        assert status['name'] == 'fully-migrated'
        assert status['aget_version'] == '2.0.0'
        assert status['migration_date'] == '2025-09-24'
        assert status['migration_status'] == MigrationStatus.COMPLETE
        assert status['score'] >= 90
        assert 'AGENTS.md' in status['patterns_adopted']
        assert '.aget directory' in status['patterns_adopted']
        assert 'session protocols' in status['patterns_adopted']
        assert 'housekeeping protocols' in status['patterns_adopted']

    def test_scan_partial_migration(self, temp_workspace):
        """Test scanning a partially migrated project."""
        scanner = ProjectScanner(temp_workspace)

        status = scanner.scan_directory(Path(temp_workspace) / "partial-migration")

        assert status is not None
        assert status['migration_status'] == MigrationStatus.PARTIAL
        assert 20 <= status['score'] < 60
        assert 'AGENTS.md' in status['patterns_adopted']
        assert 'session protocols' in status['patterns_adopted']
        assert '.aget directory' in status['patterns_missing']
        assert 'housekeeping protocols' in status['patterns_missing']

    def test_scan_legacy_project(self, temp_workspace):
        """Test scanning a legacy project with CLAUDE.md."""
        scanner = ProjectScanner(temp_workspace)

        status = scanner.scan_directory(Path(temp_workspace) / "legacy-project")

        assert status is not None
        assert status['migration_status'] == MigrationStatus.NOT_STARTED
        assert status['score'] == 0
        assert 'CLAUDE.md' in status['legacy_files']
        assert len(status['patterns_adopted']) == 0

    def test_scan_all_projects(self, temp_workspace):
        """Test scanning all projects in a workspace."""
        scanner = ProjectScanner(temp_workspace)
        scanner.scan_all_projects()

        assert scanner.summary['total_projects'] == 4
        assert scanner.summary['migrated'] >= 1
        assert scanner.summary['partial'] >= 1
        assert scanner.summary['not_started'] >= 1

        assert 'fully-migrated' in scanner.projects
        assert 'partial-migration' in scanner.projects
        assert 'legacy-project' in scanner.projects
        assert 'unmigrated' in scanner.projects

    def test_migration_status_detection(self, temp_workspace):
        """Test correct detection of migration status levels."""
        scanner = ProjectScanner(temp_workspace)
        scanner.scan_all_projects()

        # Check each project has correct status
        assert scanner.projects['fully-migrated']['migration_status'] == MigrationStatus.COMPLETE
        assert scanner.projects['partial-migration']['migration_status'] == MigrationStatus.PARTIAL
        assert scanner.projects['legacy-project']['migration_status'] == MigrationStatus.NOT_STARTED
        assert scanner.projects['unmigrated']['migration_status'] == MigrationStatus.NOT_STARTED

    def test_generate_text_report(self, temp_workspace):
        """Test generating text format report."""
        scanner = ProjectScanner(temp_workspace)
        scanner.scan_all_projects()

        report = scanner.generate_report('text')

        assert 'AGET Migration Status Report' in report
        assert 'Total Projects: 4' in report
        assert 'fully-migrated' in report
        assert 'Score:' in report
        assert 'Recommendations:' in report

    def test_generate_json_report(self, temp_workspace):
        """Test generating JSON format report."""
        scanner = ProjectScanner(temp_workspace)
        scanner.scan_all_projects()

        report_json = scanner.generate_report('json')
        report = json.loads(report_json)

        assert 'summary' in report
        assert 'projects' in report
        assert report['summary']['total_projects'] == 4
        assert 'fully-migrated' in report['projects']
        assert report['projects']['fully-migrated']['migration_status'] == 'complete'

    def test_save_report(self, temp_workspace):
        """Test saving report to filesystem."""
        scanner = ProjectScanner(temp_workspace)
        scanner.scan_all_projects()

        report_file = scanner.save_report()

        assert report_file.exists()
        assert report_file.name == 'migration_report.json'

        # Check text report also saved
        text_file = report_file.parent / 'migration_report.txt'
        assert text_file.exists()

        # Verify JSON content
        with open(report_file) as f:
            data = json.load(f)
            assert 'summary' in data
            assert 'projects' in data

    def test_customized_status_detection(self, temp_workspace):
        """Test detection of customized projects with extra patterns."""
        # Create a customized project
        custom = Path(temp_workspace) / "customized-project"
        custom.mkdir()
        (custom / "AGENTS.md").write_text("# AGET Configuration")
        (custom / ".aget").mkdir()
        (custom / "scripts").mkdir()
        (custom / "scripts" / "aget_session_protocol.py").write_text("# Session")
        (custom / "scripts" / "health_check.py").write_text("# Housekeeping")
        (custom / "patterns").mkdir()

        # Add custom pattern categories
        for pattern in ['session', 'housekeeping', 'custom1', 'custom2', 'custom3']:
            (custom / "patterns" / pattern).mkdir()

        scanner = ProjectScanner(temp_workspace)
        status = scanner.scan_directory(custom)

        assert status['migration_status'] == MigrationStatus.CUSTOMIZED
        assert status['score'] >= 60

    def test_compatibility_files_detection(self, temp_workspace):
        """Test detection of compatibility files for other agents."""
        compat = Path(temp_workspace) / "multi-agent"
        compat.mkdir()
        (compat / "AGENTS.md").write_text("# AGET Configuration")
        (compat / ".cursorrules").write_text("# Cursor rules")
        (compat / ".aider.conf.yml").write_text("# Aider config")

        scanner = ProjectScanner(temp_workspace)
        status = scanner.scan_directory(compat)

        assert '.cursorrules' in status['compatibility_files']
        assert '.aider.conf.yml' in status['compatibility_files']

    def test_version_extraction_from_agents_md(self, temp_workspace):
        """Test extracting version from AGENTS.md header."""
        versioned = Path(temp_workspace) / "versioned-project"
        versioned.mkdir()
        (versioned / "AGENTS.md").write_text("""# AGET Agent Configuration
# @aget-version: 2.1.0-beta
# @migration-date: 2025-09-24

Configuration content here...""")

        scanner = ProjectScanner(temp_workspace)
        status = scanner.scan_directory(versioned)

        assert status['aget_version'] == '2.1.0-beta'

    def test_empty_workspace(self):
        """Test scanning an empty workspace."""
        with tempfile.TemporaryDirectory() as tmpdir:
            scanner = ProjectScanner(tmpdir)
            scanner.scan_all_projects()

            assert scanner.summary['total_projects'] == 0
            assert scanner.summary['migrated'] == 0
            assert scanner.summary['partial'] == 0
            assert scanner.summary['not_started'] == 0

    def test_current_directory_as_project(self, temp_workspace):
        """Test when the root directory itself is a project."""
        # Make workspace root a project
        (Path(temp_workspace) / "AGENTS.md").write_text("# Root AGET Config")
        (Path(temp_workspace) / ".git").mkdir()

        scanner = ProjectScanner(temp_workspace)
        scanner.scan_all_projects()

        # Should include both root and subdirectories
        assert '.' in scanner.projects
        assert scanner.summary['total_projects'] >= 5  # Root + 4 subdirs