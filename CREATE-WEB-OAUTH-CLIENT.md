# Create Web Application OAuth Client

**Correct Approach:** Use "Web application" type to configure redirect URIs.

---

## Steps to Create Web Application OAuth Client

### 1. Go to Google Cloud Console
**Direct Link:** https://console.cloud.google.com/apis/credentials?project=theta-bliss-179022

### 2. Create OAuth Client
- Click **+ CREATE CREDENTIALS** → **OAuth client ID**

### 3. Configure OAuth Consent Screen (if first time)
- User Type: **External** (or Internal if Google Workspace)
- App name: **Linear Agent Tasks**
- Your email for support/developer
- Add scopes:
  - `https://www.googleapis.com/auth/documents`
  - `https://www.googleapis.com/auth/spreadsheets`
  - `https://www.googleapis.com/auth/drive.file`

### 4. Create Web Application Client
- **Application type: Web application** ⭐ (Important!)
- Name: **Linear Agent Tasks Web**
- **Authorized redirect URIs:**
  - Click **+ ADD URI** and add:
    - `http://localhost`
    - `http://localhost:8080`
    - `http://localhost:8080/`
- Click **CREATE**

### 5. Download Credentials
- Click **DOWNLOAD JSON**
- The file will be named like: `client_secret_XXXXX.json`
- Upload it to the workspace

### 6. Update Configuration
- Move file to `/workspace/credentials/`
- Update `.env`: `GOOGLE_CREDENTIALS_PATH=/workspace/credentials/NEW_FILE.json`
- Run authorization script

---

## After Creating Web Application Client

1. Upload the new JSON file to workspace
2. Update `.env` file
3. Run: `python3 scripts/get_oauth_token.py`
4. Complete authorization with proper redirect URI

---

**Note:** Web application clients allow you to configure redirect URIs, which is what we need!
