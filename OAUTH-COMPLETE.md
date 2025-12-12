# Complete OAuth Authorization

**Status:** Authorization URL generated - Complete the flow to get token

---

## 🔐 Authorization Steps

### Step 1: Visit Authorization URL

The authorization URL has been generated. You need to:

1. **Copy this URL and open it in your browser:**
   ```
   (URL will be shown when you run the script)
   ```

2. **Sign in** with your Google account (the one that owns the shared folder)

3. **Review and grant permissions** for:
   - Google Docs API
   - Google Sheets API  
   - Google Drive API

4. **You'll be redirected** to `http://localhost:XXXX/?code=...`

5. **Copy the `code` parameter** from the redirect URL

### Step 2: Exchange Code for Token

Once you have the code, run:

```bash
python3 scripts/get_oauth_token.py --code YOUR_CODE_HERE
```

Replace `YOUR_CODE_HERE` with the code from the redirect URL.

### Step 3: Verify

Test that it works:

```bash
python3 scripts/execute_tasks.py --task TRA-56
```

---

## 📝 Quick Reference

**Get Authorization URL:**
```bash
python3 scripts/get_oauth_token.py
```

**Complete Authorization (with code):**
```bash
python3 scripts/get_oauth_token.py --code 4/0AeanS...
```

**Test Authorization:**
```bash
python3 scripts/execute_tasks.py --task TRA-56
```

---

## ✅ After Authorization

Once the token is saved, you can:
- ✅ Execute TRA-56 (Document lifecycle states)
- ✅ Execute TRA-54 and TRA-109 (SOP tasks)
- ✅ Execute all Google Sheets tasks (TRA-41-48, TRA-49)

---

**Note:** The token is saved locally and will be reused automatically for all future API calls.
