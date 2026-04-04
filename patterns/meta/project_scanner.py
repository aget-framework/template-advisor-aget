#!/usr/bin/env python3
"""
AGET Project Scanner
Scans all sub-projects in meta-repository for AGET migration readiness

Exit Codes:
  0 - All projects fully migrated
  1 - Partial migration (some projects migrated)
  2 - No migration started
  3 - Script execution error

Usage:
  python3 project_scanner.py [options]

Options:
  --quiet, -q      Minimal output (just summary)
  --verbose, -v    Detailed output with debug info
  --json           Output in JSON format
  --no-save        Don't save report to .aget/project_scan.json
  --exit-zero      Always exit with 0 (for CI/CD compatibility)
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from enum import Enum


class MigrationStatus(Enum):
    """Migration status levels for AGET projects"""
    COMPLETE = 'complete'
    PARTIAL = 'partial'
    NOT_STARTED = 'not_started'
    CUSTOMIZED = 'customized'

    def __str__(self):
        return self.value


class ProjectScanner:
    """Scans projects for AGET compatibility and migration status"""

    def __init__(self, root_path = None):
        self.root = Path(root_path) if root_path else Path.cwd()
        self.projects = {}
        self.summary = {
            'total_projects': 0,
            'migrated': 0,
            'partial': 0,
            'not_started': 0,
            'customized': 0
        }
        self.results = {
            'scan_date': datetime.now().isoformat(),
            'root_path': str(self.root),
            'projects': {},
            'summary': {
                'total': 0,
                'git_repos': 0,
                'has_claude_md': 0,
                'has_agents_md': 0,
                'has_aget_version': 0,
                'fully_migrated': 0,
                'partially_migrated': 0,
                'not_started': 0
            }
        }

    def is_git_repo(self, path: Path) -> bool:
        """Check if directory is a git repository"""
        return (path / '.git').exists()

    def check_file_exists(self, path: Path, filename: str) -> bool:
        """Check if a file exists in the given path"""
        return (path / filename).exists()

    def read_aget_version(self, path: Path) -> Optional[Dict]:
        """Read AGET version info if present"""
        version_file = path / '.aget' / 'version.json'
        if version_file.exists():
            try:
                with open(version_file) as f:
                    return json.load(f)
            except:
                return None
        return None

    def check_agents_md_header(self, path: Path) -> Optional[str]:
        """Check AGENTS.md for @aget-version header"""
        agents_file = path / 'AGENTS.md'
        if agents_file.exists():
            try:
                with open(agents_file) as f:
                    for line in f:
                        if '@aget-version:' in line:
                            return line.strip()
                        if line.startswith('##'):  # Stop at first section
                            break
            except:
                pass
        return None

    def extract_version_from_agents_md(self, path: Path) -> Optional[str]:
        """Extract version number from AGENTS.md header"""
        agents_file = path / 'AGENTS.md'
        if agents_file.exists():
            try:
                with open(agents_file) as f:
                    for line in f:
                        if '@aget-version:' in line:
                            # Extract version from line like "# @aget-version: 2.1.0-beta"
                            version = line.split('@aget-version:')[1].strip()
                            return version
                        if line.startswith('##'):  # Stop at first section
                            break
            except:
                pass
        return None

    def detect_compatibility_files(self, path: Path) -> List[str]:
        """Detect compatibility files for other agents"""
        compatibility_files = []
        known_files = [
            '.cursorrules',
            '.aider.conf.yml',
            '.aider.conf.yaml',
            '.claude.md',
            'cursor.toml',
            'aider.toml'
        ]

        for filename in known_files:
            if (path / filename).exists():
                compatibility_files.append(filename)

        return compatibility_files

    def calculate_migration_score(self, analysis: Dict) -> int:
        """Calculate migration score based on project analysis"""
        score = 0

        # AGET migration indicators
        if analysis['has_agents_md']:
            score += 25
        if analysis.get('has_aget_dir'):
            score += 25
        if analysis['aget_version']:
            score += 15

        # Pattern structure
        if analysis['has_patterns_dir']:
            score += 15
        if analysis.get('has_session_protocols'):
            score += 10
        if analysis.get('has_housekeeping_protocols'):
            score += 10

        # Base score for having a git repo (only if some migration features exist)
        if analysis['is_git_repo'] and score > 0:
            score += 10

        # Check for custom patterns (bonus points)
        patterns_count = len(analysis.get('pattern_categories', []))
        if patterns_count > 4:  # More than basic session/housekeeping
            score += min(20, (patterns_count - 4) * 5)

        return min(100, score)

    def detect_pattern_categories(self, path: Path) -> List[str]:
        """Detect pattern categories in patterns directory"""
        patterns_dir = path / 'patterns'
        if not patterns_dir.exists():
            return []

        categories = []
        for item in patterns_dir.iterdir():
            if item.is_dir():
                categories.append(item.name)
        return categories

    def analyze_project(self, project_path: Path) -> Dict:
        """Analyze a single project for AGET status"""
        project_name = project_path.name if project_path.name != '.' else project_path.parent.name

        # Skip non-directories and hidden directories (except current directory)
        if not project_path.is_dir() or (project_name.startswith('.') and project_name != '.'):
            return None

        # Basic file checks
        has_claude_md = self.check_file_exists(project_path, 'CLAUDE.md')
        has_agents_md = self.check_file_exists(project_path, 'AGENTS.md')
        has_patterns_dir = self.check_file_exists(project_path, 'patterns')
        has_scripts_dir = self.check_file_exists(project_path, 'scripts')
        has_aget_dir = self.check_file_exists(project_path, '.aget')

        # Session protocol checks
        has_session_protocols = (
            self.check_file_exists(project_path, 'scripts/aget_session_protocol.py') or
            self.check_file_exists(project_path, 'scripts/session_protocol.py')
        )
        has_housekeeping_protocols = self.check_file_exists(project_path, 'scripts/health_check.py')

        # Get pattern categories
        pattern_categories = self.detect_pattern_categories(project_path)

        # Get compatibility files
        compatibility_files = self.detect_compatibility_files(project_path)

        # Get AGET version info
        aget_info = self.read_aget_version(project_path)
        aget_version = None
        migration_date = None
        if aget_info:
            aget_version = aget_info.get('aget_version') or aget_info.get('version')
            migration_date = aget_info.get('migration_date')

        # Try to extract version from AGENTS.md if not in .aget/version.json
        if not aget_version and has_agents_md:
            aget_version = self.extract_version_from_agents_md(project_path)

        analysis = {
            'name': project_name,
            'path': str(project_path),
            'is_git_repo': self.is_git_repo(project_path),
            'has_claude_md': has_claude_md,
            'has_agents_md': has_agents_md,
            'has_makefile': self.check_file_exists(project_path, 'Makefile'),
            'has_patterns_dir': has_patterns_dir,
            'has_scripts_dir': has_scripts_dir,
            'has_aget_dir': has_aget_dir,
            'has_session_protocols': has_session_protocols,
            'has_housekeeping_protocols': has_housekeeping_protocols,
            'aget_version': aget_version,
            'migration_date': migration_date,
            'pattern_categories': pattern_categories,
            'compatibility_files': compatibility_files,
            'legacy_files': [],
            'patterns_adopted': [],
            'patterns_missing': [],
            'agents_md_header': self.check_agents_md_header(project_path)
        }

        # Determine legacy files
        if has_claude_md:
            analysis['legacy_files'].append('CLAUDE.md')

        # Determine patterns adopted and missing
        if has_agents_md:
            analysis['patterns_adopted'].append('AGENTS.md')
        if has_aget_dir:
            analysis['patterns_adopted'].append('.aget directory')
        if has_session_protocols:
            analysis['patterns_adopted'].append('session protocols')
        if has_housekeeping_protocols:
            analysis['patterns_adopted'].append('housekeeping protocols')

        # Patterns missing
        if not has_agents_md:
            analysis['patterns_missing'].append('AGENTS.md')
        if not has_aget_dir:
            analysis['patterns_missing'].append('.aget directory')
        if not has_session_protocols:
            analysis['patterns_missing'].append('session protocols')
        if not has_housekeeping_protocols:
            analysis['patterns_missing'].append('housekeeping protocols')

        # Determine migration status
        if aget_info:
            status = aget_info.get('status', aget_info.get('phase', 'unknown'))
            if status in ('fully_migrated', 'complete'):
                analysis['migration_status'] = MigrationStatus.COMPLETE
            elif status in ('partially_migrated', 'partial'):
                analysis['migration_status'] = MigrationStatus.PARTIAL
            elif status in ('claude_compatible', 'customized'):
                analysis['migration_status'] = MigrationStatus.CUSTOMIZED
            else:
                analysis['migration_status'] = MigrationStatus.NOT_STARTED
        else:
            # Logic-based detection
            if has_agents_md and has_aget_dir and has_session_protocols and has_housekeeping_protocols:
                # Check for customized status (extra patterns)
                if len(pattern_categories) > 4:
                    analysis['migration_status'] = MigrationStatus.CUSTOMIZED
                else:
                    analysis['migration_status'] = MigrationStatus.COMPLETE
            elif has_agents_md or has_patterns_dir or has_session_protocols:
                analysis['migration_status'] = MigrationStatus.PARTIAL
            else:
                # Legacy project with CLAUDE.md should be NOT_STARTED, not CUSTOMIZED
                analysis['migration_status'] = MigrationStatus.NOT_STARTED

        # Calculate score
        analysis['score'] = self.calculate_migration_score(analysis)

        return analysis

    def scan_directory(self, project_path: Path) -> Dict:
        """Alias for analyze_project to maintain backwards compatibility"""
        return self.analyze_project(project_path)

    def scan_all_projects(self) -> Dict:
        """Scan all subdirectories for projects"""
        # Check if the root directory itself is a project
        root_analysis = self.analyze_project(self.root)
        if root_analysis and root_analysis['is_git_repo']:
            self.projects['.'] = root_analysis
            self.update_new_summary(root_analysis)

        # Scan subdirectories
        for item in self.root.iterdir():
            # Skip certain directories
            if item.name in ['scripts', 'patterns', 'SESSION_NOTES', '.git', '__pycache__',
                            'scripts.backup', '.aget', 'node_modules', '.venv', 'venv']:
                continue

            analysis = self.analyze_project(item)
            if analysis and analysis['is_git_repo']:
                self.projects[item.name] = analysis
                self.update_new_summary(analysis)

        return self.results

    def update_new_summary(self, analysis: Dict):
        """Update new summary structure expected by tests"""
        self.summary['total_projects'] += 1

        status = analysis['migration_status']
        if status == MigrationStatus.COMPLETE:
            self.summary['migrated'] += 1
        elif status == MigrationStatus.PARTIAL:
            self.summary['partial'] += 1
        elif status == MigrationStatus.CUSTOMIZED:
            self.summary['customized'] += 1
        else:  # NOT_STARTED
            self.summary['not_started'] += 1

    def update_summary(self, analysis: Dict):
        """Update summary statistics"""
        s = self.results['summary']
        s['total'] += 1

        if analysis['is_git_repo']:
            s['git_repos'] += 1
        if analysis['has_claude_md']:
            s['has_claude_md'] += 1
        if analysis['has_agents_md']:
            s['has_agents_md'] += 1
        if analysis['aget_version']:
            s['has_aget_version'] += 1

        status = analysis['migration_status']
        if status == 'fully_migrated':
            s['fully_migrated'] += 1
        elif status in ['partially_migrated', 'migrating']:
            s['partially_migrated'] += 1
        elif status in ['not_started', 'claude_compatible']:
            s['not_started'] += 1

    def print_report(self):
        """Print a formatted report of scan results"""
        print("\n" + "="*60)
        print("AGET Migration Status Report")
        print("="*60)
        print(f"Scan Date: {self.results['scan_date']}")
        print(f"Root Path: {self.results['root_path']}")
        print("\n" + "-"*60)
        print("SUMMARY")
        print("-"*60)

        s = self.results['summary']
        print(f"Total Git Repositories: {s['git_repos']}")
        print(f"├─ With CLAUDE.md: {s['has_claude_md']}")
        print(f"├─ With AGENTS.md: {s['has_agents_md']}")
        print(f"└─ With AGET version: {s['has_aget_version']}")
        print()
        print(f"Migration Status:")
        print(f"├─ Fully Migrated: {s['fully_migrated']}")
        print(f"├─ Partially Migrated: {s['partially_migrated']}")
        print(f"└─ Not Started: {s['not_started']}")

        print("\n" + "-"*60)
        print("PROJECT DETAILS")
        print("-"*60)

        # Sort projects by migration status
        projects_by_status = {}
        for name, proj in self.results['projects'].items():
            status = proj['migration_status']
            if status not in projects_by_status:
                projects_by_status[status] = []
            projects_by_status[status].append(proj)

        # Display by status groups
        status_order = ['fully_migrated', 'partially_migrated', 'migrating',
                       'claude_compatible', 'not_started', 'not_applicable']

        status_symbols = {
            'fully_migrated': '✅',
            'partially_migrated': '🔄',
            'migrating': '🔄',
            'claude_compatible': '📝',
            'not_started': '⏳',
            'not_applicable': '➖'
        }

        for status in status_order:
            if status in projects_by_status:
                print(f"\n{status_symbols.get(status, '?')} {status.replace('_', ' ').upper()}:")
                for proj in sorted(projects_by_status[status], key=lambda x: x['name']):
                    indicators = []
                    if proj['has_agents_md']:
                        indicators.append('AGENTS.md')
                    if proj['has_claude_md']:
                        indicators.append('CLAUDE.md')
                    if proj['has_patterns_dir']:
                        indicators.append('patterns/')
                    if proj['aget_version']:
                        indicators.append(f"v{proj['aget_version']}")

                    indicator_str = f" [{', '.join(indicators)}]" if indicators else ""
                    print(f"  • {proj['name']}{indicator_str}")

        print("\n" + "="*60)

    def generate_report(self, format: str = 'text') -> str:
        """Generate report in specified format"""
        if format == 'json':
            return self.generate_json_report()
        else:
            return self.generate_text_report()

    def generate_text_report(self) -> str:
        """Generate text format report"""
        lines = []
        lines.append("AGET Migration Status Report")
        lines.append("=" * 60)
        lines.append(f"Total Projects: {self.summary['total_projects']}")
        lines.append(f"Migrated: {self.summary['migrated']}")
        lines.append(f"Partial: {self.summary['partial']}")
        lines.append(f"Not Started: {self.summary['not_started']}")
        lines.append("")

        for name, project in self.projects.items():
            lines.append(f"Project: {name}")
            lines.append(f"  Score: {project['score']}")
            lines.append(f"  Status: {project['migration_status'].value}")
            lines.append(f"  Recommendations:")
            if project['patterns_missing']:
                for pattern in project['patterns_missing']:
                    lines.append(f"    - Add {pattern}")
            lines.append("")

        return "\n".join(lines)

    def generate_json_report(self) -> str:
        """Generate JSON format report"""
        report_data = {
            'summary': self.summary,
            'projects': {}
        }

        for name, project in self.projects.items():
            # Convert MigrationStatus enum to string for JSON serialization
            project_copy = project.copy()
            project_copy['migration_status'] = project['migration_status'].value
            report_data['projects'][name] = project_copy

        return json.dumps(report_data, indent=2)

    def save_report(self, filename: str = None) -> Path:
        """Save scan results to file"""
        if not filename:
            filename = 'migration_report.json'

        output_path = self.root / filename

        # Save JSON report
        json_content = self.generate_json_report()
        with open(output_path, 'w') as f:
            f.write(json_content)

        # Save text report
        text_filename = filename.replace('.json', '.txt')
        text_path = self.root / text_filename
        text_content = self.generate_text_report()
        with open(text_path, 'w') as f:
            f.write(text_content)

        return output_path


def main():
    """Main entry point with argument parsing and error handling"""
    parser = argparse.ArgumentParser(
        description='Scan projects for AGET migration status',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exit Codes:
  0 - All projects fully migrated
  1 - Partial migration (some projects migrated)
  2 - No migration started
  3 - Script execution error
        """
    )
    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Minimal output (just summary)')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Detailed output with debug info')
    parser.add_argument('--json', action='store_true',
                        help='Output in JSON format')
    parser.add_argument('--no-save', action='store_true',
                        help="Don't save report to .aget/project_scan.json")
    parser.add_argument('--exit-zero', action='store_true',
                        help='Always exit with 0 (for CI/CD compatibility)')

    args = parser.parse_args()

    try:
        scanner = ProjectScanner()

        # Set verbosity level
        if args.verbose:
            print(f"[DEBUG] Scanning root directory: {scanner.root}", file=sys.stderr)

        results = scanner.scan_all_projects()

        # Output based on format preference
        if args.json:
            print(json.dumps(results, indent=2))
        elif args.quiet:
            s = results['summary']
            print(f"Migration: {s['fully_migrated']}/{s['git_repos']} projects")
            if s['partially_migrated'] > 0:
                print(f"In progress: {s['partially_migrated']} projects")
        else:
            scanner.print_report()

        # Save report unless disabled
        if not args.no_save:
            scanner.save_report('project_scan.json')
        elif args.verbose:
            print("[DEBUG] Skipping report save (--no-save)", file=sys.stderr)

        # Determine exit code
        if args.exit_zero:
            return 0

        if results['summary']['git_repos'] == 0:
            return 2  # No repos found
        elif results['summary']['fully_migrated'] == results['summary']['git_repos']:
            return 0  # All migrated
        elif results['summary']['has_agents_md'] > 0:
            return 1  # Some migration
        else:
            return 2  # No migration

    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        return 3
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc(file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())