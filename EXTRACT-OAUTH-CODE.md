# Extract OAuth Authorization Code

**Status:** Redirect worked! You were redirected to localhost with "it works!"

---

## Find the Authorization Code

When you were redirected to `http://localhost/?code=...`, the authorization code is in the URL.

### Step 1: Check the Browser URL

Look at the address bar in your browser. The URL should look like:

```
http://localhost/?code=4/0AeanS1234567890abcdef...&scope=...
```

### Step 2: Copy the Code

Copy everything after `code=` and before the next `&` (or end of URL).

**Example:**
- Full URL: `http://localhost/?code=4/0AeanS1234567890abcdef&scope=...`
- Code to copy: `4/0AeanS1234567890abcdef`

### Step 3: Use the Code

Run this command with your code:

```bash
python3 scripts/get_oauth_token.py --code YOUR_CODE_HERE
```

Replace `YOUR_CODE_HERE` with the code you copied.

---

## If You Can't Find the Code

If you closed the browser or can't see the URL:

1. **Run the local server script:**
   ```bash
   python3 scripts/authorize_oauth_server.py
   ```

2. **Visit the authorization URL** it shows

3. **After authorization**, the server will automatically capture the code

---

## Quick Test

After providing the code and getting the token, test with:

```bash
python3 scripts/execute_tasks.py --task TRA-56
```

---

**Next Step:** Copy the code from the localhost URL and run the command above.
