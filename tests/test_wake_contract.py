#!/usr/bin/env python3
"""v3.0 Wake Protocol Contract Tests - Advisor Template

Tests that wake protocol correctly reports agent identity, version, capabilities,
and advisor-specific information (advisory mode, persona).

v3.0.0: 5D Composition Architecture - instance_type replaces roles

Part of AGET framework advisor template validation.
"""

import pytest
import json
from pathlib import Path


def test_wake_protocol_reports_agent_name():
    """Wake protocol must report agent name from version.json (if present)."""
    version_file = Path(__file__).parent.parent / ".aget/version.json"
    assert version_file.exists(), "version.json not found"

    with open(version_file) as f:
        data = json.load(f)
        # agent_name optional in templates, required in instantiated agents
        if "agent_name" in data:
            agent_name = data["agent_name"]
            assert agent_name, "agent_name field is empty"
            assert isinstance(agent_name, str), "agent_name must be a string"


def test_wake_protocol_reports_version():
    """Wake protocol must report current AGET version."""
    version_file = Path(__file__).parent.parent / ".aget/version.json"
    assert version_file.exists(), "version.json not found"

    with open(version_file) as f:
        data = json.load(f)
        assert "aget_version" in data, "version.json missing aget_version field"
        # Version format: X.Y.Z
        version = data["aget_version"]
        base_version = version.split("-")[0]  # Handle pre-release
        parts = base_version.split(".")
        assert len(parts) == 3, f"Version format invalid: {version} (expected X.Y.Z)"


def test_wake_protocol_reports_capabilities():
    """Wake protocol must report agent capabilities (if present)."""
    version_file = Path(__file__).parent.parent / ".aget/version.json"
    assert version_file.exists(), "version.json not found"

    with open(version_file) as f:
        data = json.load(f)
        # Capabilities are optional in template, but if present, must be dict
        if "capabilities" in data:
            capabilities = data["capabilities"]
            assert isinstance(capabilities, (dict, list)), "capabilities must be dict or list"


def test_wake_protocol_reports_domain():
    """Wake protocol must report agent domain for context (if present)."""
    version_file = Path(__file__).parent.parent / ".aget/version.json"
    assert version_file.exists(), "version.json not found"

    with open(version_file) as f:
        data = json.load(f)
        # Domain is optional in template, but if present, must be string
        if "domain" in data:
            domain = data["domain"]
            assert isinstance(domain, str), "domain must be a string"
            assert domain, "domain field is empty"


# ============================================================================
# Advisor-Specific Wake Protocol Tests (v3.0)
# ============================================================================


def test_wake_displays_advisory_mode():
    """Wake protocol must indicate advisory mode for advisor agents.

    v3.0: Uses instance_type and template fields instead of roles.
    - instance_type: "aget" (advisory) vs "AGET" (action-taking) vs "template"
    - template: archetype name (advisor, consultant, etc.)
    """
    version_file = Path(__file__).parent.parent / ".aget/version.json"
    assert version_file.exists(), "version.json not found"

    with open(version_file) as f:
        data = json.load(f)

        # v3.0: Check template or instance_type for advisory mode
        template = data.get("template", "")
        instance_type = data.get("instance_type", "")

        # Advisor templates are advisory by nature
        advisory_archetypes = ["advisor", "consultant", "spec-engineer"]
        is_advisory_archetype = template in advisory_archetypes

        # For templates, instance_type may be "template"
        # For instances, "aget" = advisory, "AGET" = action-taking
        is_advisory_instance = instance_type in ["aget", "template"]

        if is_advisory_archetype:
            # Advisory archetypes should not be action-taking
            assert instance_type != "AGET", \
                f"Advisory archetype '{template}' should not have instance_type 'AGET'"

            # v3.0: advisory_capabilities section is optional but if present, validate
            if "advisory_capabilities" in data:
                caps = data["advisory_capabilities"]
                if "can_execute" in caps:
                    assert caps["can_execute"] is False, \
                        "Advisory agents should have can_execute: false"


def test_wake_displays_persona():
    """Wake protocol must display persona type for advisor agents.

    v3.0: Persona is defined in .aget/persona/ directory structure.
    version.json may have persona field for quick reference.
    """
    version_file = Path(__file__).parent.parent / ".aget/version.json"
    assert version_file.exists(), "version.json not found"

    with open(version_file) as f:
        data = json.load(f)

        # v3.0: Check template field instead of roles
        template = data.get("template", "")
        advisory_archetypes = ["advisor", "consultant", "spec-engineer"]

        if template in advisory_archetypes:
            # Persona can be in version.json or .aget/persona/
            persona_in_version = data.get("persona")
            persona_dir = Path(__file__).parent.parent / ".aget/persona"

            # Either persona in version.json or persona directory should exist
            has_persona = (persona_in_version is not None) or persona_dir.exists()

            # For templates, persona may be null (set at instantiation)
            instance_type = data.get("instance_type", "")
            if instance_type != "template":
                # Instantiated agents should have persona defined
                assert has_persona, \
                    "Instantiated advisor agents must have persona defined"

            # If persona is set in version.json, validate format
            if persona_in_version is not None:
                assert isinstance(persona_in_version, str), \
                    f"persona must be string if set, got {type(persona_in_version)}"
                assert persona_in_version.strip(), \
                    "persona must not be empty string"
