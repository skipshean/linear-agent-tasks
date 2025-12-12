#!/usr/bin/env python3
"""
Get OAuth Token - Simplified Version

This script generates an authorization URL and saves the token after you provide the code.

Usage:
1. Run: python3 scripts/get_oauth_token.py
2. Visit the URL shown
3. Copy the authorization code from the redirect URL
4. Run again with the code: python3 scripts/get_oauth_token.py --code YOUR_CODE
"""

import os
import sys
import json
import pickle
from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow

load_dotenv()

SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

def main():
    creds_path = os.getenv('GOOGLE_CREDENTIALS_PATH')
    if not creds_path:
        print("Error: GOOGLE_CREDENTIALS_PATH not set")
        return 1
    
    token_path = creds_path.replace('.json', '_token.pickle')
    
    # Check if code provided as argument
    code = None
    if len(sys.argv) > 1 and sys.argv[1] == '--code' and len(sys.argv) > 2:
        code = sys.argv[2]
    
    # Check for existing token
    if os.path.exists(token_path) and not code:
        print("✅ Token already exists!")
        print(f"Token file: {token_path}")
        return 0
    
    # Load client config
    with open(creds_path, 'r') as f:
        client_config = json.load(f)
    
    if 'installed' in client_config:
        flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
    elif 'web' in client_config:
        flow = InstalledAppFlow.from_client_config({'installed': client_config['web']}, SCOPES)
    else:
        print("Error: Invalid OAuth configuration")
        return 1
    
    if code:
        # Exchange code for token
        print("Exchanging authorization code for token...")
        flow.fetch_token(code=code)
        credentials = flow.credentials
        
        # Save token
        with open(token_path, 'wb') as token_file:
            pickle.dump(credentials, token_file)
        
        print("✅ Token saved successfully!")
        print(f"Token file: {token_path}")
        return 0
    else:
        # Generate authorization URL
        auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
        
        print("=" * 60)
        print("OAUTH AUTHORIZATION")
        print("=" * 60)
        print("\n1. Visit this URL in your browser:")
        print(f"\n{auth_url}\n")
        print("2. Sign in with your Google account")
        print("3. Grant permissions")
        print("4. You'll be redirected to localhost")
        print("5. Copy the 'code' parameter from the redirect URL")
        print("\nExample redirect URL:")
        print("http://localhost:8080/?code=4/0AeanS...&scope=...")
        print("\n6. Run this command with the code:")
        print("python3 scripts/get_oauth_token.py --code YOUR_CODE_HERE")
        print("=" * 60)
        return 0

if __name__ == '__main__':
    exit(main())
