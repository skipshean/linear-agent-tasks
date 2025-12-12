#!/usr/bin/env python3
"""
OAuth Authorization Script for Google APIs

Run this script once to authorize Google APIs access.
It will open a browser (or provide a URL) for you to authorize.

Usage:
    python3 scripts/authorize_google_oauth.py
"""

import os
import json
import pickle
from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow

# Load environment
load_dotenv()

# Scopes needed
SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

def main():
    creds_path = os.getenv('GOOGLE_CREDENTIALS_PATH')
    if not creds_path:
        print("Error: GOOGLE_CREDENTIALS_PATH not set in .env")
        return 1
    
    if not os.path.exists(creds_path):
        print(f"Error: Credentials file not found: {creds_path}")
        return 1
    
    # Check for existing token
    token_path = creds_path.replace('.json', '_token.pickle')
    if os.path.exists(token_path):
        print("✅ Token file already exists!")
        print(f"   Token file: {token_path}")
        print("\nIf you need to re-authorize, delete the token file and run again.")
        return 0
    
    # Load client secret
    with open(creds_path, 'r') as f:
        client_config = json.load(f)
    
    # Create flow
    if 'installed' in client_config:
        flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
    elif 'web' in client_config:
        # Convert web to installed format for flow
        flow = InstalledAppFlow.from_client_config(
            {'installed': client_config['web']}, SCOPES
        )
    else:
        print("Error: Invalid OAuth client configuration")
        return 1
    
    print("=" * 60)
    print("Google OAuth Authorization")
    print("=" * 60)
    print("\nStarting OAuth flow...")
    print("This will open a browser for authorization.")
    print("\nIf browser doesn't open, visit the URL shown below.")
    print("=" * 60)
    
    try:
        # Try to run local server (opens browser)
        credentials = flow.run_local_server(port=0, open_browser=True)
    except Exception as e:
        # Fall back to manual URL
        print("\n⚠️  Could not open browser automatically.")
        print("\nPlease visit this URL to authorize:")
        auth_url, _ = flow.authorization_url(prompt='consent')
        print(f"\n{auth_url}\n")
        print("After authorization, you'll be redirected to localhost.")
        print("Copy the 'code' parameter from the redirect URL.")
        print("\nExample redirect URL:")
        print("http://localhost:8080/?code=4/0AeanS...&scope=...")
        print("\nEnter the authorization code:")
        code = input("Code: ").strip()
        flow.fetch_token(code=code)
        credentials = flow.credentials
    
    # Save token
    with open(token_path, 'wb') as token_file:
        pickle.dump(credentials, token_file)
    
    print("\n" + "=" * 60)
    print("✅ Authorization successful!")
    print("=" * 60)
    print(f"\nToken saved to: {token_path}")
    print("\nYou can now use Google APIs. The token will be reused automatically.")
    
    return 0

if __name__ == '__main__':
    exit(main())
