# ActiveCampaign API Setup Guide

Step-by-step guide for setting up ActiveCampaign API access.

## Step 1: Get Your API Credentials

1. Log in to [ActiveCampaign](https://www.activecampaign.com)
2. Go to **Settings** → **Developer**
3. Find your API credentials:
   - **API URL:** Format is `https://{your-account}.api-us1.com`
     - Replace `{your-account}` with your account name
     - The region (`us1`, `us2`, etc.) depends on your account
   - **API Key:** Your personal API key

⚠️ **Important:** Use the **Trade Ideas ActiveCampaign account** for these tasks.

## Step 2: Verify API Access

1. Check that API access is enabled for your account
2. Verify your account plan supports API access
3. Note your API rate limits (varies by plan, typically ~10,000 requests/day)

## Step 3: Configure Environment

Add to your `.env` file:
```bash
ACTIVE_CAMPAIGN_API_URL=https://your-account.api-us1.com
ACTIVE_CAMPAIGN_API_KEY=your_api_key_here
```

**Example:**
```bash
ACTIVE_CAMPAIGN_API_URL=https://tradeideas.api-us1.com
ACTIVE_CAMPAIGN_API_KEY=abc123def456...
```

## Step 4: Test Connection

Run the validation script:
```bash
python scripts/validate_apis.py
```

Or test manually:
```python
from activecampaign_client import ActiveCampaignClient

client = ActiveCampaignClient()
tags = client.list_tags(limit=5)
print(f"Found {len(tags)} tags")
```

## API Rate Limits

- **Typical limit:** ~10,000 requests per day (varies by plan)
- The client includes rate limiting delays
- Monitor your usage in ActiveCampaign dashboard

## Common API Endpoints Used

- `/api/3/tags` - Tag management (TRA-59, TRA-60)
- `/api/3/automations` - Automation workflows (TRA-63, TRA-65)
- `/api/3/goals` - Goal configuration (TRA-65)
- `/api/3/contacts` - Contact data (for data exports)

## Troubleshooting

### "401 Unauthorized" error
- Verify your API key is correct
- Check that API access is enabled for your account
- Make sure you're using the correct account

### "404 Not Found" or "Invalid URL" error
- Verify the API URL format is correct
- Check the region (us1, us2, etc.) matches your account
- Ensure the account name in URL is correct

### "Rate limit exceeded" error
- Wait before making more requests
- Check your daily API usage in ActiveCampaign
- Consider batching operations or adding delays

### "Tag already exists" warning
- This is expected behavior - the client checks for duplicates
- Existing tags are skipped, new tags are created
- Check the execution results for created vs. skipped counts

## Security Best Practices

1. **Never commit API keys to git**
   - `.env` file should be in `.gitignore` ✅
   - Use environment variables, not hardcoded keys

2. **Use account-specific keys**
   - Each ActiveCampaign account has its own API credentials
   - Don't share keys between accounts

3. **Limit key permissions**
   - API keys have full account access
   - Rotate keys if compromised

4. **Monitor API usage**
   - Check ActiveCampaign dashboard for API usage
   - Set up alerts for unusual activity

## Important Notes for Task Execution

### TRA-59: Create Tags
- **Critical:** Check for existing tags before creating
- Use case-insensitive comparison
- Account: Trade Ideas ActiveCampaign account

### TRA-60: Bracket Naming
- ActiveCampaign doesn't have folders
- Use `[Category] Tag Name` format for alphabetical grouping
- All tags should follow this convention

### TRA-65: Add Goal
- Goals are linked to automations
- Verify automation ID before creating goal
- Goal name: "Became Customer During Onboard"

## Additional Resources

- [ActiveCampaign API Documentation](https://developers.activecampaign.com/reference/overview)
- [ActiveCampaign API Authentication](https://developers.activecampaign.com/reference/authentication)
- [ActiveCampaign API Rate Limits](https://developers.activecampaign.com/reference/rate-limits)
