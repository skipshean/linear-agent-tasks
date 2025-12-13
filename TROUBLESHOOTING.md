# Troubleshooting Guide

Common issues and solutions for the Linear Agent Tasks system.

## Quick Diagnostics

Before troubleshooting, run these diagnostic commands:

```bash
# Comprehensive health check
python scripts/setup.py --check

# Validate team configurations
python scripts/validate_teams.py

# Status dashboard
python scripts/setup.py --status
```

## Setup Issues

### "Team configuration not found"

**Error:**
```
FileNotFoundError: Team configuration file not found: config/teams.json
```

**Solution:**
1. Run the setup script:
   ```bash
   python scripts/setup.py
   ```
2. This will create `config/teams.json` and guide you through team setup

**Next Steps:**
- Follow the interactive prompts
- At minimum, you need a Linear API key
- Optional: Add Google and ActiveCampaign credentials

---

### "Dependencies missing"

**Error:**
```
ImportError: No module named 'requests'
```

**Solution:**
1. Install dependencies:
   ```bash
   pip install -r scripts/requirements.txt
   ```
2. Or let setup script install them:
   ```bash
   python scripts/setup.py
   ```

**Next Steps:**
- Verify installation: `python scripts/setup.py --check`
- If issues persist, check Python version (needs 3.8+)

---

### "Linear API key not working"

**Error:**
```
Linear API connection failed: HTTP 401
```

**Solution:**
1. Verify your API key in Linear:
   - Go to Linear Settings → API
   - Check that the key exists and is active
   - Create a new key if needed
2. Update team configuration:
   ```bash
   python scripts/setup_team.py
   ```
3. Verify connection:
   ```bash
   python scripts/validate_teams.py --team YOUR_TEAM_ID
   ```

**Next Steps:**
- Make sure you copied the entire API key
- Check that the key hasn't been revoked
- Verify you have the correct Linear workspace

---

### "Google credentials not found"

**Error:**
```
Google credentials path required. Set GOOGLE_CREDENTIALS_PATH env var.
```

**Solution:**
1. Google APIs are optional - you can skip them if not needed
2. If you need Google APIs:
   - Get credentials from Google Cloud Console
   - Update team config:
     ```bash
     python scripts/setup_team.py
     ```
   - Enter the path to your credentials JSON file

**Next Steps:**
- See `CLOUD-EXECUTION-GUIDE.md` for Google Cloud project setup
- Credentials can be service account or OAuth
- Make sure the file path is correct

---

## Team Configuration Issues

### "Team not found"

**Error:**
```
Team 'trade-ideas' not found
```

**Solution:**
1. List configured teams:
   ```bash
   python scripts/agent_workflow.py --list-teams
   ```
2. If team doesn't exist, add it:
   ```bash
   python scripts/setup_team.py
   ```
3. Verify team ID matches exactly (case-sensitive)

**Next Steps:**
- Check `config/teams.json` to see configured teams
- Team IDs are case-sensitive
- Use `--list-teams` to see exact team IDs

---

### "No Linear API key configured for team"

**Error:**
```
No Linear API key configured for team: trade-ideas
```

**Solution:**
1. Update team configuration:
   ```bash
   python scripts/setup_team.py
   ```
2. Select the team when prompted (or create new)
3. Enter Linear API key

**Next Steps:**
- Get API key from Linear Settings → API
- Make sure to save the configuration
- Verify with: `python scripts/validate_teams.py --team YOUR_TEAM`

---

## Task Execution Issues

### "No agent-suitable tasks found"

**Message:**
```
No agent-suitable tasks found.
```

**This is normal!** Not all tasks are suitable for automation.

**What makes a task agent-suitable:**
- Clear description (50+ characters)
- Automation keywords (create, build, document, etc.)
- Acceptance criteria or requirements
- Not assigned to someone else
- Not blocked or canceled

**Solution:**
1. Try a different team:
   ```bash
   python scripts/agent_workflow.py --team OTHER_TEAM --analyze
   ```
2. Try a specific project:
   ```bash
   python scripts/agent_workflow.py --team YOUR_TEAM --project PROJECT_ID --analyze
   ```
3. Add more detail to tasks in Linear (descriptions, acceptance criteria)

**Next Steps:**
- Review tasks in Linear and add more detail
- Some tasks may need manual execution
- Check if tasks are assigned (unassign if needed)

---

### "Could not initialize API clients"

**Error:**
```
Warning: Could not initialize API clients: ...
```

**Solution:**
1. Run health check:
   ```bash
   python scripts/setup.py --check
   ```
2. Fix any issues identified
3. Verify credentials:
   ```bash
   python scripts/validate_teams.py
   ```

**Common Causes:**
- Missing API keys
- Invalid credentials
- Network issues
- Rate limits exceeded

**Next Steps:**
- Check the specific error message
- Verify credentials are correct
- Test API connections individually

---

### "Rate limit exceeded"

**Error:**
```
Rate limit exceeded. Wait before making more requests.
```

**Solution:**
1. Linear API limit: 1500 requests/hour
2. Wait before retrying
3. Use `--limit` to work on fewer tasks:
   ```bash
   python scripts/agent_workflow.py --team YOUR_TEAM --work --limit 5
   ```

**Next Steps:**
- Check current rate limit status
- Space out task execution
- Consider cloud execution for large batches

---

## Cloud Execution Issues

### "Cloud package not created"

**Error:**
```
Warning: Could not create package: ...
```

**Solution:**
1. Check write permissions in workspace
2. Verify disk space
3. Check that team configuration is valid

**Next Steps:**
- Check `.cloud-packages/` directory permissions
- Verify `config/teams.json` is valid JSON
- Try creating package manually if needed

---

### "Task not found in queue"

**Error:**
```
Task TRA-56 not found in queue
```

**Solution:**
1. Check if task was submitted:
   ```bash
   python scripts/agent_workflow.py --check-status
   ```
2. Verify task ID is correct
3. Check `.cloud-queue/pending/` directory

**Next Steps:**
- Re-submit task if needed
- Check Linear comments for submission confirmation
- Verify queue files exist

---

## Configuration Issues

### "Invalid JSON in teams.json"

**Error:**
```
JSONDecodeError: Expecting value: line X column Y
```

**Solution:**
1. Validate JSON syntax:
   ```bash
   python -m json.tool config/teams.json
   ```
2. Fix any syntax errors
3. Use template as reference:
   ```bash
   cat config/teams.json.template
   ```

**Next Steps:**
- Check for missing commas, quotes, brackets
- Validate JSON online if needed
- Restore from backup if corrupted

---

### "Credentials file not found"

**Error:**
```
FileNotFoundError: credentials/trade-ideas-google-credentials.json
```

**Solution:**
1. Verify file path in `config/teams.json`
2. Use absolute path if relative path doesn't work
3. Update team configuration:
   ```bash
   python scripts/setup_team.py
   ```

**Next Steps:**
- Check file actually exists
- Verify path is correct (absolute vs relative)
- Re-download credentials if needed

---

## Still Having Issues?

1. **Run diagnostics:**
   ```bash
   python scripts/setup.py --check
   python scripts/validate_teams.py
   ```

2. **Check logs:**
   - Error messages usually include next steps
   - Check Linear comments for task-specific errors

3. **Review documentation:**
   - `GETTING-STARTED.md` - First-time setup
   - `README.md` - Main documentation
   - `QUICK-REFERENCE.md` - Command reference

4. **Verify system requirements:**
   - Python 3.8+
   - All dependencies installed
   - Valid API credentials

5. **Common fixes:**
   - Re-run setup: `python scripts/setup.py`
   - Re-validate: `python scripts/validate_teams.py`
   - Check team config: `cat config/teams.json`

---

## Getting Help

If you're still stuck:

1. Check the error message - it usually includes next steps
2. Run health check: `python scripts/setup.py --check`
3. Review relevant documentation
4. Check that all prerequisites are met
5. Verify credentials are correct and not expired

Most issues can be resolved by:
- Running the setup script again
- Validating team configurations
- Checking API credentials
- Reviewing error messages for specific guidance
