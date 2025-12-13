# Migration Guide: Multi-Team Support

## What Changed

The system has been refactored from a single-project (Trade Ideas) focus to a multi-team, multi-project system.

## New Architecture

### Before
- Single `.env` file with credentials
- Hard-coded team references (TRA-*)
- Single team focus

### After
- `config/teams.json` for team configurations
- Support for multiple teams with separate credentials
- Team-agnostic task execution
- Project-level filtering

## New Files

1. **`config/teams.json.template`** - Template for team configuration
2. **`scripts/team_manager.py`** - Manages teams and credentials
3. **`scripts/task_analyzer.py`** - Analyzes tasks across teams/projects
4. **`scripts/agent_workflow.py`** - New main workflow script
5. **`scripts/setup_team.py`** - Interactive team setup utility

## Migration Steps

### 1. Set Up Your First Team

If you have existing credentials in `.env`, you can migrate them:

```bash
python scripts/setup_team.py
```

When prompted:
- **Team ID**: `trade-ideas` (or your preferred identifier)
- **Team Name**: `Trade Ideas`
- **Linear API Key**: Copy from your existing `.env` or Linear settings
- **Google Credentials**: Point to your existing credentials file
- **ActiveCampaign**: Copy from your existing `.env`

### 2. Verify Setup

```bash
python scripts/agent_workflow.py --list-teams
```

You should see your team listed.

### 3. Test Analysis

```bash
python scripts/agent_workflow.py --team trade-ideas --analyze
```

This should show tasks for your team.

## New Commands

### Old Way (Still Works)
```bash
python scripts/execute_tasks.py --task TRA-56
```

### New Way (Recommended)
```bash
# Analyze what can be done
python scripts/agent_workflow.py --team trade-ideas --analyze

# Work on tasks
python scripts/agent_workflow.py --team trade-ideas --work
```

## Adding More Teams

Simply run `setup_team.py` again:

```bash
python scripts/setup_team.py
```

Enter a new team ID and credentials. The system will manage multiple teams automatically.

## Configuration Location

- **Team Configs**: `config/teams.json` (gitignored - contains credentials)
- **Template**: `config/teams.json.template` (committed to git)
- **Old `.env`**: Can be kept for backward compatibility, but teams.json is preferred

## Backward Compatibility

The old `execute_tasks.py` script still works, but it will use environment variables. For multi-team support, use `agent_workflow.py`.

## Benefits

1. **Multiple Clients**: Manage tasks for different clients/projects
2. **Isolated Credentials**: Each team has its own credentials
3. **Better Organization**: Clear separation between teams
4. **Scalable**: Easy to add new teams without code changes
5. **Flexible**: Work on specific teams, projects, or all teams

## Next Steps

1. Set up your first team using `setup_team.py`
2. Test with `--analyze` to see what tasks are available
3. Use `--work` to have the agent work on suitable tasks
4. Add more teams as needed

See `QUICK-REFERENCE.md` for common commands and examples.
