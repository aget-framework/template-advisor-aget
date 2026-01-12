"""
Session Script Re-entrancy Guard (L468)

Prevents automation loops in session scripts by enforcing cooldown periods,
atomic locking, and automation pattern detection.

Usage:
    from src.aget.patterns.session.session_guard import SessionGuard

    guard = SessionGuard('wind_down', agent_path)
    allowed, message = guard.should_proceed(force=args.force)

    if not allowed:
        print(f"Blocked: {message}")
        return 1

    if not guard.acquire_lock():
        print("Already running")
        return 1

    try:
        # ... script logic ...
        guard.record_invocation()
    finally:
        guard.release_lock()

CLI Compatibility: Works with Claude Code, Cursor, Aider, Windsurf, and any
Python-compatible CLI agent.

Best Practices Sources:
- Baeldung: https://www.baeldung.com/linux/bash-ensure-instance-running
- DEV Community: https://dev.to/mochafreddo/understanding-the-use-of-flock-in-linux-cron-jobs
- Better Stack: https://betterstack.com/community/questions/how-to-prevent-duplicate-cron-jobs
"""

from pathlib import Path
from typing import Tuple, Optional
import time
import json
import fcntl
import os
import atexit
import signal

# Default configurations per script type
SCRIPT_CONFIGS = {
    'wind_down': {
        'cooldown_seconds': 300,      # 5 minutes
        'automation_threshold': 3,     # warn after 3 invocations in window
        'automation_window': 1800,     # 30 minute window
    },
    'session_protocol': {
        'cooldown_seconds': 60,        # 1 minute (shorter for session creation)
        'automation_threshold': 5,
        'automation_window': 600,      # 10 minute window
    },
    'default': {
        'cooldown_seconds': 300,
        'automation_threshold': 3,
        'automation_window': 1800,
    }
}


class SessionGuard:
    """
    Reusable re-entrancy guard for session scripts.

    Prevents automation loops by:
    1. Enforcing cooldown period between invocations (atomic locking)
    2. Detecting rapid repeated invocations (automation pattern)
    3. Providing bypass for legitimate emergency use
    4. Automatic cleanup on normal/abnormal exit

    Enhanced with industry best practices:
    - fcntl.flock() for atomic locking (no race conditions)
    - PID tracking for stale lock detection
    - atexit handlers for cleanup on abnormal exit

    Pattern: L468 (Session Script Re-entrancy Guard)
    """

    def __init__(self, script_name: str, agent_path: Optional[Path] = None):
        """
        Initialize guard for a specific script.

        Args:
            script_name: Name of the script (e.g., 'wind_down', 'session_protocol')
            agent_path: Path to agent root (defaults to cwd)
        """
        self.script_name = script_name
        self.agent_path = Path(agent_path) if agent_path else Path.cwd()
        self.config = SCRIPT_CONFIGS.get(script_name, SCRIPT_CONFIGS['default'])
        self.lock_file = self.agent_path / '.aget' / f'.{script_name}.lock'
        self.history_file = self.agent_path / '.aget' / f'.{script_name}_history'
        self._lock_fd = None
        self._registered_cleanup = False

    def should_proceed(self, force: bool = False) -> Tuple[bool, str]:
        """
        Check if script should proceed.

        Args:
            force: If True, bypass cooldown check

        Returns:
            Tuple of (allowed, message):
            - allowed: True if script should proceed
            - message: Empty if allowed, explanation if blocked, warning if automation detected
        """
        self._cleanup_stale_lock()

        if force:
            return True, "Force flag set - bypassing guard"

        # Check cooldown
        if self._is_in_cooldown():
            remaining = self._get_cooldown_remaining()
            return False, f"Cooldown active ({remaining}s remaining). Use --force to bypass."

        # Check automation loop (warn but don't block)
        if self._is_automation_loop():
            threshold = self.config['automation_threshold']
            window_min = self.config['automation_window'] // 60
            return True, f"Warning: Possible automation loop detected (>{threshold} {self.script_name} in {window_min} min)"

        return True, ""

    def acquire_lock(self) -> bool:
        """
        Acquire atomic lock using fcntl.flock().

        Returns:
            True if lock acquired, False if already locked (concurrent invocation)
        """
        self.lock_file.parent.mkdir(parents=True, exist_ok=True)

        try:
            self._lock_fd = open(self.lock_file, 'w')
            fcntl.flock(self._lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)

            # Write lock metadata for stale detection
            lock_data = {
                'pid': os.getpid(),
                'timestamp': time.time(),
                'script': self.script_name
            }
            self._lock_fd.write(json.dumps(lock_data))
            self._lock_fd.flush()

            # Register cleanup handlers (once per guard instance)
            if not self._registered_cleanup:
                atexit.register(self.release_lock)
                # Store original handlers to chain them
                self._orig_sigterm = signal.signal(signal.SIGTERM, self._signal_handler)
                self._orig_sigint = signal.signal(signal.SIGINT, self._signal_handler)
                self._registered_cleanup = True

            return True

        except (BlockingIOError, OSError):
            # Lock already held by another process
            if self._lock_fd:
                self._lock_fd.close()
                self._lock_fd = None
            return False

    def release_lock(self) -> None:
        """Release the lock and clean up lock file."""
        if self._lock_fd:
            try:
                fcntl.flock(self._lock_fd, fcntl.LOCK_UN)
                self._lock_fd.close()
            except (OSError, IOError):
                pass
            self._lock_fd = None

        # Remove lock file
        try:
            if self.lock_file.exists():
                self.lock_file.unlink()
        except (OSError, IOError):
            pass

    def record_invocation(self) -> None:
        """
        Record successful invocation for cooldown and history tracking.

        Call this after script logic completes successfully.
        """
        # Update history (for automation detection)
        history = self._load_history()
        history.append(time.time())

        # Keep only last hour of history
        cutoff = time.time() - 3600
        history = [t for t in history if t > cutoff]
        self._save_history(history)

    def _cleanup_stale_lock(self) -> None:
        """Remove lock files with dead PIDs or older than 1 hour."""
        if not self.lock_file.exists():
            return

        try:
            with open(self.lock_file, 'r') as f:
                content = f.read().strip()
                if not content:
                    # Empty lock file - remove it
                    self.lock_file.unlink()
                    return
                lock_data = json.loads(content)

            pid = lock_data.get('pid')
            timestamp = lock_data.get('timestamp', 0)

            # Check if PID is still alive
            if pid:
                try:
                    os.kill(pid, 0)  # Signal 0 = check if process exists
                    # Process alive - check age
                    if time.time() - timestamp > 3600:  # 1 hour
                        self.lock_file.unlink()
                except OSError:
                    # Process dead - remove stale lock
                    self.lock_file.unlink()
            else:
                # No PID - check age only
                if time.time() - timestamp > 3600:
                    self.lock_file.unlink()

        except (json.JSONDecodeError, IOError, OSError):
            # Corrupted lock file - remove it
            try:
                self.lock_file.unlink()
            except (OSError, IOError):
                pass

    def _signal_handler(self, signum, frame):
        """Handle termination signals gracefully."""
        self.release_lock()
        # Re-raise to allow normal signal handling
        if signum == signal.SIGTERM and hasattr(self, '_orig_sigterm'):
            if callable(self._orig_sigterm):
                self._orig_sigterm(signum, frame)
        elif signum == signal.SIGINT and hasattr(self, '_orig_sigint'):
            if callable(self._orig_sigint):
                self._orig_sigint(signum, frame)
        raise SystemExit(128 + signum)

    def _is_in_cooldown(self) -> bool:
        """Check if script is within cooldown period based on history."""
        history = self._load_history()
        if not history:
            return False
        # Check last invocation time
        last_invocation = max(history)
        return (time.time() - last_invocation) < self.config['cooldown_seconds']

    def _get_cooldown_remaining(self) -> int:
        """Get seconds remaining in cooldown period."""
        history = self._load_history()
        if not history:
            return 0
        last_invocation = max(history)
        remaining = self.config['cooldown_seconds'] - (time.time() - last_invocation)
        return max(0, int(remaining))

    def _is_automation_loop(self) -> bool:
        """Check if invocation pattern suggests automation loop."""
        history = self._load_history()
        cutoff = time.time() - self.config['automation_window']
        recent = [t for t in history if t > cutoff]
        return len(recent) >= self.config['automation_threshold']

    def _load_history(self) -> list:
        """Load invocation history from file."""
        if not self.history_file.exists():
            return []
        try:
            content = self.history_file.read_text().strip()
            if not content:
                return []
            return json.loads(content)
        except (json.JSONDecodeError, IOError):
            return []

    def _save_history(self, history: list) -> None:
        """Save invocation history to file."""
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        self.history_file.write_text(json.dumps(history))


def check_guard(script_name: str, force: bool = False,
                agent_path: Optional[Path] = None) -> Tuple[bool, str]:
    """
    Simple guard check without lock acquisition.

    For scripts that only need cooldown checking, not concurrent execution blocking.

    Args:
        script_name: Name of the script
        force: If True, bypass cooldown
        agent_path: Path to agent root

    Returns:
        Tuple of (allowed, message)

    Usage:
        allowed, msg = check_guard('wind_down', force=args.force)
        if not allowed:
            print(f"Blocked: {msg}")
            return 1
    """
    guard = SessionGuard(script_name, agent_path)
    return guard.should_proceed(force)
