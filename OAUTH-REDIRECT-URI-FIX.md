# OAuth Redirect URI Fix

**Issue:** "Missing required parameter: redirect_uri" error

---

## Problem

The OAuth client configuration shows `redirect_uris: ["http://localhost"]`, but Google is complaining about missing redirect_uri.

---

## Solution: Update Google Cloud Console

The redirect URI must be **exactly** configured in Google Cloud Console.

### Steps to Fix:

1. **Go to Google Cloud Console:**
   - https://console.cloud.google.com/
   - Navigate to: APIs & Services → Credentials

2. **Find your OAuth 2.0 Client:**
   - Client ID: `702876153883-h70gq19jcld7eda4vt3qnnllfc446std.apps.googleusercontent.com`

3. **Edit the OAuth Client:**
   - Click on the client to edit

4. **Add Authorized Redirect URIs:**
   - Under "Authorized redirect URIs", add:
     - `http://localhost`
     - `http://localhost:8080`
     - `http://localhost:8080/`
     - `urn:ietf:wg:oauth:2.0:oob` (for manual code entry)

5. **Save the changes**

6. **Wait a few minutes** for changes to propagate

7. **Try the authorization URL again**

---

## Alternative: Use Manual Code Entry

If you can't update the redirect URIs, we can use a different flow that doesn't require a redirect:

1. Visit the authorization URL
2. After granting permissions, you'll see an error page (this is expected)
3. The page will show an authorization code
4. Copy that code
5. Use it with: `python3 scripts/get_oauth_token.py --code YOUR_CODE`

---

## Current Configuration

**Client ID:** `702876153883-h70gq19jcld7eda4vt3qnnllfc446std.apps.googleusercontent.com`  
**Redirect URI in config:** `http://localhost`  
**Required:** Must match Google Cloud Console settings

---

**Next Step:** Update the redirect URIs in Google Cloud Console, then try the authorization URL again.
