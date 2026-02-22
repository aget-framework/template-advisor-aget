# {{PROJECT_NAME}} - Universal Agent Configuration

## Agent Compatibility
This configuration follows the AGENTS.md open-source standard for universal agent configuration.
Works with Claude Code, Codex CLI, Gemini CLI, and other CLI coding agents.
**Note**: CLAUDE.md is a symlink to this file for backward compatibility.

## Project Context
This project uses CLI Agent Template (Standard) for comprehensive development workflows.

## Session Management Commands

### Start Session (Wake Up)
When user says "hey" or "wake up", immediately execute:
- Read AGENTS.md (this file)
- Run: `python3 scripts/aget_session_protocol.py wake`
- Report project status with git, tests, and documentation info
- End with "Ready for tasks."

### Save Work (Wind Down)
When user says "save work" or "wind down", execute:
- Run: `python3 scripts/aget_session_protocol.py wind-down`
- Commit changes, save session state, run tests
- Report "Session preserved."

### End Session (Sign Off)
When user says "all done", "sync up", or "sign off", execute:
- Run: `python3 scripts/aget_session_protocol.py sign-off`
- Quick commit and push to remote
- Report "Signed off."

## Housekeeping Commands

### Documentation Check
When user says "check docs" or "documentation check", execute:
- Run: `python3 scripts/aget_housekeeping_protocol.py documentation-check`
- Analyze documentation quality (line counts, staleness, missing files)
- Report grade (A-F) and specific issues

### Light Cleanup (Housekeeping)
When user says "tidy up" or "housekeeping", execute:
- Run: `python3 scripts/aget_housekeeping_protocol.py housekeeping --dry-run`
- Clean temporary files, caches, Python artifacts
- Show what would be removed, then ask for confirmation

### Deep Clean
When user says "deep clean" or "spring clean", execute:
- Run: `python3 scripts/aget_housekeeping_protocol.py spring-clean --dry-run`
- Deep cleanup: archive old files, remove duplicates, organize
- Always dry-run first, require explicit confirmation for actual execution

### Health Check
When user says "health check" or "sanity check", execute:
- Run: `python3 scripts/aget_housekeeping_protocol.py sanity-check`
- Emergency diagnostics: Python version, git status, dependencies
- Report system status: OK/DEGRADED/CRITICAL

## Project Information
- **Name**: {{PROJECT_NAME}}
- **Type**: {{PROJECT_TYPE}}
- **Path**: {{PROJECT_PATH}}
- **Test Command**: {{TEST_COMMAND}}

## Development Workflow

### Before Committing
1. Run tests: `{{TEST_COMMAND}}`
2. Check documentation: Say "documentation check"
3. Clean workspace: Say "housekeeping"

### When Something's Wrong
1. Say "sanity check" for diagnostics
2. Review the reported issues
3. Follow suggested fixes

## Important Notes
- All housekeeping commands default to dry-run for safety
- Session state is preserved in SESSION_NOTES/ directory
- Git commits follow conventional format: type: description
- Always maintain clean git history