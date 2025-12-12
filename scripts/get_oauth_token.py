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
    
    # Ensure redirect_uri is set correctly in config
    if 'installed' in client_config:
        # Make sure redirect_uris includes localhost
        if 'redirect_uris' not in client_config['installed']:
            client_config['installed']['redirect_uris'] = ['http://localhost']
        elif 'http://localhost' not in client_config['installed']['redirect_uris']:
            client_config['installed']['redirect_uris'].append('http://localhost')
        flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
    elif 'web' in client_config:
        # Convert web to installed format
        installed_config = {
            'installed': {
                **client_config['web'],
                'redirect_uris': client_config['web'].get('redirect_uris', ['http://localhost'])
            }
        }
        flow = InstalledAppFlow.from_client_config(installed_config, SCOPES)
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
