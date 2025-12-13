# Configuration Examples

Examples and patterns for configuring teams in `config/teams.json`.

## Basic Team (Linear Only)

Minimal configuration with just Linear API:

```json
{
  "teams": [
    {
      "id": "my-team",
      "name": "My Team",
      "linear": {
        "api_key": "lin_api_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
      },
      "enabled": true
    }
  ]
}
```

## Full Configuration

Team with all services configured:

```json
{
  "teams": [
    {
      "id": "full-team",
      "name": "Full Team",
      "linear": {
        "api_key": "lin_api_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
      },
      "google": {
        "credentials_path": "credentials/full-team-google.json",
        "drive_folder_id": "1a2b3c4d5e6f7g8h9i0j",
        "cloud_project_id": "team-specific-project",
        "use_shared_project": false
      },
      "activecampaign": {
        "api_url": "https://account.api-us1.com",
        "api_key": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
      },
      "enabled": true,
      "notes": "Full configuration with all services"
    }
  ]
}
```

## Shared Google Cloud Project

Multiple teams using the same Google Cloud project:

```json
{
  "teams": [
    {
      "id": "team-1",
      "name": "Team 1",
      "linear": {
        "api_key": "lin_api_team1_key"
      },
      "google": {
        "credentials_path": "credentials/shared-credentials.json",
        "drive_folder_id": "team1_folder_id",
        "cloud_project_id": "shared-project-id",
        "use_shared_project": true
      },
      "enabled": true
    },
    {
      "id": "team-2",
      "name": "Team 2",
      "linear": {
        "api_key": "lin_api_team2_key"
      },
      "google": {
        "credentials_path": "credentials/shared-credentials.json",
        "drive_folder_id": "team2_folder_id",
        "cloud_project_id": "shared-project-id",
        "use_shared_project": true
      },
      "enabled": true
    }
  ]
}
```

## Team-Specific Google Projects

Each team with its own Google Cloud project:

```json
{
  "teams": [
    {
      "id": "client-a",
      "name": "Client A",
      "linear": {
        "api_key": "lin_api_client_a"
      },
      "google": {
        "credentials_path": "credentials/client-a-google.json",
        "drive_folder_id": "client_a_folder",
        "cloud_project_id": "client-a-project",
        "use_shared_project": false
      },
      "enabled": true,
      "notes": "Client A - isolated project for security"
    },
    {
      "id": "client-b",
      "name": "Client B",
      "linear": {
        "api_key": "lin_api_client_b"
      },
      "google": {
        "credentials_path": "credentials/client-b-google.json",
        "drive_folder_id": "client_b_folder",
        "cloud_project_id": "client-b-project",
        "use_shared_project": false
      },
      "enabled": true,
      "notes": "Client B - separate project for billing isolation"
    }
  ]
}
```

## Disabled Team

Temporarily disable a team without deleting it:

```json
{
  "teams": [
    {
      "id": "inactive-team",
      "name": "Inactive Team",
      "linear": {
        "api_key": "lin_api_xxxxxxxx"
      },
      "enabled": false,
      "notes": "Temporarily disabled - project on hold"
    }
  ]
}
```

## Field Descriptions

### Required Fields

- **id**: Unique identifier (lowercase, hyphens, no spaces)
- **name**: Display name
- **linear.api_key**: Linear API key (get from https://linear.app/settings/api)

### Optional Fields

- **google.credentials_path**: Path to Google credentials JSON file
- **google.drive_folder_id**: Google Drive folder ID for documents
- **google.cloud_project_id**: Google Cloud project ID
- **google.use_shared_project**: `true` to use shared project, `false` for team-specific
- **activecampaign.api_url**: ActiveCampaign API URL
- **activecampaign.api_key**: ActiveCampaign API key
- **enabled**: `true` to enable team, `false` to disable (default: `true`)
- **notes**: Optional notes about the team

## Best Practices

1. **Team IDs**: Use lowercase, hyphens, descriptive names
   - ✅ Good: `trade-ideas`, `client-acme`, `project-alpha`
   - ❌ Bad: `Team1`, `My Team`, `client_acme`

2. **Credentials Paths**: Use relative paths from workspace root
   - ✅ Good: `credentials/team-google.json`
   - ❌ Bad: `/Users/name/credentials.json` (absolute paths break on different machines)

3. **Security**: Never commit `config/teams.json` to git (it's gitignored)
   - Use `config/teams.json.template` for examples
   - Keep real credentials local only

4. **Organization**: Group related teams together
   - Use consistent naming
   - Add notes for context

5. **Validation**: Always validate after changes
   ```bash
   python scripts/validate_teams.py
   ```

## Common Patterns

### Pattern 1: Single Team, All Services
One team with Linear, Google, and ActiveCampaign configured.

### Pattern 2: Multiple Teams, Shared Google Project
Several teams sharing one Google Cloud project (simpler, lower cost).

### Pattern 3: Multiple Teams, Separate Projects
Each team has its own Google Cloud project (better isolation, separate billing).

### Pattern 4: Linear Only
Teams with just Linear API (no Google/ActiveCampaign automation).

## See Also

- `config/teams.json.template` - Template file
- `config/teams.json.example` - Example configurations
- `GETTING-STARTED.md` - Setup guide
- `TROUBLESHOOTING.md` - Common issues
