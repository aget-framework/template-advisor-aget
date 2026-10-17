"""Pytest configuration for advisor template tests.

Provides template/instance detection for conditional test execution.
Contract tests for instance-specific features should be skipped when running on templates.

v2.10.0: Added template context detection for CI compatibility
"""

# --------------------------------------------------------------------------
# Repository-location isolation (gmelli/aget-aget#3019; same list as core's tests/conftest.py)
#
# git obeys these variables in every command, whatever folder it runs in. A hook run from a linked
# worktree hands the suite an absolute GIT_DIR, so a test that runs `git init/config/add/commit` in a
# scratch folder acts on the repository GIT_DIR names instead; GIT_CONFIG redirects `git config` writes
# to the file it names. They are removed here, at import, before any test module is collected. A test
# that needs one sets it itself. Falsifier: tests/test_conftest_git_env_isolation.py
# --------------------------------------------------------------------------
import os as _os
import tempfile as _tempfile

REPO_LOCATION_VARS = ("GIT_DIR", "GIT_WORK_TREE", "GIT_COMMON_DIR", "GIT_INDEX_FILE",
                      "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES",
                      "GIT_NAMESPACE", "GIT_PREFIX", "GIT_CONFIG")
for _var in REPO_LOCATION_VARS:
    _os.environ.pop(_var, None)

# git also searches upward for a repository from a folder that is not one. When the temp folder sits inside a
# working tree (a harness that keeps TMPDIR in its checkout), a test running git in a non-repository scratch
# folder would commit into the enclosing repository. Stop that search at the temp root.
_tmp_root = _tempfile.gettempdir()
_ceilings = [_tmp_root, _os.path.realpath(_tmp_root)] + [p for p in _os.environ.get("GIT_CEILING_DIRECTORIES", "").split(_os.pathsep) if p]
_os.environ["GIT_CEILING_DIRECTORIES"] = _os.pathsep.join(dict.fromkeys(_ceilings))


import json
import os
import pytest
from pathlib import Path


def get_version_json_path():
    """Find version.json relative to test file location."""
    tests_dir = Path(__file__).parent
    project_root = tests_dir.parent
    return project_root / ".aget" / "version.json"


def is_template_context():
    """
    Detect if tests are running in template context vs instance context.

    Templates are detected by:
    1. agent_name starts with 'template-'
    2. OR instance_type == 'template'

    Returns True for templates (skip instance-only tests).
    Returns False for instances (run all tests).
    """
    version_file = get_version_json_path()

    if not version_file.exists():
        return True

    try:
        with open(version_file) as f:
            data = json.load(f)

        agent_name = data.get("agent_name", "")
        if agent_name.startswith("template-"):
            return True

        instance_type = data.get("instance_type", "")
        if instance_type == "template":
            return True

        return False
    except (json.JSONDecodeError, IOError):
        return True


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers",
        "instance_only: mark test as instance-only (skipped on templates)"
    )


@pytest.fixture(scope="session", autouse=True)
def ensure_project_root():
    """Ensure contract tests run from project root where .aget/ exists."""
    current = Path.cwd()

    if (current / ".aget" / "version.json").exists():
        return

    if current.name == "tests" and (current.parent / ".aget" / "version.json").exists():
        os.chdir(current.parent)
        return


@pytest.fixture(scope="session")
def template_context():
    """Fixture providing template context detection."""
    return is_template_context()
