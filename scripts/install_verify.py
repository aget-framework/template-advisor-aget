#!/usr/bin/env python3
"""
Install verification script
Tests that the installer works correctly in a temporary directory
"""

import os
import sys
import tempfile
import shutil
import subprocess
from pathlib import Path

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

class InstallVerifier:
    """Verify CLI Agent Template installation"""

    def __init__(self):
        self.repo_root = Path(__file__).parent.parent
        self.installer_path = self.repo_root / 'installer/install.py'
        self.test_results = []

    def run(self):
        """Run all verification tests"""
        print(f"\n{BOLD}{BLUE}🔍 Install Verification - Testing Installer{RESET}")
        print(f"Repository: {self.repo_root.name}")
        print("=" * 50)

        # Test all template types
        templates = ['minimal', 'standard', 'advanced']

        for template in templates:
            if not self.test_template_install(template):
                return 1

        # Test dry-run mode
        if not self.test_dry_run():
            return 1

        # Test file customization
        if not self.test_customization():
            return 1

        # Print summary
        self.print_summary()
        return 0 if all(self.test_results) else 1

    def test_template_install(self, template):
        """Test installation of a specific template"""
        print(f"\n{BOLD}Testing {template} template...{RESET}")

        with tempfile.TemporaryDirectory() as tmpdir:
            test_dir = Path(tmpdir) / 'test_project'
            test_dir.mkdir()

            # Create a minimal project structure
            (test_dir / 'README.md').write_text('# Test Project')

            # Run installer
            result = subprocess.run(
                [sys.executable, str(self.installer_path), str(test_dir), '--template', template],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                print(f"  {RED}✗ Installation failed{RESET}")
                print(f"  Error: {result.stderr}")
                self.test_results.append(False)
                return False

            # Verify expected files exist
            expected_files = {
                'minimal': ['AGENTS.md', 'CLAUDE.md', 'scripts/session_protocol.py', 'Makefile'],
                'standard': ['AGENTS.md', 'CLAUDE.md', 'scripts/session_protocol.py',
                            'scripts/health_check.py', 'Makefile'],
                'advanced': ['AGENTS.md', 'CLAUDE.md', 'scripts/session_protocol.py',
                            'scripts/health_check.py', 'Makefile']
            }

            missing = []
            for expected in expected_files.get(template, []):
                if not (test_dir / expected).exists():
                    missing.append(expected)

            if missing:
                print(f"  {RED}✗ Missing files: {', '.join(missing)}{RESET}")
                self.test_results.append(False)
                return False

            # Verify CLAUDE.md is a symlink (or copy)
            claude_path = test_dir / 'CLAUDE.md'
            if claude_path.is_symlink():
                print(f"  {GREEN}✓ CLAUDE.md symlink created{RESET}")
            elif claude_path.exists():
                print(f"  {YELLOW}✓ CLAUDE.md copy created (symlinks not supported){RESET}")
            else:
                print(f"  {RED}✗ CLAUDE.md not created{RESET}")
                self.test_results.append(False)
                return False

            print(f"  {GREEN}✓ {template.capitalize()} template installed successfully{RESET}")
            self.test_results.append(True)
            return True

    def test_dry_run(self):
        """Test dry-run mode"""
        print(f"\n{BOLD}Testing dry-run mode...{RESET}")

        with tempfile.TemporaryDirectory() as tmpdir:
            test_dir = Path(tmpdir) / 'test_project'
            test_dir.mkdir()

            # Run installer in dry-run mode
            result = subprocess.run(
                [sys.executable, str(self.installer_path), str(test_dir), '--dry-run'],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                print(f"  {RED}✗ Dry-run failed{RESET}")
                self.test_results.append(False)
                return False

            # Verify no files were created
            files_created = list(test_dir.glob('*'))
            if files_created:
                print(f"  {RED}✗ Dry-run created files: {files_created}{RESET}")
                self.test_results.append(False)
                return False

            print(f"  {GREEN}✓ Dry-run mode works correctly{RESET}")
            self.test_results.append(True)
            return True

    def test_customization(self):
        """Test file customization (template variable replacement)"""
        print(f"\n{BOLD}Testing file customization...{RESET}")

        with tempfile.TemporaryDirectory() as tmpdir:
            test_dir = Path(tmpdir) / 'my_awesome_project'
            test_dir.mkdir()

            # Create Python project indicators
            (test_dir / 'requirements.txt').write_text('pytest\n')

            # Run installer
            subprocess.run(
                [sys.executable, str(self.installer_path), str(test_dir), '--template', 'minimal'],
                capture_output=True,
                text=True
            )

            # Check AGENTS.md was customized
            agents_content = (test_dir / 'AGENTS.md').read_text()

            errors = []
            if '{{PROJECT_NAME}}' in agents_content:
                errors.append('PROJECT_NAME not replaced')
            if 'my_awesome_project' not in agents_content:
                errors.append('Project name not inserted')
            if '{{PROJECT_TYPE}}' in agents_content:
                errors.append('PROJECT_TYPE not replaced')
            if 'Python' not in agents_content:
                errors.append('Python project type not detected')

            if errors:
                print(f"  {RED}✗ Customization failed: {', '.join(errors)}{RESET}")
                self.test_results.append(False)
                return False

            print(f"  {GREEN}✓ File customization works correctly{RESET}")
            self.test_results.append(True)
            return True

    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 50)
        print(f"{BOLD}Summary{RESET}")
        print("=" * 50)

        passed = sum(self.test_results)
        total = len(self.test_results)

        if passed == total:
            print(f"{GREEN}✅ All {total} tests passed!{RESET}")
            print(f"{GREEN}✅ Installer verified and working correctly{RESET}")
        else:
            print(f"{RED}❌ {passed}/{total} tests passed{RESET}")
            print(f"{RED}❌ Installer needs fixes{RESET}")

def main():
    """Main entry point"""
    verifier = InstallVerifier()
    return verifier.run()

if __name__ == '__main__':
    exit(main())