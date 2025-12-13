# Cloud Execution Guide

## Overview

The system supports executing tasks in the cloud instead of locally. This is useful for:
- Long-running tasks that would tie up your local machine
- Tasks that need to run in the background
- Tasks that require specific cloud resources

## How It Works

1. **Task Submission**: Tasks are submitted to a cloud queue
2. **Package Creation**: A self-contained package is created with all necessary code and credentials
3. **Cloud Execution**: The package can be uploaded to any cloud environment and executed
4. **Status Tracking**: Execution status is tracked in Linear comments

## Usage

### Submit Tasks for Cloud Execution

```bash
# Submit tasks for cloud execution
python scripts/agent_workflow.py --team trade-ideas --work --cloud

# Limit number of tasks
python scripts/agent_workflow.py --team trade-ideas --work --cloud --limit 5
```

### Check Status

```bash
# Check status of all cloud tasks
python scripts/agent_workflow.py --check-status

# Check status of specific task
python scripts/agent_workflow.py --check-status TRA-56
```

## Cloud Package Structure

When you submit tasks for cloud execution, a package is created in `.cloud-packages/`:

```
.cloud-packages/
  trade-ideas_1234567890/
    ├── execute_cloud.py      # Main execution script
    ├── team_manager.py       # Team management
    ├── linear_client.py      # Linear API client
    ├── google_client.py      # Google API client
    ├── activecampaign_client.py  # ActiveCampaign API client
    ├── execute_tasks.py      # Task execution logic
    ├── config/
    │   └── teams.json        # Team configuration (credentials)
    ├── requirements.txt      # Python dependencies
    └── README.md            # Instructions
```

## Deploying to Cloud

### Option 1: Google Cloud Run

1. Upload the package directory to Google Cloud Storage
2. Create a Cloud Run service that:
   - Downloads the package
   - Installs dependencies
   - Runs `execute_cloud.py`

### Option 2: Google Cloud Functions

1. Package the code
2. Deploy as a Cloud Function
3. Trigger via Cloud Tasks or Pub/Sub

### Option 3: Any Cloud Environment

The package is self-contained and can run on:
- AWS Lambda
- Azure Functions
- Any Linux server with Python 3.8+

## Queue Files

Tasks are also stored as queue files in `.cloud-queue/`:

- `.cloud-queue/pending/` - Tasks waiting to be executed
- `.cloud-queue/running/` - Tasks currently being executed
- `.cloud-queue/completed/` - Successfully completed tasks
- `.cloud-queue/failed/` - Failed tasks

Your cloud agent can poll the `pending/` directory and move files to `running/` and then `completed/` or `failed/`.

## Google Cloud Project Configuration

### Shared Project (Recommended for Most Cases)

Use one Google Cloud project for all teams:

```json
{
  "google": {
    "credentials_path": "credentials/shared-google-credentials.json",
    "cloud_project_id": "my-shared-project",
    "use_shared_project": true
  }
}
```

### Per-Team Projects

Use separate Google Cloud projects for each team:

```json
{
  "google": {
    "credentials_path": "credentials/team-specific-credentials.json",
    "cloud_project_id": "team-specific-project",
    "use_shared_project": false
  }
}
```

### Benefits of Per-Team Projects

- **Isolation**: Each client's data is completely isolated
- **Billing**: Separate billing per client
- **Security**: Client-specific access controls
- **Compliance**: Easier to meet client-specific compliance requirements

### Benefits of Shared Project

- **Simplicity**: One project to manage
- **Cost**: Potentially lower costs (shared resources)
- **Easier Setup**: One set of credentials

## Setting Up Cloud Execution

### 1. Configure Team with Cloud Project

When setting up a team, you'll be asked about Google Cloud project configuration:

```bash
python scripts/setup_team.py
```

Choose:
- **Shared project**: Use one project for all teams
- **Team-specific project**: Separate project for this team

### 2. Submit Tasks

```bash
python scripts/agent_workflow.py --team your-team --work --cloud
```

### 3. Deploy Package

Upload the generated package to your cloud environment and execute.

## Monitoring

- Check Linear comments for execution updates
- Monitor `.cloud-queue/` directory for queue status
- Check `cloud_execution_results.json` in the package directory after execution

## Troubleshooting

### "No pending tasks" but tasks were submitted

- Check `.cloud-queue/pending/` directory
- Verify task files were created
- Check file permissions

### Cloud execution fails

- Verify credentials in `config/teams.json` are correct
- Check that all dependencies are installed
- Review error logs in Linear comments

### Package not created

- Check write permissions in workspace
- Verify team configuration is valid
- Check disk space
