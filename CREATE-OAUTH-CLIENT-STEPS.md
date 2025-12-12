# Create New OAuth 2.0 Client - Step by Step

Since you're the owner, you can create a new OAuth client with proper redirect URI configuration.

---

## Quick Steps

### 1. Go to Google Cloud Console
**Direct Link:** https://console.cloud.google.com/apis/credentials?project=theta-bliss-179022

### 2. Create OAuth Client
- Click **+ CREATE CREDENTIALS** (top of page)
- Select **OAuth client ID**

### 3. Configure (if first time)
- If prompted for OAuth consent screen:
  - User Type: **External**
  - App name: **Linear Agent Tasks**
  - Your email for support/developer
  - Click through and add scopes:
    - `https://www.googleapis.com/auth/documents`
    - `https://www.googleapis.com/auth/spreadsheets`
    - `https://www.googleapis.com/auth/drive.file`

### 4. Create Desktop App Client
- Application type: **Desktop app**
- Name: **Linear Agent Tasks Desktop**
- Click **CREATE**

### 5. Configure Redirect URIs
- After creation, click on the new client to **EDIT**
- Under **Authorized redirect URIs**, click **+ ADD URI**
- Add these URIs (one at a time):
  1. `http://localhost`
  2. `http://localhost:8080`
  3. `urn:ietf:wg:oauth:2.0:oob`
- Click **SAVE**

### 6. Download Credentials
- Click **DOWNLOAD JSON**
- The file will download (e.g., `client_secret_XXXXX.json`)
- Upload it to the workspace
- Update `.env` with the new file path

---

## After Creating New Client

1. Upload the new JSON file to workspace
2. Update `.env`: `GOOGLE_CREDENTIALS_PATH=/workspace/credentials/NEW_FILE.json`
3. Run: `python3 scripts/get_oauth_token.py`
4. Complete authorization

---

**Alternative:** If you prefer, I can help you use the existing client with a workaround, but creating a new one is cleaner.
