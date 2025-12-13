# OAuth Setup Instructions

**Date:** December 12, 2025  
**Status:** OAuth credentials uploaded, authorization needed

---

## ✅ OAuth Credentials Uploaded

**File:** `client_secret_702876153883-h70gq19jcld7eda4vt3qnnllfc446std.apps.googleusercontent.com.json`  
**Location:** `/workspace/credentials/`  
**Type:** OAuth 2.0 Client Secret (Desktop app)

---

## 🔐 Authorization Required

The OAuth credentials file has been uploaded, but **authorization is required** before use.

### Step 1: Run Authorization Script

```bash
python3 scripts/authorize_google_oauth.py
```

This will:
1. Open a browser (or provide a URL)
2. Prompt you to sign in with your Google account
3. Ask you to grant permissions for:
   - Google Docs API
   - Google Sheets API
   - Google Drive API
4. Save the authorization token for future use

### Step 2: Complete Authorization

**If browser opens:**
- Sign in with your Google account
- Review and grant permissions
- You'll be redirected automatically
- Token will be saved

**If browser doesn't open:**
- Copy the authorization URL from the console
- Open it in your browser
- Sign in and grant permissions
- Copy the `code` parameter from the redirect URL
- Paste it when prompted

### Step 3: Verify Authorization

After authorization, test with:

```bash
python3 scripts/execute_tasks.py --task TRA-56
```

---

## 📝 Current Configuration

**Environment Variable:**
```bash
GOOGLE_CREDENTIALS_PATH=/workspace/credentials/client_secret_702876153883-h70gq19jcld7eda4vt3qnnllfc446std.apps.googleusercontent.com.json
```

**Token File (will be created after authorization):**
```
/workspace/credentials/client_secret_702876153883-h70gq19jcld7eda4vt3qnnllfc446std.apps.googleusercontent.com_token.pickle
```

---

## 🔄 Token Management

- **Token is saved automatically** after first authorization
- **Token is reused** for all future API calls
- **No re-authorization needed** unless token expires or is revoked
- **Token file is in `.gitignore`** (won't be committed)

---

## ⚠️ Important Notes

1. **One-time setup:** Authorization only needed once
2. **Uses your quota:** Files created will use your personal Google Drive quota (15 GB free)
3. **Secure:** Token is stored locally and not shared
4. **Revocable:** You can revoke access in Google Account settings

---

## 🚀 After Authorization

Once authorized, you can:
- ✅ Create Google Docs (TRA-56, TRA-54, TRA-109)
- ✅ Create Google Sheets (TRA-41-48, TRA-49)
- ✅ All Google Docs/Sheets tasks will work

---

**Next Step:** Run `python3 scripts/authorize_google_oauth.py` to complete authorization.
