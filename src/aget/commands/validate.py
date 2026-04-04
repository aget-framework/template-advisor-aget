#!/usr/bin/env python3
"""
AGET Validate Command - Pattern and Configuration Validator

Validates:
- Pattern syntax and structure
- Configuration file format
- Required files exist
- Dependencies are available
- Pattern compatibility
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import importlib.util
import ast


class PatternValidator:
    """Validate pattern files for compliance."""

    def __init__(self, pattern_path: Path):
        self.path = pattern_path
        self.errors = []
        self.warnings = []

    def validate(self) -> bool:
        """Validate a single pattern file."""
        if not self.path.exists():
            self.errors.append(f"Pattern file not found: {self.path}")
            return False

        # Check Python syntax
        try:
            with open(self.path, 'r') as f:
                ast.parse(f.read())
        except SyntaxError as e:
            self.errors.append(f"Syntax error: {e}")
            return False

        # Check for required functions/classes
        module_name = self.path.stem
        spec = importlib.util.spec_from_file_location(module_name, self.path)
        if not spec or not spec.loader:
            self.errors.append(f"Cannot load pattern: {self.path}")
            return False

        try:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Check for main() function or run() method
            if not hasattr(module, 'main') and not hasattr(module, 'run'):
                self.warnings.append("Pattern has no main() or run() entry point")

        except Exception as e:
            self.errors.append(f"Import error: {e}")
            return False

        return len(self.errors) == 0


class ConfigValidator:
    """Validate AGENTS.md and other configuration files."""

    def __init__(self, config_path: Path):
        self.path = config_path
        self.errors = []
        self.warnings = []

    def validate(self) -> bool:
        """Validate configuration file."""
        if not self.path.exists():
            self.errors.append(f"Configuration file not found: {self.path}")
            return False

        try:
            content = self.path.read_text()

            # Check for required sections
            required_sections = [
                "## Session Management Protocols",
                "## Project Context"
            ]

            for section in required_sections:
                if section not in content:
                    self.warnings.append(f"Missing recommended section: {section}")

            # Check for version information
            if '@aget-version:' not in content:
                self.warnings.append("No @aget-version tag found")

            # Check minimum length
            if len(content) < 100:
                self.warnings.append("Configuration file seems too short")

        except Exception as e:
            self.errors.append(f"Cannot read configuration: {e}")
            return False

        return len(self.errors) == 0


class ProjectValidator:
    """Validate entire project structure and compliance."""

    def __init__(self, project_path: Path = Path('.')):
        self.path = project_path
        self.errors = []
        self.warnings = []
        self.checks_passed = 0
        self.checks_total = 0

    def validate_structure(self) -> bool:
        """Validate project directory structure."""
        self.checks_total += 1

        # Check for AGENTS.md
        agents_file = self.path / 'AGENTS.md'
        if not agents_file.exists():
            # Check for CLAUDE.md as fallback
            claude_file = self.path / 'CLAUDE.md'
            if claude_file.exists():
                self.warnings.append("Using CLAUDE.md (consider renaming to AGENTS.md)")
                agents_file = claude_file
            else:
                self.errors.append("No AGENTS.md or CLAUDE.md found")
                return False

        self.checks_passed += 1

        # Validate configuration
        self.checks_total += 1
        config_validator = ConfigValidator(agents_file)
        if config_validator.validate():
            self.checks_passed += 1
        else:
            self.errors.extend(config_validator.errors)

        self.warnings.extend(config_validator.warnings)

        return True

    def validate_patterns(self) -> bool:
        """Validate all patterns in patterns/ directory."""
        patterns_dir = self.path / 'patterns'
        if not patterns_dir.exists():
            self.warnings.append("No patterns/ directory found")
            return True

        pattern_files = list(patterns_dir.rglob('*.py'))

        for pattern_file in pattern_files:
            if pattern_file.name.startswith('__'):
                continue

            self.checks_total += 1
            validator = PatternValidator(pattern_file)

            if validator.validate():
                self.checks_passed += 1
            else:
                self.errors.append(f"Pattern {pattern_file.stem}: {', '.join(validator.errors)}")

            if validator.warnings:
                self.warnings.append(f"Pattern {pattern_file.stem}: {', '.join(validator.warnings)}")

        return True

    def validate_scripts(self) -> bool:
        """Validate protocol scripts."""
        scripts_dir = self.path / 'scripts'
        if not scripts_dir.exists():
            self.warnings.append("No scripts/ directory found")
            return True

        # Check for session protocols
        session_scripts = [
            'aget_session_protocol.py',
            'session_protocol.py'
        ]

        self.checks_total += 1
        if any((scripts_dir / script).exists() for script in session_scripts):
            self.checks_passed += 1
        else:
            self.warnings.append("No session protocol script found")

        # Check for housekeeping protocols
        housekeeping_scripts = [
            'health_check.py',
            'housekeeping_protocol.py'
        ]

        self.checks_total += 1
        if any((scripts_dir / script).exists() for script in housekeeping_scripts):
            self.checks_passed += 1
        else:
            self.warnings.append("No housekeeping protocol script found")

        return True

    def validate_dependencies(self) -> bool:
        """Check Python version and required modules."""
        self.checks_total += 1

        # Check Python version
        if sys.version_info < (3, 8):
            self.errors.append(f"Python 3.8+ required, found {sys.version}")
            return False

        self.checks_passed += 1

        # Check for .aget directory
        self.checks_total += 1
        aget_dir = self.path / '.aget'
        if aget_dir.exists():
            self.checks_passed += 1

            # Check for version.json
            version_file = aget_dir / 'version.json'
            if version_file.exists():
                try:
                    with open(version_file) as f:
                        data = json.load(f)
                        if 'version' not in data:
                            self.warnings.append("version.json missing 'version' field")
                except Exception as e:
                    self.warnings.append(f"Cannot parse version.json: {e}")
        else:
            self.warnings.append("No .aget directory found")

        return True

    def generate_report(self) -> str:
        """Generate validation report."""
        lines = []
        lines.append("=" * 60)
        lines.append("AGET Configuration Validation Report")
        lines.append("=" * 60)

        # Overall status
        status = "✅ PASSED" if len(self.errors) == 0 else "❌ FAILED"
        lines.append(f"\nStatus: {status}")
        lines.append(f"Checks: {self.checks_passed}/{self.checks_total} passed")

        # Errors
        if self.errors:
            lines.append(f"\n❌ Errors ({len(self.errors)}):")
            for error in self.errors:
                lines.append(f"  • {error}")

        # Warnings
        if self.warnings:
            lines.append(f"\n⚠️  Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                lines.append(f"  • {warning}")

        # Recommendations
        if self.errors or self.warnings:
            lines.append("\n📋 Recommendations:")

            if "No AGENTS.md" in str(self.errors):
                lines.append("  1. Run: aget init")

            if "No session protocol" in str(self.warnings):
                lines.append("  2. Run: aget apply session/wake")

            if "No patterns/ directory" in str(self.warnings):
                lines.append("  3. Run: aget apply --list")

            if "@aget-version" in str(self.warnings):
                lines.append("  4. Add @aget-version tag to AGENTS.md")

        else:
            lines.append("\n✅ All validation checks passed!")
            lines.append("Your project is properly configured for AGET.")

        lines.append("\n" + "=" * 60)
        return "\n".join(lines)

    def validate_all(self) -> bool:
        """Run all validations."""
        self.validate_structure()
        self.validate_patterns()
        self.validate_scripts()
        self.validate_dependencies()

        return len(self.errors) == 0


def main():
    """Main entry point for aget validate command."""
    parser = argparse.ArgumentParser(
        description='Validate AGET configuration and patterns'
    )
    parser.add_argument(
        'path',
        nargs='?',
        default='.',
        help='Path to project (default: current directory)'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output in JSON format'
    )
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Quiet mode - only show errors'
    )
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Treat warnings as errors'
    )

    args = parser.parse_args()

    # Run validation
    project_path = Path(args.path)
    validator = ProjectValidator(project_path)
    is_valid = validator.validate_all()

    # Handle strict mode
    if args.strict and validator.warnings:
        is_valid = False

    # Output results
    if args.json:
        result = {
            'valid': is_valid,
            'checks_passed': validator.checks_passed,
            'checks_total': validator.checks_total,
            'errors': validator.errors,
            'warnings': validator.warnings
        }
        print(json.dumps(result, indent=2))
    elif args.quiet:
        if not is_valid:
            for error in validator.errors:
                print(f"Error: {error}")
    else:
        print(validator.generate_report())

    # Exit code
    if not is_valid:
        return 1
    elif validator.warnings and not args.strict:
        return 0  # Success with warnings
    else:
        return 0


if __name__ == '__main__':
    sys.exit(main())