# Quick Reference Guide

## Common Commands

### Team Management

```bash
# Set up a new team (interactive)
python scripts/setup_team.py

# List all configured teams
python scripts/agent_workflow.py --list-teams
```

### Task Analysis

```bash
# Analyze all teams and get summaries
python scripts/agent_workflow.py --analyze-all

# Analyze tasks for a specific team
python scripts/agent_workflow.py --team trade-ideas --analyze

# Analyze tasks in a specific project
python scripts/agent_workflow.py --team trade-ideas --project PROJECT_ID --analyze
```

### Working on Tasks

```bash
# Work on all agent-suitable tasks for a team (local execution)
python scripts/agent_workflow.py --team trade-ideas --work

# Work on tasks in a specific project
python scripts/agent_workflow.py --team trade-ideas --project PROJECT_ID --work

# Work on limited number of tasks (e.g., first 5)
python scripts/agent_workflow.py --team trade-ideas --work --limit 5

# Submit tasks for cloud execution (background)
python scripts/agent_workflow.py --team trade-ideas --work --cloud

# Check status of cloud-executed tasks
python scripts/agent_workflow.py --check-status
python scripts/agent_workflow.py --check-status TRA-56
```

## Workflow Examples

### Example 1: Evaluate All Teams

```bash
# Get overview of what can be done across all teams
python scripts/agent_workflow.py --analyze-all
```

This will:
- Analyze all configured teams
- Show summary of agent-suitable tasks per team
- Save detailed results to `analysis_results.json`

### Example 2: Work on Specific Team

```bash
# 1. First, see what's available
python scripts/agent_workflow.py --team trade-ideas --analyze

# 2. Then work on suitable tasks
python scripts/agent_workflow.py --team trade-ideas --work
```

### Example 3: Project-Specific Work

```bash
# Work on tasks in a specific project
python scripts/agent_workflow.py --team trade-ideas --project abc123 --work
```

## Configuration

Team configurations are stored in `config/teams.json`. To add a team:

1. Run `python scripts/setup_team.py`
2. Follow the interactive prompts
3. Credentials are stored securely (file is gitignored)

## Task Status

- **In Review**: Agent completed the task - waiting for your approval
- **Done**: You've reviewed and approved the task
- **In Progress**: Task is being worked on
- **Todo**: Task hasn't been started

**Important**: Agents mark tasks as "In Review", not "Done". You must manually approve.

## Troubleshooting

### Quick Diagnostics

```bash
# Run health check
python scripts/setup.py --check

# Validate teams
python scripts/validate_teams.py

# Check status
python scripts/setup.py --status
```

### Common Issues

**"Team not found" error**
- Run `python scripts/setup.py` to set up teams
- Or `python scripts/setup_team.py` to add a team
- Check `config/teams.json` exists and has the team configured

**"No Linear API key" error**
- Make sure you've configured the Linear API key for the team
- Run `python scripts/setup_team.py` to update credentials
- Verify key in Linear Settings → API

**"No agent-suitable tasks found"**
- Tasks need clear descriptions (50+ characters)
- Tasks should have automation keywords or acceptance criteria
- Some tasks may need manual review/assignment first
- Try analyzing a different team or project

**"Dependencies missing"**
- Run `pip install -r scripts/requirements.txt`
- Or let `python scripts/setup.py` install them automatically

**"API connection failed"**
- Run `python scripts/validate_teams.py --team YOUR_TEAM` to diagnose
- Check API keys are correct and not expired
- Verify credentials file paths are correct
