#!/usr/bin/env python3
"""
OAuth Token - OOB (Out-of-Band) Flow

Uses urn:ietf:wg:oauth:2.0:oob redirect URI which shows code on page.
This works even if redirect URIs aren't configured in Google Cloud Console.

Usage:
1. Run: python3 scripts/get_oauth_token_oob.py
2. Visit URL and authorize
3. Copy code from the page
4. Run: python3 scripts/get_oauth_token_oob.py --code YOUR_CODE
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
    
    # Check if code provided
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
    
    # Modify config to use OOB redirect URI
    if 'installed' in client_config:
        # Use OOB (out-of-band) redirect URI
        client_config['installed']['redirect_uris'] = ['urn:ietf:wg:oauth:2.0:oob']
        flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
    elif 'web' in client_config:
        # Convert to installed with OOB
        client_config['installed'] = {
            **client_config['web'],
            'redirect_uris': ['urn:ietf:wg:oauth:2.0:oob']
        }
        flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
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
        print("\nYou can now use Google APIs!")
        return 0
    else:
        # Generate authorization URL with OOB redirect
        auth_url, _ = flow.authorization_url(
            prompt='consent',
            access_type='offline'
        )
        
        print("=" * 60)
        print("OAUTH AUTHORIZATION (OOB Flow)")
        print("=" * 60)
        print("\nThis uses OOB (out-of-band) flow - no redirect URI needed!")
        print("\n1. Visit this URL in your browser:")
        print(f"\n{auth_url}\n")
        print("2. Sign in with your Google account")
        print("3. Grant permissions")
        print("4. Google will show the authorization code ON THE PAGE")
        print("   (You won't be redirected - the code appears on the consent page)")
        print("5. Copy the authorization code")
        print("   It will look like: 4/0AeanS...")
        print("\n6. Run this command with the code:")
        print("python3 scripts/get_oauth_token_oob.py --code YOUR_CODE")
        print("=" * 60)
        return 0

if __name__ == '__main__':
    exit(main())
