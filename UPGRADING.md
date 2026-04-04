# Upgrading Guide for CLI Agent Template

This guide explains how to update repositories that use the CLI Agent Template after the template itself has been enhanced.

## Migrating to AGET Architecture

The CLI Agent Template has transitioned to the AGET (Agent Template) naming convention for clearer architecture.

### What Changed
- All protocol scripts now use `aget_` prefix
- `session_protocol.py` → `aget_session_protocol.py`
- `housekeeping_protocol.py` → `health_check.py`

### Migration Steps

1. **Update script references in your AGENTS.md or CLAUDE.md**:
   ```bash
   # Old
   python3 scripts/session_protocol.py wake

   # New
   python3 scripts/aget_session_protocol.py wake
   ```

2. **Update Makefile targets** (if customized):
   ```makefile
   # Old
   WAKE_CMD := python3 scripts/session_protocol.py wake

   # New
   WAKE_CMD := python3 scripts/aget_session_protocol.py wake
   ```

3. **Create compatibility symlinks** (optional for transition period):
   ```bash
   cd scripts
   ln -s aget_session_protocol.py session_protocol.py
   ln -s health_check.py housekeeping_protocol.py
   ```

### Benefits of AGET Architecture
- Clearer separation between template and user files
- Prevents naming conflicts with user scripts
- Easier updates without breaking user customizations
- Consistent naming convention across all template files

## The Challenge

Once you've used this as a template, your repository has its own copy of the files. Updates to the template don't automatically flow to your project. However, CLI agents can intelligently merge updates rather than blindly overwriting your customizations.

## Five-Phased Update Approach

This approach allows CLI agents to cautiously update your repository while preserving your customizations.

### Phase 1: Assess Changes (Non-destructive)

First, understand what has changed between your version and the latest template:

```bash
# Compare versions and see what's different
diff scripts/aget_session_protocol.py ~/github/aget-cli-agent-template/scripts/aget_session_protocol.py
diff scripts/health_check.py ~/github/aget-cli-agent-template/scripts/health_check.py

# Check for new scripts in the template
ls ~/github/aget-cli-agent-template/scripts/ | grep -v "$(ls scripts/)"

# Check template version
cd ~/github/aget-cli-agent-template && git log --oneline -5
```

### Phase 2: Update Core Scripts Only

Update the protocol scripts (these are usually safe as they're self-contained):

```bash
# Backup current scripts first
cp scripts/session_protocol.py scripts/session_protocol.py.bak
cp scripts/housekeeping_protocol.py scripts/housekeeping_protocol.py.bak

# Update protocol scripts (with AGET naming)
cp ~/github/aget-cli-agent-template/scripts/aget_session_protocol.py scripts/
cp ~/github/aget-cli-agent-template/scripts/health_check.py scripts/

# Test they still work with your configuration
python3 scripts/session_protocol.py status
python3 scripts/housekeeping_protocol.py sanity-check
```

### Phase 3: Merge AGENTS.md Changes (Manual)

Your AGENTS.md (or CLAUDE.md) likely contains project-specific content. Don't overwrite it; instead, selectively merge updates:

```bash
# Extract just the protocol sections from template
grep -A 20 "Session Management Protocols" ~/github/aget-cli-agent-template/AGENTS.md > /tmp/new_protocols.txt
grep -A 20 "Housekeeping Protocols" ~/github/aget-cli-agent-template/AGENTS.md >> /tmp/new_protocols.txt

# Review the new protocols
cat /tmp/new_protocols.txt

# Manually merge into your AGENTS.md, updating only:
# - Trigger phrases (e.g., "hey" instead of "wake up")
# - Command syntax
# - Protocol descriptions
# Keep your project-specific sections intact
```

### Phase 4: Add New Features (Optional)

Check for new features and add only what you need:

```bash
# See what's new in the template
ls ~/github/aget-cli-agent-template/scripts/
ls ~/github/aget-cli-agent-template/patterns/

# Selectively copy new features you want
# Examples:
cp ~/github/aget-cli-agent-template/scripts/validate_patterns.py scripts/  # if you need pattern validation
cp ~/github/aget-cli-agent-template/installer/update.py installer/  # if you want the updater
```

### Phase 5: Validate & Document

Ensure everything works and document the update:

```bash
# Run comprehensive checks
python3 scripts/housekeeping_protocol.py sanity-check
python3 scripts/session_protocol.py wake

# Test your project-specific commands still work
# (Add your own tests here)

# Document what template version you're aligned with
echo "Template version: $(cd ~/github/aget-cli-agent-template && git rev-parse --short HEAD)" > .template_version
echo "Updated: $(date)" >> .template_version

# Commit the updates
git add -A
git commit -m "chore: Update CLI agent patterns from template"
```

## Common Update Scenarios

### Updating Trigger Phrases Only

If you just need to update trigger phrases (e.g., recent change from "wake up" to "hey"):

1. Edit your AGENTS.md or CLAUDE.md
2. Update the trigger phrase descriptions
3. The scripts themselves usually read from environment or use multiple phrases

### Adding a New Protocol

To add a new protocol from the template:

1. Copy the specific protocol script from `~/github/aget-cli-agent-template/scripts/`
2. Add its documentation section to your AGENTS.md
3. Test it works in your environment

### Fixing Bugs in Protocol Scripts

If there's a bug fix in the template's protocol scripts:

1. Check the diff to understand the fix
2. Either apply the fix manually or copy the entire script
3. Test thoroughly as the fix might have dependencies

## Future-Proofing Your Repository

To make future updates easier:

1. **Minimize modifications to core scripts** - Instead of modifying `session_protocol.py`, create wrapper scripts
2. **Use configuration files** - Put project-specific settings in separate config files
3. **Document your customizations** - Keep a CUSTOMIZATIONS.md noting what you've changed
4. **Track template version** - Maintain a `.template_version` file

## Alternative Approaches

### Git Remote Approach

Add the template as a remote and cherry-pick updates:

```bash
git remote add template https://github.com/aget-framework/aget-cli-agent-template.git
git fetch template
git log template/main --oneline  # See what's new
git cherry-pick <commit-hash>  # Selectively apply updates
```

### Submodule Approach

Use the template as a git submodule (more complex but cleaner updates):

```bash
git submodule add https://github.com/aget-framework/aget-cli-agent-template.git .cli-agent
ln -s .cli-agent/scripts/session_protocol.py scripts/
```

## When NOT to Update

Don't update if:
- Your current setup is working well
- The update doesn't offer features you need
- You've heavily customized the scripts
- You're in the middle of critical work

## Getting Help

If an update breaks something:
1. Restore from your backups (`.bak` files)
2. Check the template's CHANGELOG.md for breaking changes
3. Run `python3 scripts/housekeeping_protocol.py sanity-check` for diagnostics
4. Open an issue on the template repository

Remember: The goal is to get improvements while preserving your customizations. When in doubt, make backups and test thoroughly.