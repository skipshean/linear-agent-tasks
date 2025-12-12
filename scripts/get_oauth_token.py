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
    
    # Handle both web and installed app types
    if 'web' in client_config:
        # Web application - use redirect URIs from config
        # Convert to installed format for InstalledAppFlow
        installed_config = {
            'installed': {
                'client_id': client_config['web']['client_id'],
                'client_secret': client_config['web']['client_secret'],
                'auth_uri': client_config['web'].get('auth_uri', 'https://accounts.google.com/o/oauth2/auth'),
                'token_uri': client_config['web'].get('token_uri', 'https://oauth2.googleapis.com/token'),
                'redirect_uris': client_config['web'].get('redirect_uris', ['http://localhost'])
            }
        }
        flow = InstalledAppFlow.from_client_config(installed_config, SCOPES)
    elif 'installed' in client_config:
        # Desktop app - ensure redirect URIs are set
        if 'redirect_uris' not in client_config['installed']:
            client_config['installed']['redirect_uris'] = ['http://localhost']
        flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
    else:
        print("Error: Invalid OAuth configuration")
        print("Expected 'web' or 'installed' key in JSON")
        return 1
    
    if code:
        # Exchange code for token
        print("Exchanging authorization code for token...")
        # Ensure redirect_uri matches what was used in authorization URL
        # For web apps, use the first redirect URI from config
        if 'web' in client_config:
            redirect_uri = client_config['web'].get('redirect_uris', ['http://localhost'])[0]
        elif 'installed' in client_config:
            redirect_uri = client_config['installed'].get('redirect_uris', ['http://localhost'])[0]
        else:
            redirect_uri = 'http://localhost'
        
        # Fetch token with explicit redirect_uri
        flow.fetch_token(code=code, redirect_uri=redirect_uri)
        credentials = flow.credentials
        
        # Save token
        with open(token_path, 'wb') as token_file:
            pickle.dump(credentials, token_file)
        
        print("✅ Token saved successfully!")
        print(f"Token file: {token_path}")
        return 0
    else:
        # For installed apps, we can use OOB (out-of-band) flow
        # This shows the code on the consent page instead of redirecting
        try:
            # Try with explicit redirect_uri parameter
            redirect_uri = 'http://localhost'
            if 'installed' in client_config and 'redirect_uris' in client_config['installed']:
                redirect_uri = client_config['installed']['redirect_uris'][0]
            
            auth_url, state = flow.authorization_url(
                prompt='consent',
                access_type='offline',
                include_granted_scopes='true'
            )
            
            # Manually add redirect_uri to URL if not present
            if 'redirect_uri=' not in auth_url:
                from urllib.parse import urlencode, urlparse, parse_qs, urlunparse
                parsed = urlparse(auth_url)
                params = parse_qs(parsed.query)
                params['redirect_uri'] = [redirect_uri]
                new_query = urlencode(params, doseq=True)
                auth_url = urlunparse(parsed._replace(query=new_query))
        except Exception as e:
            # Fallback: generate URL without explicit redirect_uri
            auth_url, state = flow.authorization_url(
                prompt='consent',
                access_type='offline'
            )
            redirect_uri = 'http://localhost'
        
        print("=" * 60)
        print("OAUTH AUTHORIZATION")
        print("=" * 60)
        print(f"\nRedirect URI: {redirect_uri}")
        print("\n1. Visit this URL in your browser:")
        print(f"\n{auth_url}\n")
        print("2. Sign in with your Google account")
        print("3. Grant permissions")
        print(f"4. After authorization:")
        print("   - If redirected to localhost, copy the 'code' from the URL")
        print("   - If you see an error page, look for the authorization code on the page")
        print("   - The code will look like: 4/0AeanS...")
        print("\n5. Run this command with the code:")
        print("python3 scripts/get_oauth_token.py --code YOUR_CODE_HERE")
        print("=" * 60)
        print("\n⚠️  If you get 'redirect_uri' error:")
        print("   Go to Google Cloud Console → Credentials → Edit OAuth Client")
        print("   Add 'http://localhost' to Authorized redirect URIs")
        print("=" * 60)
        return 0

if __name__ == '__main__':
    exit(main())
