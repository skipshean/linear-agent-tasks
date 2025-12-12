# Task Execution Requirements

## Quick Setup

**Fastest way to get started:**
```bash
# Run interactive setup script
python scripts/setup_apis.py

# Then validate your configuration
python scripts/validate_apis.py
```

**Or manually:**
1. Copy `.env.template` to `.env`
2. Fill in your API credentials
3. Run validation script

See detailed guides:
- [Linear API Setup](scripts/setup_linear_api.md)
- [Google APIs Setup](scripts/setup_google_apis.md)
- [ActiveCampaign API Setup](scripts/setup_activecampaign_api.md)

---

## API Access Required

### 1. Linear API
- **Purpose:** Fetch task details, update issue status, add comments
- **Required Scopes:**
  - `read` - Read issues, projects, teams
  - `write` - Update issues, create comments
- **Rate Limit:** 1500 requests/hour
- **Setup:** 
  - Create Linear API key
  - Configure authentication
  - Test connection

### 2. Google Docs API
- **Purpose:** Create and edit Google Docs (TRA-56, TRA-54)
- **Required Scopes:**
  - `https://www.googleapis.com/auth/documents`
  - `https://www.googleapis.com/auth/drive.file`
- **Setup:**
  - Enable Google Docs API in Google Cloud Console
  - Create service account or OAuth credentials
  - Share service account email with target Google Drive

### 3. Google Sheets API
- **Purpose:** Create dashboards and data tabs (TRA-41, TRA-42-48, TRA-49)
- **Required Scopes:**
  - `https://www.googleapis.com/auth/spreadsheets`
  - `https://www.googleapis.com/auth/drive.file`
- **Setup:**
  - Enable Google Sheets API in Google Cloud Console
  - Use same credentials as Docs API
  - Configure spreadsheet permissions

### 4. ActiveCampaign API
- **Purpose:** Create tags, configure automations, add goals (TRA-59, TRA-60, TRA-63-65)
- **Required:**
  - API URL (e.g., `https://{account}.api-us1.com`)
  - API Key
- **Rate Limits:** Varies by plan, typically 10,000 requests/day
- **Setup:**
  - Get API credentials from ActiveCampaign account
  - Test API connection
  - Verify account: Trade Ideas ActiveCampaign account

## Data Sources Required

### 1. Task Details from Linear
- Issue descriptions
- Acceptance criteria
- Attachments (templates, lists, etc.)
- Related issues and dependencies

### 2. Master Tag List (TRA-59)
- Complete list of tags to create
- Naming conventions
- Category structure

### 3. Email Content (TRA-63)
- 6 email copies/content
- Subject lines
- Sequence order

### 4. Dashboard Specifications
- Schema definitions (TRA-41)
- Formula definitions (TRA-42-48)
- Metric calculations
- Data source mappings

### 5. Lifecycle State Definitions (TRA-56)
- List of all lifecycle states
- State descriptions
- Transition rules

### 6. SOP Content/Template (TRA-54)
- Existing SOP structure
- Content to paste (TRA-109)
- System-specific details

### 7. Forecast Data (TRA-49, TRA-106-108)
- Intent segment definitions
- Probability weights (Drop 8)
- Historical MRR data

## Execution Environment

### Python Environment
- Python 3.8+
- Required packages:
  - `linear-sdk` or `requests` for Linear API
  - `google-api-python-client` for Google APIs
  - `requests` for ActiveCampaign API
  - `python-dotenv` for environment variables

### Configuration Files
- `.env` file with API keys:
  ```
  LINEAR_API_KEY=...
  GOOGLE_CREDENTIALS_PATH=...
  ACTIVE_CAMPAIGN_API_URL=...
  ACTIVE_CAMPAIGN_API_KEY=...
  ```

### File Structure
```
/workspace/
  ├── task-execution-guides/    # Detailed guides for each task
  ├── execution-plan.md          # Overall execution plan
  ├── execution-requirements.md  # This file
  ├── scripts/                   # Execution scripts
  │   ├── linear_client.py
  │   ├── google_client.py
  │   ├── activecampaign_client.py
  │   └── execute_tasks.py
  └── .env                       # API credentials (gitignored)
```

## Execution Workflow

### Phase 1: Setup
1. Configure API access
2. Test all API connections
3. Fetch task details from Linear
4. Gather required data sources

### Phase 2: Quick Wins
1. TRA-56: Document lifecycle states
2. TRA-65: Add goal
3. TRA-109: Paste SOP structure
4. TRA-54: Create SOP Manual

### Phase 3: Foundation
1. TRA-41: Base Data Tabs
2. TRA-59: Create tags
3. TRA-60: Bracket naming

### Phase 4: Dashboards
1. TRA-42-48: Build all dashboards
2. TRA-49: Forecast sheet
3. TRA-106-108: Forecast subtasks

### Phase 5: Configuration
1. TRA-63: Add emails
2. TRA-64: Add tag triggers
3. TRA-40: Data connection
4. TRA-51: Naming conventions
5. TRA-52: Domain validation
6. TRA-53: Tracking verification

## Validation & Testing

### Before Marking Complete
- [ ] Verify task requirements met
- [ ] Test functionality (where possible)
- [ ] Check API rate limits not exceeded
- [ ] Update Linear issue with results
- [ ] Add comments with links/details
- [ ] Document any issues or blockers

### Error Handling
- API rate limit errors → Implement retry logic with backoff
- Missing data → Document and flag for manual input
- API errors → Log and report, don't fail silently
- Validation failures → Report specific issues

## Notes

### Rate Limiting
- Linear: 1500 requests/hour
- Google APIs: Varies by operation
- ActiveCampaign: ~10,000 requests/day (varies by plan)
- Implement batching and rate limiting in scripts

### Data Privacy
- Don't commit API keys to git
- Use environment variables
- Follow data handling best practices
- Respect API terms of service

### Manual Steps
Some tasks require manual intervention:
- TRA-40: Initial CSV exports
- TRA-52: DNS changes (needs approval)
- TRA-53: Code changes (needs review)
- TRA-61: ❌ Canceled (not possible in AC)
