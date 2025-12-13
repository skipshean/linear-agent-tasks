# Changelog

## 2025-12-13 - Major UX Improvements

### Added
- ✅ **Unified Setup Script** (`scripts/setup.py`)
  - Single entry point for first-time setup
  - Automatic dependency checking and installation
  - Interactive team configuration
  - Health check mode (`--check`)
  - Status dashboard (`--status`)

- ✅ **Interactive Mode** (`agent_workflow.py --interactive`)
  - Menu-driven interface
  - Guided workflows
  - No need to remember command syntax

- ✅ **Enhanced Validation** (`scripts/validate_teams.py`)
  - Works with teams.json (not .env)
  - Validates each team's API connections
  - Actionable error messages

- ✅ **Comprehensive Documentation**
  - `GETTING-STARTED.md` - 5-minute onboarding guide
  - `TROUBLESHOOTING.md` - Complete troubleshooting guide
  - `CONFIGURATION-EXAMPLES.md` - Team configuration patterns
  - `config/teams.json.example` - Example configurations

### Improved
- ✅ **Error Messages** - All errors now include "Next steps"
- ✅ **Setup Script** - Added help links for getting API keys
- ✅ **Documentation** - Consolidated and clarified
- ✅ **README.md** - Better structure and navigation

### Changed
- ✅ **Archived Old Docs** - Moved to `docs/archive/`
  - Old execution status files
  - OAuth setup documentation
  - Old quick start guide

### Fixed
- ✅ Updated `scripts/README.md` to reference new system
- ✅ Fixed duplicate error messages
- ✅ Improved credential help in setup prompts

## 2025-12-13 - Multi-Team Support

### Added
- Multi-team configuration system
- Team-specific credential management
- Project-level task filtering
- Cloud execution support
- Google Cloud project configuration (shared or per-team)

### Changed
- Migrated from `.env` to `config/teams.json`
- Refactored to support multiple teams/projects
- Task status workflow: "In Review" instead of "Done"

## Previous Versions

See `docs/archive/` for historical documentation and execution summaries.
