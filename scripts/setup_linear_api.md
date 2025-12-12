# Linear API Setup Guide

Step-by-step guide for setting up Linear API access.

## Step 1: Get Your Linear API Key

1. Log in to [Linear](https://linear.app)
2. Click your profile icon (bottom left)
3. Go to **Settings** → **API**
4. Under "Personal API Keys", click **"Create API Key"**
5. Give it a name: "Linear Agent Tasks" (or your choice)
6. Copy the API key (starts with `lin_api_`)
   - ⚠️ **Important:** You can only see this key once! Save it securely.

## Step 2: Get Your Team Key (Optional)

1. In Linear, look at your issue identifiers (e.g., `TRA-56`)
2. The prefix before the dash is your team key (e.g., `TRA`)
3. This is used to filter issues by team

## Step 3: Configure Environment

Add to your `.env` file:
```bash
LINEAR_API_KEY=lin_api_your_actual_api_key_here
LINEAR_TEAM_KEY=TRA  # Optional, your team key
```

## Step 4: Test Connection

Run the validation script:
```bash
python scripts/validate_apis.py
```

Or test manually:
```python
from linear_client import LinearClient

client = LinearClient()
issue = client.get_issue_by_identifier('TRA-56')
print(f"Issue: {issue.get('title')}")
```

## API Rate Limits

- **Limit:** 1,500 requests per hour
- The client automatically tracks rate limits
- If you hit the limit, wait before making more requests

## Troubleshooting

### "Invalid API key" error
- Verify the API key is correct (starts with `lin_api_`)
- Check for extra spaces or newlines
- Make sure the key hasn't been revoked in Linear settings

### "Rate limit exceeded" error
- Wait before making more requests
- The client tracks remaining requests
- Consider batching operations

### "Issue not found" error
- Verify the issue identifier is correct (e.g., `TRA-56`)
- Check that you have access to the team/workspace
- Verify the team key is correct

## Security Best Practices

1. **Never commit API keys to git**
   - `.env` file should be in `.gitignore` ✅
   - Use environment variables, not hardcoded keys

2. **Use personal API keys**
   - Each team member should have their own key
   - Revoke keys when no longer needed

3. **Limit key scope**
   - Personal API keys have access to your Linear account
   - Don't share keys between team members

4. **Rotate keys periodically**
   - Create new keys and revoke old ones
   - Update `.env` file with new key

## Additional Resources

- [Linear API Documentation](https://developers.linear.app/docs)
- [Linear GraphQL API](https://developers.linear.app/docs/graphql/working-with-the-graphql-api)
- [Linear API Rate Limits](https://developers.linear.app/docs/graphql/working-with-the-graphql-api#rate-limits)
