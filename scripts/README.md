# Execution Scripts

This directory contains Python scripts for executing Linear agent tasks.

## Files

- **execute_tasks.py** - Master execution script for running tasks
- **linear_client.py** - Linear API client
- **google_client.py** - Google Docs and Sheets API clients
- **activecampaign_client.py** - ActiveCampaign API client
- **requirements.txt** - Python dependencies

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the workspace root:

```bash
# Linear API
LINEAR_API_KEY=your_linear_api_key

# Google APIs
GOOGLE_CREDENTIALS_PATH=/path/to/credentials.json

# ActiveCampaign API
ACTIVE_CAMPAIGN_API_URL=https://your-account.api-us1.com
ACTIVE_CAMPAIGN_API_KEY=your_api_key
```

### 3. Google API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project or select existing
3. Enable APIs:
   - Google Docs API
   - Google Sheets API
   - Google Drive API
4. Create credentials:
   - Service Account (recommended) or OAuth 2.0
5. Download credentials JSON file
6. Set `GOOGLE_CREDENTIALS_PATH` to path of JSON file
7. Share target Google Drive folders with service account email (if using service account)

### 4. Linear API Setup

1. Go to Linear Settings → API
2. Create Personal API Key
3. Set `LINEAR_API_KEY` environment variable

### 5. ActiveCampaign API Setup

1. Go to ActiveCampaign Settings → Developer
2. Get API URL and API Key
3. Set `ACTIVE_CAMPAIGN_API_URL` and `ACTIVE_CAMPAIGN_API_KEY` environment variables

## Usage

### Execute Single Task

```bash
python scripts/execute_tasks.py --task TRA-56
```

### Execute Phase

```bash
python scripts/execute_tasks.py --phase quick-wins
```

Available phases:
- `quick-wins` - TRA-56, TRA-65, TRA-109, TRA-54
- `foundation` - TRA-41, TRA-59, TRA-60
- `dashboards` - TRA-42 through TRA-48
- `forecast` - TRA-49, TRA-106-108
- `configuration` - TRA-63-64, TRA-40, TRA-51-53

### Execute All Tasks

```bash
python scripts/execute_tasks.py --all
```

### List Available Tasks

```bash
python scripts/execute_tasks.py --list
```

### Dry Run Mode

If API credentials are not configured, the script will run in dry-run mode:
- No actual API calls will be made
- Tasks will report what they would do
- Useful for testing script logic

## API Clients

### LinearClient

```python
from linear_client import LinearClient

client = LinearClient()
issue = client.get_issue_by_identifier('TRA-56')
client.add_comment('TRA-56', 'Task completed')
client.update_issue_status('TRA-56', 'Done')
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
