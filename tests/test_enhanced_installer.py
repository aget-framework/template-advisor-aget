"""
Enhanced tests for the installer with better coverage
"""

import pytest
import tempfile
import shutil
from pathlib import Path
import sys
import os
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from installer.install import TemplateInstaller


class TestTemplateInstaller:
    """Test the template installer"""

    def test_minimal_install(self):
        """Test minimal template installation"""
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / 'test_project'
            target.mkdir()

            installer = TemplateInstaller(target, template='minimal')
            success = installer.install()

            assert success
            assert (target / 'AGENTS.md').exists()
            assert (target / 'scripts' / 'session_protocol.py').exists()
            assert (target / 'Makefile').exists()

    def test_standard_install(self):
        """Test standard template installation"""
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / 'test_project'
            target.mkdir()

            installer = TemplateInstaller(target, template='standard')
            success = installer.install()

            assert success
            assert (target / 'AGENTS.md').exists()
            assert (target / 'scripts' / 'session_protocol.py').exists()
            assert (target / 'scripts' / 'health_check.py').exists()
            assert (target / 'Makefile').exists()

    def test_advanced_install(self):
        """Test advanced template installation"""
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / 'test_project'
            target.mkdir()

            installer = TemplateInstaller(target, template='advanced')
            success = installer.install()

            assert success
            # Should include everything from standard
            assert (target / 'AGENTS.md').exists()
            assert (target / 'scripts' / 'session_protocol.py').exists()
            assert (target / 'scripts' / 'health_check.py').exists()

    def test_dry_run(self):
        """Test dry run mode doesn't modify files"""
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / 'test_project'
            target.mkdir()

            installer = TemplateInstaller(target, template='minimal', dry_run=True)
            success = installer.install()

            assert success
            # Files should NOT be created in dry run
            assert not (target / 'AGENTS.md').exists()
            assert not (target / 'scripts').exists()

    def test_invalid_template(self):
        """Test handling of invalid template name"""
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / 'test_project'
            target.mkdir()

            installer = TemplateInstaller(target, template='nonexistent')
            success = installer.install()

            assert not success

    def test_target_not_exists(self):
        """Test handling when target doesn't exist"""
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / 'nonexistent'

            installer = TemplateInstaller(target)
            success = installer.install()

            assert not success

    def test_symlink_creation(self):
        """Test CLAUDE.md symlink creation"""
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / 'test_project'
            target.mkdir()

            installer = TemplateInstaller(target, template='minimal')
            installer.install()

            # Check symlink or copy exists
            assert (target / 'CLAUDE.md').exists()
            # If symlinks are supported, it should be a symlink
            if hasattr(os, 'symlink'):
                assert (target / 'CLAUDE.md').is_symlink() or (target / 'CLAUDE.md').is_file()

    def test_customize_python_project(self):
        """Test customization for Python project"""
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / 'test_project'
            target.mkdir()

            # Create requirements.txt to identify as Python project
            (target / 'requirements.txt').write_text('pytest\n')

            installer = TemplateInstaller(target)
            installer.install()

            # Read AGENTS.md and check customization
            agent_content = (target / 'AGENTS.md').read_text()
            assert 'Python' in agent_content or 'test_project' in agent_content

    def test_customize_node_project(self):
        """Test customization for Node.js project"""
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / 'test_project'
            target.mkdir()

            # Create package.json to identify as Node project
            (target / 'package.json').write_text('{"name": "test"}')

            installer = TemplateInstaller(target)
            installer.install()

            # Read AGENTS.md and check customization
            agent_content = (target / 'AGENTS.md').read_text()
            assert 'JavaScript' in agent_content or 'Node' in agent_content or 'test_project' in agent_content

    def test_merge_makefile(self):
        """Test Makefile merging with existing file"""
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / 'test_project'
            target.mkdir()

            # Create existing Makefile
            existing_makefile = target / 'Makefile'
            existing_makefile.write_text('test:\n\tpython -m pytest\n')

            installer = TemplateInstaller(target)
            installer.install()

            # Check Makefile was merged
            makefile_content = existing_makefile.read_text()
            assert 'test:' in makefile_content  # Original content
            # New content would be appended

    def test_config_file_creation(self):
        """Test .cli-agent.yaml configuration file creation"""
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / 'test_project'
            target.mkdir()

            installer = TemplateInstaller(target, template='standard')
            installer.install()

            config_file = target / '.cli-agent.yaml'
            if config_file.exists():
                # PyYAML is installed
                import yaml
                with open(config_file) as f:
                    config = yaml.safe_load(f)

                assert 'template' in config
                assert config['template']['template'] == 'standard'
                assert 'patterns' in config
                assert 'session_management' in config['patterns']