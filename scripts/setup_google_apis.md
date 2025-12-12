# Google APIs Setup Guide

Detailed step-by-step guide for setting up Google Docs and Sheets API access.

## Option 1: Service Account (Recommended for Automation)

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Enter project name: "Linear Agent Tasks" (or your choice)
4. Click "Create"

### Step 2: Enable Required APIs

1. In your project, go to "APIs & Services" → "Library"
2. Search for and enable:
   - **Google Docs API**
   - **Google Sheets API**
   - **Google Drive API**

### Step 3: Create Service Account

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "Service Account"
3. Enter service account details:
   - Name: "linear-agent-tasks"
   - Description: "Service account for Linear agent task automation"
4. Click "Create and Continue"
5. Skip role assignment (click "Continue")
6. Click "Done"

### Step 4: Create and Download Key

1. Click on the service account you just created
2. Go to "Keys" tab
3. Click "Add Key" → "Create new key"
4. Select "JSON" format
5. Click "Create"
6. JSON file will download automatically
7. **Save this file securely** - you'll need it for `GOOGLE_CREDENTIALS_PATH`

### Step 5: Share Google Drive Folders

1. Open the downloaded JSON file
2. Find the `client_email` field (e.g., `linear-agent-tasks@project-id.iam.gserviceaccount.com`)
3. In Google Drive, share the folder where you want documents created with this email
4. Give it "Editor" permissions

### Step 6: Configure Environment

Add to your `.env` file:
```bash
GOOGLE_CREDENTIALS_PATH=/path/to/downloaded-service-account-key.json
GOOGLE_DRIVE_FOLDER_ID=your-folder-id  # Optional
```

---

## Option 2: OAuth 2.0 (For Personal Use)

### Step 1-2: Same as Service Account

Create project and enable APIs (see Option 1, Steps 1-2)

### Step 3: Create OAuth Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, configure OAuth consent screen:
   - User Type: "External" (or "Internal" if using Google Workspace)
   - App name: "Linear Agent Tasks"
   - User support email: Your email
   - Developer contact: Your email
   - Click "Save and Continue"
   - Add scopes:
     - `https://www.googleapis.com/auth/documents`
     - `https://www.googleapis.com/auth/spreadsheets`
     - `https://www.googleapis.com/auth/drive.file`
   - Click "Save and Continue"
   - Add test users (if external)
   - Click "Save and Continue"
4. Create OAuth client:
   - Application type: "Desktop app"
   - Name: "Linear Agent Tasks"
   - Click "Create"
5. Download JSON credentials
6. **Save this file securely**

### Step 4: First-Time Authorization

On first use, the script will:
1. Open browser for OAuth authorization
2. Sign in with your Google account
3. Grant permissions
4. Save token for future use

### Step 5: Configure Environment

Add to your `.env` file:
```bash
GOOGLE_CREDENTIALS_PATH=/path/to/downloaded-oauth-credentials.json
```

---

## Testing Your Setup

Run the validation script:
```bash
python scripts/validate_apis.py
```

Or test manually:
```python
from google_client import GoogleDocsClient

client = GoogleDocsClient()
doc_id = client.create_document("Test Document")
print(f"Created document: {doc_id}")
```

---

## Troubleshooting

### "File not found" error
- Verify the path to credentials JSON file is correct
- Use absolute path instead of relative path

### "Permission denied" error
- For service account: Make sure you shared the Google Drive folder with the service account email
- For OAuth: Make sure you granted all required permissions

### "API not enabled" error
- Go to Google Cloud Console → APIs & Services → Library
- Enable: Google Docs API, Google Sheets API, Google Drive API

### "Invalid credentials" error
- Verify the JSON file is not corrupted
- Re-download credentials if needed
- Check that the service account/OAuth client is active

---

## Security Best Practices

1. **Never commit credentials to git**
   - `.env` file should be in `.gitignore` ✅
   - Credentials JSON files should not be in repository

2. **Use service account for automation**
   - More secure than OAuth for automated scripts
   - Can be restricted to specific folders

3. **Limit permissions**
   - Only share necessary folders with service account
   - Use least privilege principle

4. **Rotate credentials periodically**
   - Regenerate service account keys annually
   - Revoke old keys when creating new ones

---

## Additional Resources

- [Google Cloud Console](https://console.cloud.google.com/)
- [Google Docs API Documentation](https://developers.google.com/docs/api)
- [Google Sheets API Documentation](https://developers.google.com/sheets/api)
- [Service Account Best Practices](https://cloud.google.com/iam/docs/best-practices-service-accounts)
