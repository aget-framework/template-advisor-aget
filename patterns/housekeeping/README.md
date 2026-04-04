# Housekeeping Patterns

Patterns for maintaining clean, organized, and healthy codebases.

## Available Patterns

### housekeeping
**Trigger**: "housekeeping"
**Purpose**: Light cleanup of temporary files
**Safety**: Always runs dry-run first
**Actions**:
- Remove `__pycache__` directories
- Clean `.pyc` and `.pyo` files
- Remove `.DS_Store` files
- Clear temporary test artifacts
- Clean build directories

### spring_clean
**Trigger**: "spring clean"
**Purpose**: Deep cleanup with archiving
**Safety**: Requires explicit confirmation
**Actions**:
- Everything from housekeeping
- Archive old log files (>30 days)
- Remove duplicate files
- Clean empty directories
- Organize downloads and temp folders
- Compress old session notes

### sanity_check
**Trigger**: "sanity check"
**Purpose**: Emergency diagnostics
**Safety**: Read-only operations
**Actions**:
- Verify Python version and environment
- Check git repository health
- Validate critical files exist
- Test import statements
- Check disk space
- Verify permissions

### documentation_check
**Trigger**: "documentation check"
**Purpose**: Assess documentation quality
**Safety**: Read-only analysis
**Actions**:
- Check for README.md
- Verify license file exists
- Analyze documentation completeness
- Grade A-F based on coverage
- Suggest improvements

## Usage Examples

```bash
# Regular maintenance
You: housekeeping
Agent: [Shows what would be cleaned, asks confirmation]

# Quarterly cleanup
You: spring clean
Agent: [Deep analysis, archives old files, requires confirmation]

# Something's broken
You: sanity check
Agent: [Runs diagnostics, reports system status]

# Documentation review
You: documentation check
Agent: [Grades docs, suggests improvements]
```

## Safety Mechanisms

### Dry-Run by Default
```python
def clean(dry_run=True):
    if dry_run:
        print("Would remove: ...")
    else:
        # Actually remove files
```

### Progressive Permissions
1. **Read** - Sanity check, documentation check
2. **Modify** - Housekeeping (with confirmation)
3. **Reorganize** - Spring clean (explicit approval)

### Exclusion Lists
Protected files and directories:
- `.git/`
- `.env`
- `node_modules/` (handled separately)
- `venv/` and virtual environments
- User data directories

## Configuration

### Custom Cleanup Rules
Add to `scripts/health_check.py`:
```python
CUSTOM_PATTERNS = [
    "*.tmp",
    "*.bak",
    "*.old",
    "debug.log"
]
```

### Archive Settings
```python
ARCHIVE_DAYS = 30  # Files older than this
ARCHIVE_DIR = "SESSION_NOTES/archive/"
```

## Metrics

Track cleanup effectiveness:
- Files removed per session
- Space recovered
- Time saved vs manual cleanup
- Error prevention rate

## Best Practices

1. **Run weekly**: Regular housekeeping prevents buildup
2. **Spring clean quarterly**: Deep cleanup every 3 months
3. **Sanity check on errors**: First response to problems
4. **Document regularly**: Check documentation with each release

## Integration with CI/CD

```yaml
# .github/workflows/housekeeping.yml
- name: Housekeeping Check
  run: python scripts/health_check.py housekeeping --check-only
```