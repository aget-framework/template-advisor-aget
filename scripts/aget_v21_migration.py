#!/usr/bin/env python3
"""
AGET v2.1.0 Migration Script
Implements the new ownership standard for clear separation between
framework and agent files.

Usage:
    python3 scripts/aget_v21_migration.py [--check|--apply]
"""

import os
import sys
import shutil
from pathlib import Path
from typing import List, Tuple

class V21Migration:
    """Handle migration to v2.1 ownership standard."""

    def __init__(self, root_path: str = "."):
        self.root = Path(root_path).resolve()
        self.scripts_dir = self.root / "scripts"
        self.aget_dir = self.root / ".aget"
        self.changes = []

    def check_migrations_needed(self) -> List[str]:
        """Check what migrations are needed."""
        needed = []

        # Check for framework scripts without aget_ prefix
        framework_scripts = [
            "housekeeping_protocol.py",
            "session_protocol.py",
            "check_file_permissions.py",
            "pre-release.sh",
        ]

        for script in framework_scripts:
            old_path = self.scripts_dir / script
            if old_path.exists():
                new_name = f"aget_{script.replace('-', '_')}"
                needed.append(f"Rename: {script} → {new_name}")

        # Check for custom scripts with aget_ prefix (warn only)
        if self.scripts_dir.exists():
            # List of known framework scripts that should have aget_ prefix
            framework_scripts_with_prefix = [
                "health_check.py",
                "aget_session_protocol.py",
                "aget_check_permissions.py",
                "aget_pre_release.sh",
                "aget_v21_migration.py",
            ]

            for script in self.scripts_dir.glob("aget_*"):
                # Skip if it's a known framework script
                if script.name not in framework_scripts_with_prefix:
                    needed.append(f"WARNING: Unknown script has aget_ prefix: {script.name}")

        return needed

    def apply_migrations(self, dry_run: bool = True) -> bool:
        """Apply the v2.1 migrations."""
        print("Applying v2.1.0 Ownership Standard Migrations...")
        print("=" * 60)

        success = True

        # 1. Rename framework scripts to have aget_ prefix
        renames = [
            ("check_file_permissions.py", "aget_check_permissions.py"),
            ("pre-release.sh", "aget_pre_release.sh"),
        ]

        for old_name, new_name in renames:
            old_path = self.scripts_dir / old_name
            new_path = self.scripts_dir / new_name

            if old_path.exists() and not new_path.exists():
                if dry_run:
                    print(f"Would rename: {old_name} → {new_name}")
                else:
                    old_path.rename(new_path)
                    print(f"✅ Renamed: {old_name} → {new_name}")

                    # Update execute permissions if needed
                    if new_name.endswith('.py') or new_name.endswith('.sh'):
                        new_path.chmod(0o755)

        # 2. Create OWNERSHIP.md to document the standard
        ownership_doc = self.aget_dir / "OWNERSHIP.md"
        if not ownership_doc.exists():
            if dry_run:
                print(f"Would create: .aget/OWNERSHIP.md")
            else:
                self.create_ownership_doc(ownership_doc)
                print(f"✅ Created: .aget/OWNERSHIP.md")

        # 3. Update symlinks if needed
        # (Already handled by existing symlinks)

        return success

    def create_ownership_doc(self, path: Path) -> None:
        """Create the OWNERSHIP.md documentation."""
        content = """# AGET File Ownership Guide

## Quick Rule
- **Files starting with `aget_`** = Framework files (DO NOT MODIFY)
- **Everything else** = Your agent's files (safe to modify)

## Directory Ownership

### Framework-Owned (Don't Modify)
- `.aget/` - All AGET framework files
- `scripts/aget_*.py` - Framework scripts
- `scripts/aget_*.sh` - Framework scripts

### Agent-Owned (Your Files)
- `src/` - Your agent's source code
- `workspace/` - Your working directory
- `products/` - Products you create
- `data/` - Your data storage
- `scripts/*.py` (without aget_ prefix) - Your custom scripts
- `patterns/` - Your custom patterns

## Examples

### Framework Files (Don't Edit These)
```
scripts/aget_session_protocol.py
scripts/health_check.py
scripts/aget_pre_release.sh
.aget/patterns/
```

### Your Files (Safe to Edit)
```
scripts/my_release_tool.py
src/agent_logic.py
workspace/experiments/
products/release_notes.md
```

## Why This Matters
This separation ensures:
1. AGET updates won't overwrite your work
2. You know which files are safe to modify
3. Clear boundaries between framework and agent code

---
*AGET v2.1.0 - Clear Ownership Standard*
"""
        path.parent.mkdir(exist_ok=True)
        path.write_text(content)

    def report(self) -> None:
        """Generate migration report."""
        needed = self.check_migrations_needed()

        if not needed:
            print("✅ No migrations needed - already v2.1 compliant!")
        else:
            print("Migrations needed for v2.1.0 compliance:")
            print("-" * 40)
            for item in needed:
                if item.startswith("WARNING"):
                    print(f"⚠️  {item}")
                else:
                    print(f"• {item}")
            print("\nRun with --apply to perform migrations")

def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='AGET v2.1.0 Migration Tool')
    parser.add_argument('--check', action='store_true', help='Check what needs migration')
    parser.add_argument('--apply', action='store_true', help='Apply migrations')
    parser.add_argument('--path', default='.', help='Path to project root')

    args = parser.parse_args()

    migrator = V21Migration(args.path)

    if args.apply:
        migrator.apply_migrations(dry_run=False)
    else:
        migrator.report()

if __name__ == "__main__":
    main()