# API Setup Tools Complete ✅

**Date:** December 12, 2025  
**Status:** Ready for API configuration

---

## What's Been Created

### 1. Setup Tools ✅

**Interactive Setup Script:**
- ✅ `/scripts/setup_apis.py` - Interactive script to guide API configuration
- Prompts for all required credentials
- Validates inputs
- Creates `.env` file automatically

**Validation Script:**
- ✅ `/scripts/validate_apis.py` - Tests all API connections
- Checks environment variables
- Tests actual API connectivity
- Provides helpful error messages

### 2. Configuration Templates ✅

**Environment Template:**
- ✅ `/.env.template` - Template with all required variables
- Includes comments and examples
- Safe to commit to git (no actual credentials)

### 3. Setup Guides ✅

**Detailed Documentation:**
- ✅ `/scripts/setup_linear_api.md` - Linear API setup guide
- ✅ `/scripts/setup_google_apis.md` - Google APIs setup guide (Service Account & OAuth)
- ✅ `/scripts/setup_activecampaign_api.md` - ActiveCampaign API setup guide

---

## Quick Start

### Option 1: Interactive Setup (Recommended)

```bash
# Run interactive setup
python scripts/setup_apis.py
```

This will guide you through:
1. Linear API key configuration
2. Google APIs credentials setup
3. ActiveCampaign API configuration

### Option 2: Manual Setup

1. Copy template:
   ```bash
   cp .env.template .env
   ```

2. Edit `.env` with your credentials:
   ```bash
   # Linear API
   LINEAR_API_KEY=lin_api_...
   
   # Google APIs
   GOOGLE_CREDENTIALS_PATH=/path/to/credentials.json
   
   # ActiveCampaign API
   ACTIVE_CAMPAIGN_API_URL=https://your-account.api-us1.com
   ACTIVE_CAMPAIGN_API_KEY=your_api_key
   ```

3. Validate configuration:
   ```bash
   python scripts/validate_apis.py
   ```

---

## Setup Steps for Each API

### Linear API (5 minutes)

1. Go to Linear → Settings → API
2. Create Personal API Key
3. Copy key (starts with `lin_api_`)
4. Add to `.env`: `LINEAR_API_KEY=lin_api_...`

**Guide:** See `scripts/setup_linear_api.md`

### Google APIs (15-20 minutes)

**Service Account (Recommended):**
1. Go to Google Cloud Console
2. Create project
3. Enable: Docs API, Sheets API, Drive API
4. Create Service Account
5. Download JSON key
6. Share Google Drive folders with service account email
7. Add to `.env`: `GOOGLE_CREDENTIALS_PATH=/path/to/key.json`

**Guide:** See `scripts/setup_google_apis.md`

### ActiveCampaign API (5 minutes)

1. Go to ActiveCampaign → Settings → Developer
2. Get API URL and API Key
3. Add to `.env`:
   ```bash
   ACTIVE_CAMPAIGN_API_URL=https://your-account.api-us1.com
   ACTIVE_CAMPAIGN_API_KEY=your_key
   ```

**Guide:** See `scripts/setup_activecampaign_api.md`

---

## Validation

After setup, validate your configuration:

```bash
python scripts/validate_apis.py
```

Expected output:
```
✅ LINEAR_API_KEY is set (lin_api_...)
✅ GOOGLE_CREDENTIALS_PATH is set (/path/to/...)
✅ ACTIVE_CAMPAIGN_API_URL is set (https://...)
✅ ACTIVE_CAMPAIGN_API_KEY is set (...)
✅ Linear API connected (User: Your Name)
✅ Google APIs connected (Docs & Sheets)
✅ ActiveCampaign API connected (can list tags)
✅ All configured APIs are working correctly!
```

---

## Troubleshooting

### "File not found" errors
- Verify file paths are correct
- Use absolute paths instead of relative
- Check file permissions

### "Authentication failed" errors
- Verify API keys are correct
- Check for extra spaces/newlines in `.env`
- Re-download credentials if needed

### "API not enabled" errors
- Enable required APIs in Google Cloud Console
- Verify API access in ActiveCampaign settings
- Check account permissions

### See detailed guides:
- `scripts/setup_linear_api.md` - Linear troubleshooting
- `scripts/setup_google_apis.md` - Google APIs troubleshooting
- `scripts/setup_activecampaign_api.md` - ActiveCampaign troubleshooting

---

## Security Notes

✅ **`.env` file is in `.gitignore`** - Credentials won't be committed

**Best Practices:**
- Never commit API keys to git
- Use environment variables, not hardcoded keys
- Rotate keys periodically
- Use service accounts for automation (Google)
- Limit permissions to minimum required

---

## Next Steps

1. ✅ **Setup Complete** - All tools and guides ready
2. ⏳ **Configure APIs** - Run `python scripts/setup_apis.py`
3. ⏳ **Validate** - Run `python scripts/validate_apis.py`
4. ⏳ **Start Executing** - Run `python scripts/execute_tasks.py --phase quick-wins`

---

## Files Created

### Setup Tools
- `/scripts/setup_apis.py` - Interactive setup script
- `/scripts/validate_apis.py` - API validation script
- `/.env.template` - Environment variables template

### Documentation
- `/scripts/setup_linear_api.md` - Linear API guide
- `/scripts/setup_google_apis.md` - Google APIs guide
- `/scripts/setup_activecampaign_api.md` - ActiveCampaign API guide
- `/API-SETUP-COMPLETE.md` - This summary

---

**Ready to configure!** Run `python scripts/setup_apis.py` to get started.
