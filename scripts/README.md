# Scripts Directory

This directory contains Python scripts for executing Linear agent tasks.

## Quick Start

**New to this?** Start with the unified setup:

```bash
python scripts/setup.py
```

This will guide you through everything. See [GETTING-STARTED.md](../GETTING-STARTED.md) for details.

## Main Scripts

- **setup.py** - Unified setup and health checks (start here!)
- **agent_workflow.py** - Main workflow script for working with tasks
- **setup_team.py** - Add or update team configurations
- **validate_teams.py** - Validate team configurations and API connections
- **execute_tasks.py** - Legacy task execution (team-specific)
- **cloud_executor.py** - Cloud execution management

## API Clients

- **linear_client.py** - Linear API client
- **google_client.py** - Google Docs and Sheets API clients
- **activecampaign_client.py** - ActiveCampaign API client
- **team_manager.py** - Team and credential management
- **task_analyzer.py** - Task analysis and categorization

## Setup

### Modern Setup (Recommended)

Use the unified setup script:

```bash
python scripts/setup.py
```

This handles:
- Dependency installation
- Team configuration
- API credential setup
- Health checks

### Manual Setup (Advanced)

If you prefer manual setup:

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure teams:
   ```bash
   python scripts/setup_team.py
   ```

3. Validate:
   ```bash
   python scripts/validate_teams.py
   ```

## Configuration

Team configurations are stored in `config/teams.json` (not `.env` files).

Each team can have:
- **Linear API** - Required for task management
- **Google APIs** - Optional, for Google Docs/Sheets automation
- **ActiveCampaign API** - Optional, for ActiveCampaign automation

See `config/teams.json.template` for the structure.

### Getting API Keys

**Linear API Key:**
1. Go to [Linear Settings → API](https://linear.app/settings/api)
2. Click "Create API Key"
3. Copy the key (you'll only see it once!)

**Google API Credentials:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project or select existing
3. Enable APIs: Docs API, Sheets API, Drive API
4. Create credentials (Service Account or OAuth 2.0)
5. Download credentials JSON file

**ActiveCampaign API:**
1. Go to ActiveCampaign Settings → Developer
2. Get API URL and API Key
3. Enter during team setup

## Usage

### Recommended: Use agent_workflow.py

```bash
# List teams
python scripts/agent_workflow.py --list-teams

# Analyze tasks
python scripts/agent_workflow.py --team trade-ideas --analyze

# Work on tasks
python scripts/agent_workflow.py --team trade-ideas --work

# Cloud execution
python scripts/agent_workflow.py --team trade-ideas --work --cloud
```

See [QUICK-REFERENCE.md](../QUICK-REFERENCE.md) for all commands.

### Legacy: execute_tasks.py

For backward compatibility, `execute_tasks.py` still works but uses environment variables:

```bash
python scripts/execute_tasks.py --task TRA-56
```

**Note:** For multi-team support, use `agent_workflow.py` instead.

## API Clients

### LinearClient

```python
from linear_client import LinearClient

client = LinearClient()
issue = client.get_issue_by_identifier('TRA-56')
client.add_comment('TRA-56', 'Task completed')
client.update_issue_status('TRA-56', 'In Review')
```

### GoogleDocsClient

```python
from google_client import GoogleDocsClient

client = GoogleDocsClient()
doc_id = client.create_document('My Document')
client.insert_text(doc_id, 'Hello, World!')
```

### GoogleSheetsClient

```python
from google_client import GoogleSheetsClient

client = GoogleSheetsClient()
sheet_id = client.create_spreadsheet('My Sheet')
client.write_values(sheet_id, 'Sheet1!A1:B2', [['Header1', 'Header2'], ['Data1', 'Data2']])
```

### ActiveCampaignClient

```python
from activecampaign_client import ActiveCampaignClient

client = ActiveCampaignClient()
tags = client.list_tags()
client.create_tag('My Tag')
```

## Error Handling

- API rate limits are handled automatically
- Errors are caught and reported
- Failed tasks don't stop execution of other tasks
- All results are logged

## Rate Limits

- **Linear:** 1500 requests/hour
- **Google APIs:** Varies by operation
- **ActiveCampaign:** ~10,000 requests/day (varies by plan)

The clients include rate limiting and retry logic where appropriate.

## Testing

Test individual clients:

```bash
python scripts/linear_client.py TRA-56
```

## Notes

- Scripts are designed to be idempotent (safe to run multiple times)
- All API operations are logged
- Failed operations are reported but don't stop execution
- Use dry-run mode to test without making changes
