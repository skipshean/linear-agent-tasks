# Archived Documentation

This directory contains documentation from previous versions of the system that are no longer current but kept for reference.

## Contents

Files moved here are from the old single-team, `.env`-based system or historical execution status files.

**These are kept for historical reference only - do not use for current setup.**

## Current Documentation

See the root directory for current documentation:
- **[GETTING-STARTED.md](../GETTING-STARTED.md)** - ⭐ Start here for new users
- **[README.md](../README.md)** - Main documentation
- **[QUICK-REFERENCE.md](../QUICK-REFERENCE.md)** - Command reference
- **[TROUBLESHOOTING.md](../TROUBLESHOOTING.md)** - Problem solving
- **[CONFIGURATION-EXAMPLES.md](../CONFIGURATION-EXAMPLES.md)** - Config patterns

## Archived Files

### Old Setup Documentation
- `QUICK-START.md` - Old quick start (used .env files)
- `API-SETUP-COMPLETE.md` - Historical API setup notes
- `SETUP-SUMMARY.md` - Old setup summary
- `API-FIXES-COMPLETE.md` - Historical fixes

### OAuth Setup (Historical)
- `*OAUTH*.md` - OAuth setup instructions (if not needed)
- `CREATE-*.md` - OAuth client creation guides
- `EXTRACT-*.md` - OAuth code extraction

### Execution Status (Historical)
- `EXECUTION-*.md` - Old execution status and summary files
  - These were from specific execution runs
  - Kept for historical reference only

## Migration Notes

If you're migrating from the old system:
1. See [MIGRATION-GUIDE.md](../MIGRATION-GUIDE.md) in root directory
2. Use `python scripts/setup.py` for new setup
3. Teams are now configured in `config/teams.json` (not `.env`)

## When to Reference These

Only reference these files if you need to:
- Understand historical decisions
- See what changed from old system
- Review past execution runs

For current usage, always refer to the documentation in the root directory.
