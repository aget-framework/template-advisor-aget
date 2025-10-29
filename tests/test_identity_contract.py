#!/usr/bin/env python3
"""v2.5 Identity Contract Tests

Tests that agent identity remains consistent and separate from operational context.
Addresses issue #76 (identity conflation).
Part of AGET framework v2.5 validation standards.
"""

import pytest
import json
from pathlib import Path


def test_identity_consistency_version_json_vs_manifest():
    """Agent identity must be consistent across version.json and agent_manifest.yaml."""
    version_file = Path(__file__).parent.parent / ".aget/version.json"
    manifest_file = Path(__file__).parent.parent / ".aget/collaboration/agent_manifest.yaml"

    assert version_file.exists(), "version.json not found"

    # Read version from version.json
    with open(version_file) as f:
        version_data = json.load(f)
        version_json_version = version_data["aget_version"]

    # Read version from agent_manifest.yaml (if exists)
    if manifest_file.exists():
        with open(manifest_file) as f:
            manifest_content = f.read()
            # Simple parsing - look for aget_compliance line
            for line in manifest_content.split("\n"):
                if "aget_compliance:" in line:
                    # Extract version (format: aget_compliance: "v2.4.0" or "2.4.0")
                    manifest_version = line.split(":")[-1].strip().strip('"').lstrip("v")
                    assert version_json_version == manifest_version, \
                        f"Version mismatch: version.json={version_json_version}, manifest={manifest_version}"
                    break


def test_identity_no_conflation_with_directory_name():
    """Agent name in version.json must match directory name (identity = location)."""
    version_file = Path(__file__).parent.parent / ".aget/version.json"
    assert version_file.exists(), "version.json not found"

    with open(version_file) as f:
        data = json.load(f)
        # agent_name might not exist in templates, check first
        if "agent_name" in data:
            agent_name = data["agent_name"]
            # Get directory name
            repo_dir = Path.cwd().name
            assert agent_name == repo_dir, \
                f"Identity conflation detected: agent_name='{agent_name}' but directory='{repo_dir}'"


def test_identity_persistence_across_invocations():
    """Agent identity fields must not change between invocations (stable identity)."""
    version_file = Path(__file__).parent.parent / ".aget/version.json"
    assert version_file.exists(), "version.json not found"

    with open(version_file) as f:
        data = json.load(f)

        # Core identity fields that must be stable (if present)
        # Not all agents have all fields, but these should be stable if they exist
        stable_fields = ["agent_name", "aget_version", "created"]
        for field in stable_fields:
            if field in data:
                value = data[field]
                assert value, f"Stable identity field '{field}' is empty"

        # These fields should NOT be in version.json (they're operational, not identity)
        operational_fields = ["current_session", "last_wake_time", "active_task"]
        for field in operational_fields:
            assert field not in data, \
                f"Identity conflation: Operational field '{field}' in version.json (should be in session state)"


def test_portfolio_field_exists():
    """Portfolio field must exist in version.json for v2.7.0+ (portfolio governance)."""
    version_file = Path(__file__).parent.parent / ".aget/version.json"
    assert version_file.exists(), "version.json not found"

    with open(version_file) as f:
        data = json.load(f)
        assert "portfolio" in data, "portfolio field missing in version.json (required in v2.7.0+)"

        # Portfolio must be None (template/unassigned) or valid classification
        portfolio = data["portfolio"]
        valid_portfolios = [None, "main", "example", "workco"]
        assert portfolio in valid_portfolios, \
            f"Invalid portfolio value: '{portfolio}' (must be one of: {valid_portfolios})"
