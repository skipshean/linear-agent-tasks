# Getting Started Guide

**Welcome!** This guide will get you up and running in 5 minutes.

## Prerequisites

- Python 3.8 or higher
- Access to Linear (for API key)
- (Optional) Google Cloud account for Google APIs
- (Optional) ActiveCampaign account for ActiveCampaign APIs

## Step 1: Install Dependencies

```bash
pip install -r scripts/requirements.txt
```

Or let the setup script do it for you (see Step 2).

## Step 2: Run Setup

```bash
python scripts/setup.py
```

This interactive script will:
1. Check if dependencies are installed (and offer to install them)
2. Guide you through setting up your first team
3. Help you configure API credentials

### What You'll Need

**Required:**
- **Linear API Key**: Get this from Linear Settings → API → Create Personal API Key

**Optional (can add later):**
- **Google Credentials**: For Google Docs/Sheets automation
- **ActiveCampaign Credentials**: For ActiveCampaign automation

## Step 3: Verify Setup

```bash
python scripts/setup.py --check
```

This will verify:
- ✅ Dependencies are installed
- ✅ Teams are configured
- ✅ API connections work

## Step 4: Start Using

```bash
# See what teams you have
python scripts/agent_workflow.py --list-teams

# Analyze tasks across all teams
python scripts/agent_workflow.py --analyze-all

# Work on tasks for a specific team
python scripts/agent_workflow.py --team your-team-id --work
```

## Common First-Time Issues

### "Team configuration not found"
- Run `python scripts/setup.py` to create your first team

### "Dependencies missing"
- Run `pip install -r scripts/requirements.txt`
- Or let `setup.py` install them automatically

### "Linear API key not working"
- Verify your API key in Linear Settings → API
- Make sure you copied the entire key
- Check that the key hasn't been revoked

### "No agent-suitable tasks found"
- This is normal! Tasks need clear descriptions to be agent-suitable
- Try analyzing a different team or project
- Some tasks may need more detail before automation

## Next Steps

- Read the [README.md](README.md) for full documentation
- Check [QUICK-REFERENCE.md](QUICK-REFERENCE.md) for common commands
- See [CLOUD-EXECUTION-GUIDE.md](CLOUD-EXECUTION-GUIDE.md) for cloud execution

## Need Help?

- Run `python scripts/setup.py --check` to diagnose issues
- Check `python scripts/validate_teams.py` to verify team configurations
- Review error messages - they usually include next steps
