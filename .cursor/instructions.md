# Cursor Instructions

## Project Purpose
This repository provides a multi-team, multi-project system for managing and automating Linear tasks using AI agents.

## Key Capabilities
1. **Multi-Team Management**: Support for multiple Linear teams/projects with separate credentials
2. **Task Analysis**: Automatically identify agent-suitable tasks across teams
3. **Smart Execution**: Work on tasks by team, project, or evaluate all teams
4. **Review Workflow**: Completed tasks go to "In Review" for manual approval

## Usage Patterns

### Working with Teams
- Use `agent_workflow.py` as the main entry point
- Commands:
  - `--list-teams` - List all configured teams
  - `--analyze-all` - Analyze all teams and provide summaries
  - `--team TEAM_ID --analyze` - Analyze tasks for a specific team
  - `--team TEAM_ID --work` - Work on agent-suitable tasks for a team
  - `--team TEAM_ID --project PROJECT_ID --work` - Work on tasks in a project

### Adding New Teams
- Use `setup_team.py` for interactive team setup
- Teams are stored in `config/teams.json` (gitignored)
- Each team can have Linear, Google, and ActiveCampaign credentials

## Important Notes
- **Task Status Workflow**: When an agent completes a task, it MUST be marked as "In Review" status, NOT "Done". Only the user can determine if a task has been completed to their satisfaction and manually move it to "Done" status after review.
- **Credentials**: Team credentials are stored in `config/teams.json` (not committed to git)
- **Rate Limits**: Linear API has 1500 requests/hour limit
- **Single User**: This system is designed for single-user use, not multi-tenant
- **Focus**: Focus on tasks with clear requirements and acceptance criteria for best automation results





