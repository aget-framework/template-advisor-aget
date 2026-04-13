#!/usr/bin/env python3
"""
Housekeeping Protocol for CLI Agent Template
Simplified version for the template repository
"""

import os
import sys
import shutil
import argparse
from pathlib import Path
from datetime import datetime, timedelta

# ANSI colors
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
RESET = '\033[0m'


class DocumentationChecker:
    """Check documentation quality"""

    def __init__(self):
        self.issues = []

    def run(self):
        """Run documentation checks"""
        print(f"\n{BOLD}{BLUE}📚 Documentation Quality Check{RESET}")
        print("=" * 50)

        # Check for required docs
        required = ['README.md', 'AGENTS.md', 'LICENSE']
        for doc in required:
            if not Path(doc).exists():
                self.issues.append(f"Missing: {doc}")

        # Check README length
        if Path('README.md').exists():
            lines = Path('README.md').read_text().splitlines()
            if len(lines) < 50:
                self.issues.append("README.md seems too short")
            elif len(lines) > 500:
                self.issues.append("README.md might be too long")

        # Check for pattern documentation
        pattern_dirs = Path('patterns').glob('*') if Path('patterns').exists() else []
        for pattern_dir in pattern_dirs:
            if pattern_dir.is_dir():
                readme = pattern_dir / 'README.md'
                if not readme.exists():
                    self.issues.append(f"Missing docs: {pattern_dir.name}/README.md")

        # Calculate grade
        if len(self.issues) == 0:
            grade = 'A'
            color = GREEN
        elif len(self.issues) <= 2:
            grade = 'B'
            color = GREEN
        elif len(self.issues) <= 4:
            grade = 'C'
            color = YELLOW
        else:
            grade = 'D'
            color = RED

        # Report
        if self.issues:
            print(f"\n{YELLOW}Issues found:{RESET}")
            for issue in self.issues:
                print(f"  - {issue}")

        print(f"\n{BOLD}Grade: {color}{grade}{RESET}")
        return len(self.issues) == 0


class HousekeepingCleaner:
    """Light cleanup operations"""

    def __init__(self, dry_run=True):
        self.dry_run = dry_run
        self.cleaned = []

    def run(self):
        """Run housekeeping"""
        print(f"\n{BOLD}{BLUE}🧹 Housekeeping - Light Cleanup{RESET}")
        print("=" * 50)

        if self.dry_run:
            print(f"{YELLOW}DRY RUN MODE{RESET}\n")

        # Clean Python artifacts
        for pattern in ['__pycache__', '*.pyc', '.pytest_cache']:
            for item in Path('.').rglob(pattern):
                if not self.dry_run:
                    if item.is_dir():
                        shutil.rmtree(item)
                    else:
                        item.unlink()
                self.cleaned.append(str(item))
                print(f"  {'Would remove' if self.dry_run else 'Removed'}: {item}")

        # Clean .DS_Store files
        for ds_store in Path('.').rglob('.DS_Store'):
            if not self.dry_run:
                ds_store.unlink()
            self.cleaned.append(str(ds_store))
            print(f"  {'Would remove' if self.dry_run else 'Removed'}: {ds_store}")

        print(f"\n{BOLD}Cleaned {len(self.cleaned)} items{RESET}")
        return True


class SpringCleaner:
    """Deep cleanup operations"""

    def __init__(self, dry_run=True):
        self.dry_run = dry_run
        self.operations = []

    def run(self):
        """Run spring cleaning"""
        print(f"\n{BOLD}{BLUE}🌸 Spring Cleaning - Deep Cleanup{RESET}")
        print("=" * 50)

        if self.dry_run:
            print(f"{YELLOW}DRY RUN MODE{RESET}\n")

        # Archive old session notes
        session_dir = Path('SESSION_NOTES')
        if session_dir.exists():
            cutoff = datetime.now() - timedelta(days=30)
            for note in session_dir.glob('*.md'):
                mtime = datetime.fromtimestamp(note.stat().st_mtime)
                if mtime < cutoff:
                    archive_dir = Path('archive/session_notes')
                    if not self.dry_run:
                        archive_dir.mkdir(parents=True, exist_ok=True)
                        shutil.move(str(note), str(archive_dir / note.name))
                    self.operations.append(f"Archive {note.name}")
                    print(f"  {'Would archive' if self.dry_run else 'Archived'}: {note.name}")

        # Remove empty directories
        for dirpath in Path('.').rglob('*'):
            if dirpath.is_dir() and not any(dirpath.iterdir()):
                if '.git' not in str(dirpath):
                    if not self.dry_run:
                        dirpath.rmdir()
                    self.operations.append(f"Remove empty {dirpath}")
                    print(f"  {'Would remove' if self.dry_run else 'Removed'} empty: {dirpath}")

        print(f"\n{BOLD}Operations: {len(self.operations)}{RESET}")
        return True


class SanityChecker:
    """Emergency diagnostics"""

    def run(self):
        """Run sanity check"""
        print(f"\n{BOLD}{RED}🚨 Sanity Check - Emergency Diagnostic{RESET}")
        print("=" * 50)

        issues = []

        # Check Python
        import sys
        version = sys.version.split()[0]
        major, minor = map(int, version.split('.')[:2])
        if major == 3 and minor >= 8:
            print(f"  ✓ Python {version}")
        else:
            issues.append(f"Python {version} (need 3.8+)")
            print(f"  ✗ Python {version} (need 3.8+)")

        # Check git
        import subprocess
        try:
            subprocess.run(['git', 'status'], capture_output=True, check=True)
            print(f"  ✓ Git repository OK")
        except:
            issues.append("Git not working")
            print(f"  ✗ Git not working")

        # Check critical files
        critical = ['AGENTS.md', 'README.md']
        for file in critical:
            if Path(file).exists():
                print(f"  ✓ {file} present")
            else:
                issues.append(f"Missing {file}")
                print(f"  ✗ Missing {file}")

        # Check pattern directories
        if Path('patterns').exists():
            print(f"  ✓ Patterns directory present")
        else:
            issues.append("Missing patterns directory")
            print(f"  ✗ Missing patterns directory")

        # Status
        if not issues:
            print(f"\n{GREEN}System Status: OK{RESET}")
        elif len(issues) <= 2:
            print(f"\n{YELLOW}System Status: DEGRADED{RESET}")
        else:
            print(f"\n{RED}System Status: CRITICAL{RESET}")

        return len(issues) == 0


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Housekeeping Protocol')
    parser.add_argument('command', choices=[
        'documentation-check', 'housekeeping', 'spring-clean', 'sanity-check'
    ])
    parser.add_argument('--dry-run', action='store_true', default=True)
    parser.add_argument('--no-dry-run', dest='dry_run', action='store_false')

    args = parser.parse_args()

    if args.command == 'documentation-check':
        checker = DocumentationChecker()
        checker.run()
    elif args.command == 'housekeeping':
        cleaner = HousekeepingCleaner(dry_run=args.dry_run)
        cleaner.run()
    elif args.command == 'spring-clean':
        cleaner = SpringCleaner(dry_run=args.dry_run)
        cleaner.run()
    elif args.command == 'sanity-check':
        checker = SanityChecker()
        checker.run()


if __name__ == '__main__':
    main()