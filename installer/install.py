#!/usr/bin/env python3
"""
CLI Agent Template Installer
Installs patterns and templates into target projects
"""

import os
import sys
import shutil
import argparse
from pathlib import Path
import json


class TemplateInstaller:
    """Install CLI agent templates into projects"""

    def __init__(self, target_path, template='standard', dry_run=False):
        self.target = Path(target_path).resolve()
        self.source = Path(__file__).parent.parent
        self.template = template
        self.dry_run = dry_run
        self.installed = []

    def install(self):
        """Main installation process"""
        print(f"{'[DRY RUN] ' if self.dry_run else ''}Installing CLI Agent Template")
        print(f"Target: {self.target}")
        print(f"Template: {self.template}")
        print("-" * 50)

        # Check if target exists
        if not self.target.exists():
            print(f"Error: Target directory {self.target} does not exist")
            return False

        # Install based on template level
        if self.template == 'minimal':
            self.install_minimal()
        elif self.template == 'standard':
            self.install_standard()
        elif self.template == 'advanced':
            self.install_advanced()
        else:
            print(f"Error: Unknown template '{self.template}'")
            return False

        # Create configuration file
        self.create_config()

        # Report installation
        self.report()
        return True

    def install_minimal(self):
        """Install minimal template - just session management"""
        print("\nInstalling minimal template...")

        # Copy AGENTS.md template (universal agent configuration)
        agent_source = self.source / 'templates/minimal/AGENTS.md'
        # Fall back to CLAUDE.md if AGENTS.md doesn't exist yet
        if not agent_source.exists():
            agent_source = self.source / 'templates/minimal/CLAUDE.md'

        self.copy_file(
            agent_source,
            self.target / 'AGENTS.md',
            customize=True
        )

        # Create CLAUDE.md symlink for backward compatibility
        self.create_symlink('AGENTS.md', 'CLAUDE.md')

        # Create scripts directory
        self.create_dir(self.target / 'scripts')

        # Copy session protocol
        self.copy_file(
            self.source / 'scripts/session_protocol.py',
            self.target / 'scripts/session_protocol.py'
        )

        # Create basic Makefile
        self.copy_file(
            self.source / 'templates/minimal/Makefile',
            self.target / 'Makefile',
            merge=True
        )

    def install_standard(self):
        """Install standard template - recommended setup"""
        print("\nInstalling standard template...")

        # Start with minimal
        self.install_minimal()

        # Add health check (renamed from housekeeping_protocol in HCNA-001)
        self.copy_file(
            self.source / 'scripts/health_check.py',
            self.target / 'scripts/health_check.py'
        )

        # Add standard Makefile
        self.copy_file(
            self.source / 'templates/standard/Makefile',
            self.target / 'Makefile',
            merge=True
        )

        # Update AGENTS.md with additional commands
        agent_source = self.source / 'templates/standard/AGENTS.md'
        # Fall back to CLAUDE.md if AGENTS.md doesn't exist yet
        if not agent_source.exists():
            agent_source = self.source / 'templates/standard/CLAUDE.md'

        self.copy_file(
            agent_source,
            self.target / 'AGENTS.md',
            customize=True
        )

    def install_advanced(self):
        """Install advanced template - everything"""
        print("\nInstalling advanced template...")

        # Start with standard
        self.install_standard()

        # Add advanced patterns
        patterns_to_copy = ['recovery', 'documentation', 'testing']
        for pattern in patterns_to_copy:
            pattern_dir = self.source / f'patterns/{pattern}'
            if pattern_dir.exists():
                target_dir = self.target / f'scripts/{pattern}'
                self.copy_directory(pattern_dir, target_dir)

        # Add CI/CD configurations
        self.copy_file(
            self.source / 'templates/advanced/.github/workflows/cli-agent.yml',
            self.target / '.github/workflows/cli-agent.yml'
        )

    def copy_file(self, source, target, customize=False, merge=False):
        """Copy a single file with options"""
        if not source.exists():
            print(f"  ⚠ Source not found: {source.name}")
            return

        action = "Would copy" if self.dry_run else "Copying"

        if target.exists() and merge:
            action = "Would merge" if self.dry_run else "Merging"

        print(f"  {action}: {source.name} -> {target.relative_to(self.target.parent)}")

        if not self.dry_run:
            # Create parent directories
            target.parent.mkdir(parents=True, exist_ok=True)

            if merge and target.exists():
                # Merge logic (for Makefiles, etc.)
                self.merge_files(source, target)
            else:
                # Direct copy
                shutil.copy2(source, target)

            if customize:
                self.customize_file(target)

        self.installed.append(str(target.relative_to(self.target)))

    def copy_directory(self, source, target):
        """Copy entire directory"""
        if not source.exists():
            return

        action = "Would copy" if self.dry_run else "Copying"
        print(f"  {action} directory: {source.name} -> {target.relative_to(self.target.parent)}")

        if not self.dry_run:
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(source, target)

        self.installed.append(str(target.relative_to(self.target)))

    def create_dir(self, path):
        """Create directory if it doesn't exist"""
        if not path.exists():
            action = "Would create" if self.dry_run else "Creating"
            print(f"  {action} directory: {path.relative_to(self.target.parent)}")
            if not self.dry_run:
                path.mkdir(parents=True, exist_ok=True)

    def create_symlink(self, source_name, link_name):
        """Create symlink for backward compatibility"""
        link_path = self.target / link_name
        action = "Would create" if self.dry_run else "Creating"
        print(f"  {action} symlink: {link_name} -> {source_name}")

        if not self.dry_run:
            # Remove existing file/link if it exists
            if link_path.exists() or link_path.is_symlink():
                link_path.unlink()

            # Create symlink
            try:
                link_path.symlink_to(source_name)
            except OSError:
                # If symlinks aren't supported, create a copy instead
                print(f"    Note: Symlinks not supported, creating copy instead")
                source_path = self.target / source_name
                if source_path.exists():
                    shutil.copy2(source_path, link_path)

    def customize_file(self, file_path):
        """Customize template variables in file"""
        if not file_path.exists():
            return

        content = file_path.read_text()

        # Replace template variables
        project_name = self.target.name
        content = content.replace('{{PROJECT_NAME}}', project_name)
        content = content.replace('{{PROJECT_PATH}}', str(self.target))

        # Detect project type
        if (self.target / 'package.json').exists():
            content = content.replace('{{PROJECT_TYPE}}', 'JavaScript/Node.js')
            content = content.replace('{{TEST_COMMAND}}', 'npm test')
        elif (self.target / 'requirements.txt').exists() or (self.target / 'setup.py').exists():
            content = content.replace('{{PROJECT_TYPE}}', 'Python')
            content = content.replace('{{TEST_COMMAND}}', 'python -m pytest')
        else:
            content = content.replace('{{PROJECT_TYPE}}', 'Generic')
            content = content.replace('{{TEST_COMMAND}}', 'make test')

        file_path.write_text(content)

    def merge_files(self, source, target):
        """Merge two files (mainly for Makefiles)"""
        # Simple append for now
        source_content = source.read_text()
        target_content = target.read_text()

        if "CLI Agent Template" not in target_content:
            with open(target, 'a') as f:
                f.write("\n\n# CLI Agent Template Commands\n")
                f.write(source_content)

    def create_config(self):
        """Create .cli-agent.yaml configuration file"""
        config_path = self.target / '.cli-agent.yaml'

        config = {
            'template': {
                'source': 'github.com/aget-framework/aget',
                'version': '1.0.0',
                'template': self.template,
                'installed': self.installed
            },
            'patterns': {
                'session_management': {'version': '1.0.0', 'installed': True},
            }
        }

        if self.template in ['standard', 'advanced']:
            config['patterns']['housekeeping'] = {'version': '1.0.0', 'installed': True}

        if self.template == 'advanced':
            config['patterns']['recovery'] = {'version': '1.0.0', 'installed': True}
            config['patterns']['documentation'] = {'version': '1.0.0', 'installed': True}

        action = "Would create" if self.dry_run else "Creating"
        print(f"\n{action} configuration: .cli-agent.yaml")

        if not self.dry_run:
            import yaml
            with open(config_path, 'w') as f:
                yaml.dump(config, f, default_flow_style=False)

    def report(self):
        """Report installation summary"""
        print("\n" + "=" * 50)
        print("Installation Summary")
        print("=" * 50)

        if self.dry_run:
            print("DRY RUN - No files were actually modified")
        else:
            print(f"Installed {len(self.installed)} files")

        print("\nInstalled components:")
        for item in self.installed:
            print(f"  ✓ {item}")

        print("\n🎉 CLI Agent Template installation complete!")
        print("\nNext steps:")
        print("  1. Review CLAUDE.md for available commands")
        print("  2. Say 'wake up' to your CLI agent to start")
        print("  3. Customize patterns as needed for your project")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Install CLI Agent Template into a project'
    )
    parser.add_argument(
        'target',
        help='Target project directory'
    )
    parser.add_argument(
        '--template',
        choices=['minimal', 'standard', 'advanced'],
        default='standard',
        help='Template level to install'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview what would be installed without making changes'
    )

    args = parser.parse_args()

    installer = TemplateInstaller(
        args.target,
        template=args.template,
        dry_run=args.dry_run
    )

    success = installer.install()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    # Handle missing PyYAML gracefully
    try:
        import yaml
    except ImportError:
        print("Note: PyYAML not installed. Config file creation will be skipped.")
        print("Install with: pip install pyyaml")

    main()