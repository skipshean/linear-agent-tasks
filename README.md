# Linear Agent Tasks

Multi-team, multi-project Linear task automation system for AI agents.

## Purpose

This repository provides a system for managing and automating Linear tasks across multiple teams and projects. It helps identify tasks suitable for AI agent automation and executes them while maintaining quality control through review workflows.

## Features

- **Multi-Team Support**: Manage tasks across multiple Linear teams/projects
- **Credential Management**: Store and manage API credentials per team
- **Task Analysis**: Automatically identify agent-suitable tasks
- **Smart Execution**: Work on tasks by team, project, or across all teams
- **Review Workflow**: Completed tasks are marked "In Review" for manual approval

## Quick Start

**New to this?** Start here: [GETTING-STARTED.md](GETTING-STARTED.md)

### First Time Setup

Run the unified setup script:

```bash
python scripts/setup.py
```

This will:
1. ✅ Check and install dependencies
2. 👥 Guide you through setting up your first team
3. ✅ Validate your configuration

### Verify Setup

```bash
# Health check
python scripts/setup.py --check

# Status dashboard
python scripts/setup.py --status

# Validate specific team
python scripts/validate_teams.py --team trade-ideas
```

### Daily Usage

```bash
# List configured teams
python scripts/agent_workflow.py --list-teams

# Analyze all teams
python scripts/agent_workflow.py --analyze-all

# Work on tasks

```bash
# Analyze tasks for a team
python scripts/agent_workflow.py --team trade-ideas --analyze

# Work on agent-suitable tasks (local execution)
python scripts/agent_workflow.py --team trade-ideas --work

# Submit tasks for cloud execution (background)
python scripts/agent_workflow.py --team trade-ideas --work --cloud

# Work on tasks in a specific project
python scripts/agent_workflow.py --team trade-ideas --project PROJECT_ID --work

# Limit number of tasks
python scripts/agent_workflow.py --team trade-ideas --work --limit 5

# Check cloud execution status
python scripts/agent_workflow.py --check-status

# Interactive mode (guided prompts)
python scripts/agent_workflow.py --interactive
```

## Workflow

1. **Setup**: Run `python scripts/setup.py` for first-time setup
2. **Verify**: Run `python scripts/setup.py --check` to validate configuration
3. **Analyze**: Use `--analyze-all` or `--analyze` to see what tasks are available
4. **Work**: Use `--work` to have the agent work on suitable tasks
5. **Review**: Completed tasks are marked "In Review" - you manually approve and move to "Done"

## Adding More Teams

After initial setup, add additional teams:

```bash
python scripts/setup_team.py
```

## Structure

- **config/** - Team configurations (teams.json contains credentials)
- **scripts/** - Execution scripts and API clients
  - `agent_workflow.py` - Main workflow script (use this!)
  - `team_manager.py` - Team and credential management
  - `task_analyzer.py` - Task analysis and categorization
  - `execute_tasks.py` - Legacy task execution (team-specific)
  - `linear_client.py` - Linear API client
  - `google_client.py` - Google Docs/Sheets API clients
  - `activecampaign_client.py` - ActiveCampaign API client
- **task-execution-guides/** - Documentation for specific task types

## Configuration

Team configurations are stored in `config/teams.json` (gitignored for security). Each team can have:
- Linear API credentials
- Google API credentials (optional)
  - Can use shared Google Cloud project or team-specific project
  - Supports both service account and OAuth credentials
- ActiveCampaign API credentials (optional)

See `config/teams.json.template` for the structure.

## Cloud Execution

For long-running tasks, you can submit them for cloud execution:

```bash
# Submit tasks for cloud execution
python scripts/agent_workflow.py --team trade-ideas --work --cloud
```

This creates a self-contained package in `.cloud-packages/` that can be uploaded to any cloud environment. See `CLOUD-EXECUTION-GUIDE.md` for details.

## Important Notes

- **Task Status**: When an agent completes a task, it's marked "In Review" - not "Done". You must manually review and approve.
- **Credentials**: Team credentials are stored locally in `config/teams.json` (not committed to git)
- **Rate Limits**: Linear API has 1500 requests/hour limit
- **Single User**: This system is designed for single-user use, not multi-tenant

## Troubleshooting

Having issues? Try these:

```bash
# Health check
python scripts/setup.py --check

# Validate team configuration
python scripts/validate_teams.py

# Status dashboard
python scripts/setup.py --status
```

See [GETTING-STARTED.md](GETTING-STARTED.md) for common first-time issues.

## Documentation

### 🚀 Getting Started
- **[GETTING-STARTED.md](GETTING-STARTED.md)** - ⭐ Start here! 5-minute setup guide

### 📚 Essential Guides
- **[QUICK-REFERENCE.md](QUICK-REFERENCE.md)** - Command reference
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions
- **[CONFIGURATION-EXAMPLES.md](CONFIGURATION-EXAMPLES.md)** - Team configuration examples
- **[CLOUD-EXECUTION-GUIDE.md](CLOUD-EXECUTION-GUIDE.md)** - Cloud execution features
- **[MIGRATION-GUIDE.md](MIGRATION-GUIDE.md)** - Migrating from old system

### 📖 Reference
- **agent-task-analysis.md** - Original Trade Ideas task analysis
- **duplicate-tracking.md** - Duplicate issue tracking
- **task-execution-guides/** - Guides for specific task types

### 📦 Archived
- Old documentation moved to `docs/archive/` (historical reference only)


