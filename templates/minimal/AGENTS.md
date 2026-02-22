# {{PROJECT_NAME}} - Universal Agent Configuration

## Agent Compatibility
This configuration follows the AGENTS.md open-source standard for universal agent configuration.
Works with Claude Code, Codex CLI, Gemini CLI, and other CLI coding agents.
**Note**: CLAUDE.md is a symlink to this file for backward compatibility.

## Project Context
This project uses CLI Agent Template for conversational development workflows.

## Session Management Commands

### Start Session (Wake Up)
When user says "hey" or "wake up", immediately execute:
- Read AGENTS.md (this file)
- Run: `python3 scripts/aget_session_protocol.py wake`
- Report project status
- End with "Ready for tasks."

### Save Work (Wind Down)
When user says "save work" or "wind down", execute:
- Run: `python3 scripts/aget_session_protocol.py wind-down`
- Commit changes and save session state
- Report "Session preserved."

### End Session (Sign Off)
When user says "all done", "sync up", or "sign off", execute:
- Run: `python3 scripts/aget_session_protocol.py sign-off`
- Quick commit and push
- Report "Signed off."

## Project Information
- **Name**: {{PROJECT_NAME}}
- **Type**: {{PROJECT_TYPE}}
- **Path**: {{PROJECT_PATH}}

## Important Notes
- Always run commands exactly as specified
- Maintain conversation context across commands
- Report command outputs clearly