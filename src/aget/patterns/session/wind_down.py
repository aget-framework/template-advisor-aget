"""Wind down session - save work and create notes

Implements: L468 (Session Script Re-entrancy Guard)
"""

import subprocess
import json
from pathlib import Path
from datetime import datetime

DESCRIPTION = "Save work with commit and session notes"
CATEGORY = "session"

# L468: Session guard for re-entrancy protection
_guard = None

def _get_guard(agent_path=None):
    """Get or create SessionGuard instance."""
    global _guard
    if _guard is None:
        try:
            from src.aget.patterns.session.session_guard import SessionGuard
            _guard = SessionGuard('wind_down', agent_path or Path.cwd())
        except ImportError:
            pass
    return _guard


def apply(dry_run=False, force=False):
    """Apply the wind down pattern

    Args:
        dry_run: If True, show what would be done without doing it
        force: If True, bypass re-entrancy guard cooldown (L468)

    Returns:
        True on success, False on failure, None if blocked by guard
    """

    if dry_run:
        print("  Would perform:")
        print("    - Git add all changes")
        print("    - Commit with timestamp")
        print("    - Create session notes")
        print("    - Update session state")
        return True

    # L468: Re-entrancy guard check
    guard = _get_guard()
    if guard:
        allowed, message = guard.should_proceed(force=force)
        if not allowed:
            print(f"⚠️ Wind down blocked: {message}")
            return None
        if message:  # Warning (automation detection)
            print(message)
        if not guard.acquire_lock():
            print("⚠️ Wind down already running (concurrent invocation blocked)")
            return None

    print("\n" + "=" * 60)
    print("WIND DOWN SESSION")
    print("=" * 60)

    try:
        cwd = Path.cwd()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        # Find the git repository root
        git_root_result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, cwd=cwd
        )

        if git_root_result.returncode != 0:
            print("✗ Not in a git repository")
            return False

        git_root = Path(git_root_result.stdout.strip())
        print(f"📁 Repository root: {git_root}")

        # Check for changes
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            timeout=2,
            cwd=git_root,
        )

        if result.returncode != 0:
            print("✗ Failed to check git status")
            return False

        if result.stdout.strip():
            print("📝 Found uncommitted changes")

            # Add all changes
            add_result = subprocess.run(
                ["git", "add", "-A"], capture_output=True, text=True, cwd=git_root
            )

            if add_result.returncode != 0:
                print("✗ Failed to stage changes")
                return False

            # Commit changes
            commit_msg = f"Session save: {timestamp}"
            commit_result = subprocess.run(
                ["git", "commit", "-m", commit_msg],
                capture_output=True,
                text=True,
                cwd=git_root,
            )

            if commit_result.returncode == 0:
                # Extract commit SHA
                sha_result = subprocess.run(
                    ["git", "rev-parse", "HEAD"],
                    capture_output=True,
                    text=True,
                    cwd=git_root,
                )
                sha = (
                    sha_result.stdout.strip()[:7]
                    if sha_result.returncode == 0
                    else "unknown"
                )
                print(f"✅ Committed changes: {sha}")
            else:
                print("✗ Failed to commit")
                return False
        else:
            print("✅ No changes to commit")

        # Create session notes
        notes_dir = cwd / "sessions"
        notes_dir.mkdir(exist_ok=True)

        session_date = datetime.now().strftime("%Y-%m-%d")
        notes_file = notes_dir / f"session_{session_date}.md"

        # Get session number
        session_file = cwd / ".session_state.json"
        session_num = 1
        if session_file.exists():
            try:
                data = json.loads(session_file.read_text())
                session_num = data.get("session_number", 1)
            except Exception:
                pass

        # Append to notes
        with open(notes_file, "a") as f:
            f.write(f"\n## Session #{session_num} - {timestamp}\n")
            f.write("- Ended with wind down protocol\n")

            # Add git log of recent commits
            log_result = subprocess.run(
                ["git", "log", "--oneline", "-5"],
                capture_output=True,
                text=True,
                cwd=git_root,
            )
            if log_result.returncode == 0 and log_result.stdout.strip():
                f.write("\nRecent commits:\n")
                for line in log_result.stdout.strip().split("\n"):
                    f.write(f"  - {line}\n")

        print(f"📝 Created session notes: {notes_file.name}")

        # Update session state
        if session_file.exists():
            try:
                data = json.loads(session_file.read_text())
                data["last_wind_down"] = datetime.now().isoformat()
                session_file.write_text(json.dumps(data, indent=2))
            except Exception:
                pass

        print("\n✅ Session saved successfully")
        print("   • Changes committed")
        print("   • Notes created")
        print("   • State updated")
        print("=" * 60)

        # L468: Record successful invocation
        if guard:
            guard.record_invocation()

        return True

    finally:
        # L468: Always release lock on exit
        if guard:
            guard.release_lock()
