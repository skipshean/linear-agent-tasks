# Create New OAuth 2.0 Client

Since the existing OAuth client can't be edited, let's create a new one with proper redirect URI configuration.

---

## Steps to Create New OAuth Client

### 1. Go to Google Cloud Console
- https://console.cloud.google.com/
- Select project: **theta-bliss-179022**

### 2. Navigate to Credentials
- Go to: **APIs & Services** → **Credentials**
- Click: **+ CREATE CREDENTIALS** → **OAuth client ID**

### 3. Configure OAuth Consent Screen (if not done)
- If prompted, configure OAuth consent screen:
  - User Type: **External** (or Internal if using Google Workspace)
  - App name: **Linear Agent Tasks**
  - User support email: Your email
  - Developer contact: Your email
  - Click **Save and Continue**
  - Add scopes:
    - `https://www.googleapis.com/auth/documents`
    - `https://www.googleapis.com/auth/spreadsheets`
    - `https://www.googleapis.com/auth/drive.file`
  - Click **Save and Continue**
  - Add test users (if external)
  - Click **Save and Continue**

### 4. Create OAuth Client
- Application type: **Desktop app**
- Name: **Linear Agent Tasks Desktop**
- Click **Create**

### 5. Configure Redirect URIs
- After creation, you should be able to edit
- Under **Authorized redirect URIs**, add:
  - `http://localhost`
  - `http://localhost:8080`
  - `urn:ietf:wg:oauth:2.0:oob` (for manual code entry)

### 6. Download Credentials
- Click **Download JSON**
- Save the file
- Upload it to the workspace

---

## Alternative: Use Manual Code Entry Flow

If you can't create a new client, we can modify the script to use a flow that doesn't require redirect URI configuration.

---

## Quick Check: Current Client Permissions

**Current Client ID:** `702876153883-h70gq19jcld7eda4vt3qnnllfc446std.apps.googleusercontent.com`

**Check:**
1. Do you have Owner or Editor role on the project?
2. Can you see the "Edit" button on the OAuth client?
3. Are you the creator of the OAuth client?

If you can't edit it, creating a new client is the best solution.

---

**Next Step:** Create a new OAuth 2.0 Client ID with proper redirect URI configuration, or let me know if you'd like to try a different approach.
