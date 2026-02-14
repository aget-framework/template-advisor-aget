#!/usr/bin/env python3
"""
Wind Down Protocol - Generic Template

End session for any AGET agent with proper state capture and sanity checks.
Designed to work across CLI agents (Claude Code, Codex CLI, Cursor, etc.).

Implements: CAP-SESSION-003 (Wind Down Protocol), R-WIND-001-*
Patterns: L038 (Agent-Agnostic), L021 (Verify-Before-Modify), L039 (Diagnostic Efficiency), L468 (Re-entrancy Guard)

Usage:
    python3 wind_down.py                    # Human-readable output
    python3 wind_down.py --json             # JSON output (for programmatic use)
    python3 wind_down.py --json --pretty    # Pretty-printed JSON
    python3 wind_down.py --dir /path/agent  # Run on specific agent
    python3 wind_down.py --notes "..."      # Add handoff notes
    python3 wind_down.py --skip-sanity      # Skip sanity check (not recommended)
    python3 wind_down.py --force            # Bypass re-entrancy guard (L468)

Exit codes:
    0: Clean close (sanity healthy)
    1: Close with warnings
    2: Close with errors (requires acknowledgment in interactive mode)
    3: Configuration error
    4: Re-entrancy guard block (cooldown active or concurrent invocation)

L021 Verification Table:
    | Check | Resource | Before Action |
    |-------|----------|---------------|
    | 1 | session_state.json | Load to calculate duration |
    | 2 | housekeeping | Run sanity check before summary |
    | 3 | planning/ | Scan for pending work |
    | 4 | sessions/ | Verify exists before writing |

Author: private-aget-framework-AGET (canonical template)
Version: 1.2.0 (v3.4.0) - WD-007 commit message suggestion
"""

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional


# =============================================================================
# L039: Diagnostic Efficiency - Timing
# =============================================================================

_start_time = time.time()


def log_diagnostic(msg: str) -> None:
    """Log diagnostic message to stderr (L039: diagnostics to stderr)."""
    elapsed = (time.time() - _start_time) * 1000
    print(f"[{elapsed:.0f}ms] {msg}", file=sys.stderr)


# =============================================================================
# Core Functions
# =============================================================================

def find_agent_root(start_path: Optional[Path] = None) -> Optional[Path]:
    """
    Find agent root by looking for .aget/ directory.

    L021: Verify .aget/ exists before proceeding.
    """
    if start_path:
        path = Path(start_path).resolve()
    else:
        path = Path.cwd()

    # Check current and up to 3 parent levels
    for _ in range(4):
        if (path / '.aget').is_dir():
            return path
        if path.parent == path:
            break
        path = path.parent

    return None


def load_json_file(path: Path, default: Any = None) -> Any:
    """
    Load JSON file with default fallback.

    L021: Verify file exists before reading.
    """
    if not path.exists():
        return default
    try:
        with open(path) as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return default


def run_sanity_check(agent_path: Path, verbose: bool = False) -> Dict[str, Any]:
    """
    Run housekeeping sanity check.

    L021 Check 2: Run sanity before generating summary.
    """
    # Try to find housekeeping script
    script_locations = [
        agent_path / '.aget' / 'patterns' / 'session' / 'sanity_check.py',
        agent_path / '.aget' / 'patterns' / 'session' / 'housekeeping.py',
        Path(__file__).parent / 'aget_housekeeping_protocol.py',
    ]

    script_path = None
    for loc in script_locations:
        if loc.exists():
            script_path = loc
            break

    if not script_path:
        # Return minimal result if no script found
        return {
            'status': 'unknown',
            'checks_passed': 0,
            'checks_total': 0,
            'warnings': 0,
            'errors': 0,
            'message': 'No sanity check script found'
        }

    try:
        result = subprocess.run(
            ['python3', str(script_path), '--json', '--dir', str(agent_path)],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.stdout:
            data = json.loads(result.stdout)
            return {
                'status': data.get('status', 'unknown'),
                'checks_passed': data.get('summary', {}).get('passed', 0),
                'checks_total': data.get('summary', {}).get('total', 0),
                'warnings': data.get('summary', {}).get('warnings', 0),
                'errors': data.get('summary', {}).get('errors', 0),
                'message': ''
            }
    except (subprocess.TimeoutExpired, json.JSONDecodeError, Exception) as e:
        if verbose:
            log_diagnostic(f"Sanity check error: {e}")

    return {
        'status': 'error',
        'checks_passed': 0,
        'checks_total': 0,
        'warnings': 0,
        'errors': 1,
        'message': 'Sanity check failed to execute'
    }


def get_session_state(agent_path: Path) -> Dict[str, Any]:
    """
    Load session state if available.

    L021 Check 1: Load session_state.json to calculate duration.
    """
    state_file = agent_path / '.aget' / 'session_state.json'
    return load_json_file(state_file, {})


def calculate_duration(session_state: Dict[str, Any]) -> Optional[int]:
    """
    Calculate session duration from start time.

    WD-008 helper: Calculate duration for session log.

    Returns:
        Duration in seconds, or None if cannot calculate.
    """
    started_str = session_state.get('started')
    if not started_str:
        return None

    try:
        started = datetime.fromisoformat(started_str)
        duration = datetime.now() - started
        return int(duration.total_seconds())
    except (ValueError, TypeError):
        return None


def write_session_log(agent_path: Path, data: Dict[str, Any], description: str = "session") -> Path:
    """
    Create session log file per SESSION_LOG_SPEC_v1.0.

    Per SKILL_VOCABULARY Wind_Down_Protocol:
    "Structured session ending with notes, commit staging, and sanity checks"

    WD-008: The SKILL shall create a session log file in sessions/ with
    session summary and handoff notes.

    Returns path to created file.
    """
    import re

    sessions_dir = agent_path / 'sessions'
    sessions_dir.mkdir(exist_ok=True)

    date_str = datetime.now().strftime('%Y-%m-%d')
    safe_desc = re.sub(r'[^a-z0-9_-]', '_', description.lower())[:50]
    filename = f"SESSION_{date_str}_{safe_desc}.md"
    filepath = sessions_dir / filename

    # Avoid overwrite - append counter if exists
    counter = 1
    while filepath.exists():
        filename = f"SESSION_{date_str}_{safe_desc}_{counter}.md"
        filepath = sessions_dir / filename
        counter += 1

    # Format content
    content = format_session_log_content(data)
    filepath.write_text(content)

    return filepath


def format_session_log_content(data: Dict[str, Any]) -> str:
    """
    Format session log content per SESSION_LOG_SPEC.

    Returns markdown content for session file.
    """
    lines = []
    agent_name = data.get('agent_name', 'unknown')
    duration = format_duration(data['session'].get('duration_seconds'))

    lines.append(f"# SESSION: {agent_name}")
    lines.append("")
    lines.append(f"**Date**: {datetime.now().strftime('%Y-%m-%d')}")
    lines.append(f"**Duration**: {duration}")
    lines.append(f"**Status**: Complete")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Sanity check summary
    sanity = data.get('sanity_check', {})
    status = sanity.get('status', 'unknown')
    passed = sanity.get('checks_passed', 0)
    total = sanity.get('checks_total', 0)
    lines.append("## Sanity Check")
    lines.append("")
    lines.append(f"- Status: {status.upper()}")
    lines.append(f"- Passed: {passed}/{total}")
    lines.append("")

    # Pending work
    pending = data.get('pending_work', [])
    if pending:
        lines.append("## Pending Work")
        lines.append("")
        for item in pending:
            lines.append(f"- {item}")
        lines.append("")

    # Handoff notes
    notes = data.get('handoff_notes', '')
    if notes:
        lines.append("## Handoff Notes")
        lines.append("")
        lines.append(notes)
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("*Session log created by wind_down.py (WD-008)*")

    return "\n".join(lines)


def scan_pending_work(agent_path: Path) -> List[str]:
    """
    Scan planning/ for in-progress work.

    L021 Check 3: Scan planning/ directory.
    """
    pending = []
    planning_dir = agent_path / 'planning'

    if not planning_dir.is_dir():
        return pending

    for plan_file in planning_dir.glob('PROJECT_PLAN_*.md'):
        try:
            content = plan_file.read_text()
            # Look for in_progress or IN_PROGRESS markers
            if 'IN_PROGRESS' in content.upper() or 'status: in_progress' in content.lower():
                pending.append(plan_file.name)
        except IOError:
            pass

    return pending


def generate_commit_message(agent_path: Path) -> str:
    """
    Generate suggested commit message based on git status.

    WD-007: The SKILL shall suggest a commit message based on session activity.

    Returns:
        Suggested commit message or empty string if no changes.
    """
    try:
        # Get git status
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            cwd=agent_path,
            capture_output=True,
            text=True,
            timeout=5
        )

        if not result.stdout.strip():
            return "No changes to commit"

        lines = result.stdout.strip().split('\n')

        # Categorize changes
        categories = {
            'evolution': [],   # .aget/evolution/
            'specs': [],       # .aget/specs/
            'sessions': [],    # sessions/
            'planning': [],    # planning/
            'docs': [],        # .md, .txt
            'config': [],      # .yaml, .json, .toml
            'code': [],        # .py, .sh
            'skills': [],      # .claude/skills/
            'other': []
        }

        for line in lines:
            if len(line) < 4:
                continue
            filepath = line[3:].strip()

            if '.aget/evolution/' in filepath:
                categories['evolution'].append(filepath)
            elif '.aget/specs/' in filepath:
                categories['specs'].append(filepath)
            elif 'sessions/' in filepath:
                categories['sessions'].append(filepath)
            elif 'planning/' in filepath:
                categories['planning'].append(filepath)
            elif '.claude/skills/' in filepath:
                categories['skills'].append(filepath)
            elif filepath.endswith(('.md', '.txt')):
                categories['docs'].append(filepath)
            elif filepath.endswith(('.yaml', '.yml', '.json', '.toml')):
                categories['config'].append(filepath)
            elif filepath.endswith(('.py', '.sh')):
                categories['code'].append(filepath)
            else:
                categories['other'].append(filepath)

        # Generate message based on categories (priority order)
        parts = []
        if categories['evolution']:
            count = len(categories['evolution'])
            parts.append(f"learn: Add {count} L-doc{'s' if count > 1 else ''}")
        if categories['sessions']:
            parts.append("session: Add session log")
        if categories['planning']:
            parts.append("plan: Update project plans")
        if categories['specs']:
            parts.append("spec: Update specifications")
        if categories['skills']:
            parts.append("skill: Update skills")
        if categories['code']:
            parts.append("feat: Update scripts")
        if categories['docs']:
            parts.append("docs: Update documentation")
        if categories['config']:
            parts.append("chore: Update config")
        if categories['other']:
            count = len(categories['other'])
            parts.append(f"chore: Update {count} file{'s' if count > 1 else ''}")

        if not parts:
            return f"chore: Update {len(lines)} file{'s' if len(lines) > 1 else ''}"

        # Return primary action, note if more
        if len(parts) == 1:
            return parts[0]
        else:
            return f"{parts[0]} + {len(parts) - 1} more"

    except subprocess.TimeoutExpired:
        return "Unable to generate commit message (timeout)"
    except Exception:
        return "Unable to generate commit message"


def get_wind_down_data(agent_path: Path,
                       skip_sanity: bool = False,
                       handoff_notes: str = "",
                       verbose: bool = False) -> Dict[str, Any]:
    """
    Gather all data needed for wind down output.

    Returns structured dict suitable for JSON or human output.
    """
    now = datetime.now()

    data = {
        'timestamp': now.isoformat(),
        'agent_path': str(agent_path),
        'session': {
            'ended': now.isoformat(),
            'started': None,
            'duration_seconds': None,
        },
        'sanity_check': {},
        'pending_work': [],
        'handoff_notes': handoff_notes,
        'clean_close': True,
    }

    # L021 Check 1: Session state (WU-008 format: 'started' at root level)
    session_state = get_session_state(agent_path)
    started_str = session_state.get('started')
    if started_str:
        data['session']['started'] = started_str
        data['session']['duration_seconds'] = calculate_duration(session_state)
    else:
        # Legacy format fallback
        current = session_state.get('current_session', {})
        if current.get('started'):
            data['session']['started'] = current['started']
            try:
                started = datetime.fromisoformat(current['started'])
                data['session']['duration_seconds'] = int((now - started).total_seconds())
            except ValueError:
                pass

    # L021 Check 2: Sanity check
    if skip_sanity:
        data['sanity_check'] = {
            'status': 'skipped',
            'checks_passed': 0,
            'checks_total': 0,
            'warnings': 0,
            'errors': 0,
            'message': 'Sanity check skipped by user'
        }
    else:
        if verbose:
            log_diagnostic("Running sanity check...")
        data['sanity_check'] = run_sanity_check(agent_path, verbose)

    # L021 Check 3: Pending work
    data['pending_work'] = scan_pending_work(agent_path)

    # WD-007: Generate suggested commit message
    data['suggested_commit'] = generate_commit_message(agent_path)

    # Determine clean close
    sanity_status = data['sanity_check'].get('status', 'unknown')
    if sanity_status == 'error':
        data['clean_close'] = False
    elif sanity_status == 'warning':
        data['clean_close'] = True  # Warnings allow close

    # Load agent identity for display
    version_file = agent_path / '.aget' / 'version.json'
    version_data = load_json_file(version_file, {})
    data['agent_name'] = version_data.get('agent_name', agent_path.name)

    return data


def format_duration(seconds: Optional[int]) -> str:
    """Format duration in human-readable form."""
    if seconds is None:
        return "unknown"

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60

    if hours > 0:
        return f"{hours}h {minutes}m"
    elif minutes > 0:
        return f"{minutes}m"
    else:
        return f"{seconds}s"


def format_human_output(data: Dict[str, Any]) -> str:
    """Format data for human-readable output."""
    lines = []

    # Session header
    agent_name = data.get('agent_name', 'unknown')
    lines.append(f"\n**Session Complete: {agent_name}**")

    # Duration
    duration = format_duration(data['session'].get('duration_seconds'))
    lines.append(f"**Duration**: {duration}")
    lines.append("")

    # Sanity check
    sanity = data['sanity_check']
    status = sanity.get('status', 'unknown')
    passed = sanity.get('checks_passed', 0)
    total = sanity.get('checks_total', 0)

    if status == 'healthy':
        lines.append(f"Sanity Check: [+] HEALTHY ({passed}/{total} passed)")
    elif status == 'warning':
        warnings = sanity.get('warnings', 0)
        lines.append(f"Sanity Check: [!] WARNING ({passed}/{total} passed, {warnings} warnings)")
    elif status == 'error':
        errors = sanity.get('errors', 0)
        lines.append(f"Sanity Check: [x] ERROR ({passed}/{total} passed, {errors} errors)")
    elif status == 'skipped':
        lines.append("Sanity Check: [-] SKIPPED")
    else:
        lines.append(f"Sanity Check: [?] {status.upper()}")

    lines.append("")

    # Pending work
    pending = data['pending_work']
    if pending:
        lines.append("Pending Work:")
        for item in pending:
            lines.append(f"  - {item}")
    else:
        lines.append("Pending Work: None")

    lines.append("")

    # Handoff notes
    if data['handoff_notes']:
        lines.append(f"Handoff Notes: {data['handoff_notes']}")
        lines.append("")

    # Suggested commit (WD-007)
    if data.get('suggested_commit'):
        lines.append(f"Suggested commit: {data['suggested_commit']}")
        lines.append("")

    # Close confirmation
    if data['clean_close']:
        lines.append("Clean close confirmed.")
    else:
        lines.append("Session has issues - review sanity check results.")

    lines.append("")

    return "\n".join(lines)


# =============================================================================
# Main
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Wind down protocol for AGET agents (v3.1 template)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
L021 Verification Table:
  1. session_state.json - Load to calculate duration
  2. housekeeping - Run sanity check before summary
  3. planning/ - Scan for pending work
  4. sessions/ - Verify exists before writing

Exit codes:
  0 - Clean close (healthy)
  1 - Close with warnings
  2 - Close with errors
  3 - Configuration error
        """
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output as JSON'
    )
    parser.add_argument(
        '--pretty',
        action='store_true',
        help='Pretty-print JSON output'
    )
    parser.add_argument(
        '--dir',
        type=Path,
        help='Agent directory (default: current directory)'
    )
    parser.add_argument(
        '--notes',
        type=str,
        default='',
        help='Handoff notes for next session'
    )
    parser.add_argument(
        '--skip-sanity',
        action='store_true',
        help='Skip sanity check (not recommended)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable diagnostic output to stderr'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Bypass re-entrancy guard cooldown (L468)'
    )
    parser.add_argument(
        '--version',
        action='version',
        version='wind_down.py 1.2.0 (AGET v3.4.0, WD-007 commit suggestion)'
    )

    args = parser.parse_args()

    # L039: Diagnostic timing
    if args.verbose:
        log_diagnostic("Starting wind_down protocol")

    # Find agent root
    agent_path = find_agent_root(args.dir)

    if not agent_path:
        if args.json:
            error = {
                'clean_close': False,
                'errors': ['Could not find .aget/ directory'],
            }
            print(json.dumps(error, indent=2 if args.pretty else None))
        else:
            print("Error: Could not find .aget/ directory", file=sys.stderr)
        return 3

    if args.verbose:
        log_diagnostic(f"Found agent at: {agent_path}")

    # L468: Re-entrancy guard check
    guard = None
    try:
        # Try to import guard module (may not exist in all installations)
        sys.path.insert(0, str(agent_path))
        from src.aget.patterns.session.session_guard import SessionGuard
        guard = SessionGuard('wind_down', agent_path)

        allowed, message = guard.should_proceed(force=args.force)

        if not allowed:
            if args.json:
                error = {
                    'clean_close': False,
                    'errors': [f'Re-entrancy guard: {message}'],
                    'guard_blocked': True,
                }
                print(json.dumps(error, indent=2 if args.pretty else None))
            else:
                print(f"Blocked: {message}", file=sys.stderr)
            return 4  # New exit code for guard block

        if message and args.verbose:
            log_diagnostic(f"Guard: {message}")

        # Acquire lock for concurrent execution protection
        if not guard.acquire_lock():
            if args.json:
                error = {
                    'clean_close': False,
                    'errors': ['Wind down already running (concurrent invocation)'],
                    'guard_blocked': True,
                }
                print(json.dumps(error, indent=2 if args.pretty else None))
            else:
                print("Error: Wind down already running", file=sys.stderr)
            return 4

        if args.verbose:
            log_diagnostic("Guard: Lock acquired")

    except ImportError:
        # Guard module not available - continue without it
        if args.verbose:
            log_diagnostic("Guard: Module not available, proceeding without protection")

    # Gather data
    data = get_wind_down_data(
        agent_path,
        skip_sanity=args.skip_sanity,
        handoff_notes=args.notes,
        verbose=args.verbose
    )

    if args.verbose:
        log_diagnostic(f"Data gathered, clean_close={data['clean_close']}")

    # WD-008: Create session log file
    try:
        # Generate description from handoff notes or default
        description = "session"
        if args.notes:
            # Use first few words of notes as description
            words = args.notes.split()[:3]
            description = '_'.join(words) if words else "session"

        session_file = write_session_log(agent_path, data, description)
        data['session_file'] = str(session_file)

        if args.verbose:
            log_diagnostic(f"Session log written: {session_file}")
    except (IOError, OSError) as e:
        if args.verbose:
            log_diagnostic(f"Warning: Could not write session log: {e}")

    # Output
    if args.json:
        print(json.dumps(data, indent=2 if args.pretty else None))
    else:
        print(format_human_output(data))

    if args.verbose:
        elapsed = (time.time() - _start_time) * 1000
        log_diagnostic(f"Complete in {elapsed:.0f}ms")

    # L468: Record successful invocation and release lock
    if guard:
        guard.record_invocation()
        guard.release_lock()
        if args.verbose:
            log_diagnostic("Guard: Invocation recorded, lock released")

    # Exit code based on sanity status
    sanity_status = data['sanity_check'].get('status', 'unknown')
    if sanity_status == 'error':
        return 2
    elif sanity_status == 'warning':
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
