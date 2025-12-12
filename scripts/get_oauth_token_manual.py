#!/usr/bin/env python3
"""
OAuth Token - Manual Code Entry (No Redirect URI Required)

This version uses a flow that works even if redirect URI isn't configured.

Usage:
1. Run: python3 scripts/get_oauth_token_manual.py
2. Visit the URL and authorize
3. Copy the code from the page (even if there's an error)
4. Run: python3 scripts/get_oauth_token_manual.py --code YOUR_CODE
"""

import os
import sys
import json
import pickle
from dotenv import load_dotenv
from google_auth_oauthlib.flow import Flow

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
    
    # Get client details
    if 'installed' in client_config:
        client_info = client_config['installed']
    elif 'web' in client_config:
        client_info = client_config['web']
    else:
        print("Error: Invalid OAuth configuration")
        return 1
    
    client_id = client_info['client_id']
    client_secret = client_info['client_secret']
    
    if code:
        # Exchange code for token manually
        print("Exchanging authorization code for token...")
        
        from google.auth.transport.requests import Request
        import requests
        
        token_url = 'https://oauth2.googleapis.com/token'
        data = {
            'code': code,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': 'http://localhost',  # Must match what was used in auth URL
            'grant_type': 'authorization_code'
        }
        
        response = requests.post(token_url, data=data)
        
        if response.status_code == 200:
            token_data = response.json()
            
            # Create credentials object
            from google.oauth2.credentials import Credentials
            credentials = Credentials(
                token=token_data.get('access_token'),
                refresh_token=token_data.get('refresh_token'),
                token_uri='https://oauth2.googleapis.com/token',
                client_id=client_id,
                client_secret=client_secret,
                scopes=SCOPES
            )
            
            # Save token
            with open(token_path, 'wb') as token_file:
                pickle.dump(credentials, token_file)
            
            print("✅ Token saved successfully!")
            print(f"Token file: {token_path}")
            return 0
        else:
            print(f"❌ Error exchanging code: {response.status_code}")
            print(response.text)
            return 1
    else:
        # Generate authorization URL
        # Use a simple redirect URI that should work
        redirect_uri = 'http://localhost'
        
        auth_url = (
            f"https://accounts.google.com/o/oauth2/auth?"
            f"response_type=code&"
            f"client_id={client_id}&"
            f"redirect_uri={redirect_uri}&"
            f"scope={'+'.join(SCOPES)}&"
            f"access_type=offline&"
            f"prompt=consent"
        )
        
        print("=" * 60)
        print("OAUTH AUTHORIZATION (Manual Code Entry)")
        print("=" * 60)
        print("\n1. Visit this URL in your browser:")
        print(f"\n{auth_url}\n")
        print("2. Sign in with your Google account")
        print("3. Grant permissions")
        print("4. You may see an error page - that's OK!")
        print("5. Look for the authorization code on the page")
        print("   - It may be in the URL: ?code=4/0AeanS...")
        print("   - Or displayed on the error page")
        print("   - Or check browser address bar")
        print("\n6. Copy the code (starts with '4/')")
        print("\n7. Run this command with the code:")
        print("python3 scripts/get_oauth_token_manual.py --code YOUR_CODE")
        print("=" * 60)
        return 0

if __name__ == '__main__':
    exit(main())
