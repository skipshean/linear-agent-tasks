#!/usr/bin/env python3
"""
Quick OAuth - Generate fresh authorization URL and catch code automatically

This script will:
1. Generate a fresh authorization URL
2. Start a local server to catch the redirect
3. Automatically exchange the code for a token

Usage:
    python3 scripts/quick_oauth.py
"""

import os
import json
import pickle
import http.server
import socketserver
import threading
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
from google_auth_oauthlib.flow import Flow

load_dotenv()

SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

auth_code = None
server_ready = False

class OAuthHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global auth_code, server_ready
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        
        if 'code' in params:
            auth_code = params['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = """
            <html><head><title>Success</title></head>
            <body style="font-family: Arial; text-align: center; padding: 50px;">
            <h1 style="color: green;">Authorization Successful!</h1>
            <p>You can close this window.</p>
            <p>Return to the terminal to see the result.</p>
            </body></html>
            """
            self.wfile.write(html.encode('utf-8'))
            return
        elif 'error' in params:
            error = params['error'][0]
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f"""
            <html><head><title>Error</title></head>
            <body style="font-family: Arial; text-align: center; padding: 50px;">
            <h1 style="color: red;">Authorization Error</h1>
            <p>Error: {error}</p>
            <p>Please check the terminal.</p>
            </body></html>
            """.encode())
            return
        
        self.send_response(404)
        self.end_headers()
    
    def log_message(self, format, *args):
        # Suppress server logs
        pass

def run_server(port=8080):
    global server_ready
    with socketserver.TCPServer(("", port), OAuthHandler) as httpd:
        server_ready = True
        httpd.timeout = 300
        httpd.handle_request()

def main():
    creds_path = os.getenv('GOOGLE_CREDENTIALS_PATH')
    if not creds_path:
        print("Error: GOOGLE_CREDENTIALS_PATH not set")
        return 1
    
    token_path = creds_path.replace('.json', '_token.pickle')
    
    if os.path.exists(token_path):
        print("✅ Token already exists!")
        return 0
    
    # Load config
    with open(creds_path, 'r') as f:
        client_config = json.load(f)
    
    # Setup flow
    if 'web' in client_config:
        redirect_uri = client_config['web']['redirect_uris'][0] if client_config['web'].get('redirect_uris') else 'http://localhost:8080'
        
        # Parse port from redirect_uri
        from urllib.parse import urlparse
        parsed_uri = urlparse(redirect_uri)
        port = parsed_uri.port if parsed_uri.port else (80 if parsed_uri.scheme == 'http' else 443)
        
        # Create installed app config from web config
        installed_config = {
            'installed': {
                'client_id': client_config['web']['client_id'],
                'client_secret': client_config['web']['client_secret'],
                'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
                'token_uri': 'https://oauth2.googleapis.com/token',
                'redirect_uris': [redirect_uri]  # Use single redirect_uri
            }
        }
        flow = Flow.from_client_config(installed_config, SCOPES)
        # Explicitly set the redirect_uri on the flow and OAuth2Session
        flow.redirect_uri = redirect_uri
        if hasattr(flow, 'oauth2session'):
            flow.oauth2session.redirect_uri = redirect_uri
    else:
        print("Error: Web application config not found")
        return 1
    
    # Start server in background on the correct port
    print(f"Starting local server on port {port}...")
    if port == 80:
        print("⚠️  WARNING: Port 80 requires root privileges. If this fails, use a different redirect_uri.")
    server_thread = threading.Thread(target=run_server, args=(port,), daemon=True)
    server_thread.start()
    
    # Wait for server to be ready
    import time
    for _ in range(10):
        if server_ready:
            break
        time.sleep(0.5)
    
    # Generate auth URL (redirect_uri is set on flow object)
    # Verify redirect_uri is set
    if not hasattr(flow, 'redirect_uri') or not flow.redirect_uri:
        flow.redirect_uri = redirect_uri
    
    auth_url, _ = flow.authorization_url(
        prompt='consent',
        access_type='offline'
    )
    
    # Verify redirect_uri is in the URL
    if 'redirect_uri' not in auth_url:
        print(f"⚠️  WARNING: redirect_uri not found in auth URL!")
        print(f"   Expected redirect_uri: {redirect_uri}")
        print(f"   Adding redirect_uri to URL manually...")
        from urllib.parse import urlencode, urlparse, parse_qs, urlunparse
        parsed = urlparse(auth_url)
        params = parse_qs(parsed.query)
        params['redirect_uri'] = [redirect_uri]
        new_query = urlencode(params, doseq=True)
        auth_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))
    
    print("=" * 60)
    print("OAUTH AUTHORIZATION")
    print("=" * 60)
    print(f"\n✅ Local server running on port {port}")
    print(f"✅ Redirect URI configured: {redirect_uri}")
    print("\n1. Visit this URL in your browser:")
    print(f"\n{auth_url}\n")
    print("2. Sign in and grant permissions")
    print("3. You'll be redirected and the code will be captured automatically")
    print("\nWaiting for authorization...")
    print("(The server will automatically catch the redirect)")
    print("=" * 60)
    
    # Wait for code
    timeout = 300  # 5 minutes
    start_time = time.time()
    while not auth_code and (time.time() - start_time) < timeout:
        time.sleep(1)
        if auth_code:
            break
    
    if not auth_code:
        print("\n❌ Timeout: No authorization code received")
        print("Please try again")
        return 1
    
    # Exchange code for token (redirect_uri is set on flow object)
    print(f"\n✅ Code received! Exchanging for token...")
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
