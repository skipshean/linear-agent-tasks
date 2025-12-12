#!/usr/bin/env python3
"""
OAuth Authorization with Local Server

This script starts a local server to catch the OAuth redirect,
which works better with web application OAuth clients.

Usage:
    python3 scripts/authorize_oauth_server.py
"""

import os
import json
import pickle
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
from google_auth_oauthlib.flow import Flow

load_dotenv()

SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# Global variable to store the authorization code
auth_code = None

class OAuthHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        
        if 'code' in params:
            auth_code = params['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"""
            <html>
            <body>
            <h1>Authorization Successful!</h1>
            <p>You can close this window and return to the terminal.</p>
            <p>The authorization code has been captured.</p>
            </body>
            </html>
            """)
            return
        elif 'error' in params:
            error = params['error'][0]
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f"""
            <html>
            <body>
            <h1>Authorization Error</h1>
            <p>Error: {error}</p>
            <p>Please check the terminal for instructions.</p>
            </body>
            </html>
            """.encode())
            return
        
        self.send_response(404)
        self.end_headers()

def main():
    creds_path = os.getenv('GOOGLE_CREDENTIALS_PATH')
    if not creds_path:
        print("Error: GOOGLE_CREDENTIALS_PATH not set")
        return 1
    
    token_path = creds_path.replace('.json', '_token.pickle')
    
    # Check for existing token
    if os.path.exists(token_path):
        print("✅ Token already exists!")
        print(f"Token file: {token_path}")
        return 0
    
    # Load client config
    with open(creds_path, 'r') as f:
        client_config = json.load(f)
    
    # Handle web application client
    if 'web' in client_config:
        # Convert to installed format for Flow
        installed_config = {
            'installed': {
                'client_id': client_config['web']['client_id'],
                'client_secret': client_config['web']['client_secret'],
                'auth_uri': client_config['web'].get('auth_uri', 'https://accounts.google.com/o/oauth2/auth'),
                'token_uri': client_config['web'].get('token_uri', 'https://oauth2.googleapis.com/token'),
                'redirect_uris': client_config['web'].get('redirect_uris', ['http://localhost:8080'])
            }
        }
        flow = Flow.from_client_config(installed_config, SCOPES)
        redirect_uri = 'http://localhost:8080'
    elif 'installed' in client_config:
        flow = Flow.from_client_config(client_config, SCOPES)
        redirect_uri = client_config['installed'].get('redirect_uris', ['http://localhost:8080'])[0]
    else:
        print("Error: Invalid OAuth configuration")
        return 1
    
    # Generate authorization URL
    auth_url, _ = flow.authorization_url(
        prompt='consent',
        access_type='offline'
    )
    
    print("=" * 60)
    print("OAUTH AUTHORIZATION (Local Server)")
    print("=" * 60)
    print(f"\nStarting local server on {redirect_uri}...")
    print("\n1. Visit this URL in your browser:")
    print(f"\n{auth_url}\n")
    print("2. Sign in with your Google account")
    print("3. Grant permissions")
    print("4. You'll be redirected back and the code will be captured automatically")
    print("\nWaiting for authorization...")
    print("=" * 60)
    
    # Start local server
    PORT = 8080
    with socketserver.TCPServer(("", PORT), OAuthHandler) as httpd:
        httpd.timeout = 300  # 5 minute timeout
        try:
            httpd.handle_request()  # Handle one request
        except KeyboardInterrupt:
            print("\n\nServer stopped")
            return 1
    
    if not auth_code:
        print("\n❌ No authorization code received")
        print("Please try again or check the browser for any errors")
        return 1
    
    # Exchange code for token
    print(f"\n✅ Authorization code received!")
    print("Exchanging code for token...")
    
    flow.fetch_token(code=auth_code)
    credentials = flow.credentials
    
    # Save token
    with open(token_path, 'wb') as token_file:
        pickle.dump(credentials, token_file)
    
    print("\n" + "=" * 60)
    print("✅ Authorization successful!")
    print("=" * 60)
    print(f"\nToken saved to: {token_path}")
    print("\nYou can now use Google APIs!")
    
    return 0

if __name__ == '__main__':
    exit(main())
