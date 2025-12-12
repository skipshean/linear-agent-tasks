# Google Drive Quota Issue - Solution

**Date:** December 12, 2025  
**Issue:** Service account has 0 GB Drive storage quota

---

## Problem Identified

**Service Account:** `702876153883-compute@developer.gserviceaccount.com`  
**Quota Limit:** 0.00 GB  
**Error:** "The user's Drive storage quota has been exceeded"

**Root Cause:**
- Service accounts created via Google Cloud Compute Engine have **no Drive storage quota** by default
- Even when creating files in a shared folder, the quota is still checked against the service account
- This is a Google Cloud limitation, not a permissions issue

---

## Solutions

### Solution 1: Use OAuth 2.0 Instead of Service Account (Recommended)

**Steps:**
1. Create OAuth 2.0 credentials in Google Cloud Console
2. Download OAuth credentials JSON
3. Update `.env`: `GOOGLE_CREDENTIALS_PATH=/path/to/oauth-credentials.json`
4. On first use, complete OAuth flow (browser will open)
5. Files created will use your personal Drive quota

**Pros:**
- Uses your personal Drive quota (15 GB free)
- No quota limitations
- Full access to your Drive

**Cons:**
- Requires browser interaction on first use
- Less suitable for fully automated scripts

---

### Solution 2: Request Quota Increase for Service Account

**Steps:**
1. Go to Google Cloud Console → IAM & Admin → Service Accounts
2. Select the service account
3. Request quota increase (may require Google Workspace admin)
4. Or upgrade Google Workspace plan for more quota

**Note:** This may not be possible for Compute Engine service accounts

---

### Solution 3: Use Domain-Wide Delegation (Google Workspace Only)

**Steps:**
1. Enable domain-wide delegation for service account
2. Grant Drive API scopes
3. Impersonate a user with Drive quota
4. Create files as that user

**Requirements:**
- Google Workspace domain
- Admin access
- User account with Drive quota

---

### Solution 4: Manual Workaround (Temporary)

**For TRA-56 and other Google Docs tasks:**
1. Create documents manually in Google Drive
2. Share with team
3. Update Linear issues with document links
4. Mark tasks as complete with manual note

---

## Recommended Action

**Immediate:** Use Solution 1 (OAuth 2.0) for development/testing
**Long-term:** Set up domain-wide delegation (Solution 3) if using Google Workspace

---

## Implementation

### Switch to OAuth 2.0

1. **Create OAuth Credentials:**
   - Google Cloud Console → APIs & Services → Credentials
   - Create OAuth 2.0 Client ID
   - Application type: Desktop app
   - Download JSON

2. **Update Environment:**
   ```bash
   GOOGLE_CREDENTIALS_PATH=/path/to/oauth-credentials.json
   ```

3. **First-Time Authorization:**
   - Script will open browser
   - Sign in with Google account
   - Grant permissions
   - Token saved for future use

4. **Test:**
   ```bash
   python3 scripts/execute_tasks.py --task TRA-56
   ```

---

## Current Status

- ✅ **Permissions:** Working (can access shared folder)
- ✅ **API Access:** Working (can list files)
- ❌ **Storage Quota:** Service account has 0 GB quota
- ✅ **Workaround Available:** OAuth 2.0 credentials

---

**Last Updated:** December 12, 2025
