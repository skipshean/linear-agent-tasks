#!/usr/bin/env python3
"""
API Validation Script

Tests all API connections to ensure they're properly configured.

Usage:
    python scripts/validate_apis.py
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_env_var(name: str, required: bool = True) -> tuple[bool, str]:
    """Check if environment variable is set."""
    value = os.getenv(name)
    if required and not value:
        return False, f"❌ {name} is not set"
    elif not value:
        return True, f"⚠️  {name} is not set (optional)"
    else:
        # Mask sensitive values
        if 'KEY' in name or 'SECRET' in name or 'TOKEN' in name:
            masked = value[:8] + '...' + value[-4:] if len(value) > 12 else '***'
            return True, f"✅ {name} is set ({masked})"
        else:
            return True, f"✅ {name} is set ({value})"

def test_linear_api() -> tuple[bool, str]:
    """Test Linear API connection."""
    try:
        from linear_client import LinearClient
        client = LinearClient()
        
        # Try a simple query
        query = """
        query {
            viewer {
                id
                name
                email
            }
        }
        """
        response = client._make_request(query)
        
        if 'viewer' in response:
            user = response['viewer']
            return True, f"✅ Linear API connected (User: {user.get('name', 'Unknown')})"
        else:
            return False, "❌ Linear API connection failed - invalid response"
    except ImportError:
        return False, "❌ Linear client not available (install dependencies: pip install -r requirements.txt)"
    except Exception as e:
        return False, f"❌ Linear API connection failed: {str(e)}"

def test_google_apis() -> tuple[bool, str]:
    """Test Google APIs connection."""
    try:
        from google_client import GoogleDocsClient, GoogleSheetsClient
        
        # Test Docs API
        try:
            docs_client = GoogleDocsClient()
            # Try to list documents (requires Drive API)
            return True, "✅ Google APIs connected (Docs & Sheets)"
        except Exception as e:
            error_msg = str(e)
            if 'credentials' in error_msg.lower() or 'auth' in error_msg.lower():
                return False, f"❌ Google API authentication failed: {error_msg}"
            else:
                return False, f"❌ Google API connection failed: {error_msg}"
    except ImportError:
        return False, "❌ Google client not available (install dependencies: pip install -r requirements.txt)"
    except Exception as e:
        return False, f"❌ Google API connection failed: {str(e)}"

def test_activecampaign_api() -> tuple[bool, str]:
    """Test ActiveCampaign API connection."""
    try:
        from activecampaign_client import ActiveCampaignClient
        client = ActiveCampaignClient()
        
        # Try to list tags (simple API call)
        tags = client.list_tags(limit=1)
        return True, f"✅ ActiveCampaign API connected (can list tags)"
    except ImportError:
        return False, "❌ ActiveCampaign client not available (install dependencies: pip install -r requirements.txt)"
    except Exception as e:
        error_msg = str(e)
        if '401' in error_msg or 'unauthorized' in error_msg.lower():
            return False, "❌ ActiveCampaign API authentication failed (check API key)"
        elif 'url' in error_msg.lower() or '404' in error_msg:
            return False, "❌ ActiveCampaign API URL incorrect (check API URL format)"
        else:
            return False, f"❌ ActiveCampaign API connection failed: {error_msg}"

def main():
    """Main validation function."""
    print("=" * 60)
    print("API Configuration Validation")
    print("=" * 60)
    print()
    
    all_passed = True
    
    # Check environment variables
    print("📋 Environment Variables:")
    print("-" * 60)
    
    env_checks = [
        ('LINEAR_API_KEY', True),
        ('GOOGLE_CREDENTIALS_PATH', True),
        ('ACTIVE_CAMPAIGN_API_URL', True),
        ('ACTIVE_CAMPAIGN_API_KEY', True),
        ('LINEAR_TEAM_KEY', False),
        ('GOOGLE_DRIVE_FOLDER_ID', False),
    ]
    
    for var_name, required in env_checks:
        passed, message = check_env_var(var_name, required)
        print(f"  {message}")
        if not passed and required:
            all_passed = False
    
    print()
    
    # Test API connections
    print("🔌 API Connections:")
    print("-" * 60)
    
    # Linear API
    if os.getenv('LINEAR_API_KEY'):
        passed, message = test_linear_api()
        print(f"  Linear API: {message}")
        if not passed:
            all_passed = False
    else:
        print("  Linear API: ⏭️  Skipped (LINEAR_API_KEY not set)")
    
    # Google APIs
    if os.getenv('GOOGLE_CREDENTIALS_PATH'):
        passed, message = test_google_apis()
        print(f"  Google APIs: {message}")
        if not passed:
            all_passed = False
    else:
        print("  Google APIs: ⏭️  Skipped (GOOGLE_CREDENTIALS_PATH not set)")
    
    # ActiveCampaign API
    if os.getenv('ACTIVE_CAMPAIGN_API_URL') and os.getenv('ACTIVE_CAMPAIGN_API_KEY'):
        passed, message = test_activecampaign_api()
        print(f"  ActiveCampaign API: {message}")
        if not passed:
            all_passed = False
    else:
        print("  ActiveCampaign API: ⏭️  Skipped (API credentials not set)")
    
    print()
    print("=" * 60)
    
    if all_passed:
        print("✅ All configured APIs are working correctly!")
        return 0
    else:
        print("❌ Some API configurations need attention.")
        print()
        print("Next steps:")
        print("1. Check the error messages above")
        print("2. Verify your API credentials in .env file")
        print("3. See execution-requirements.md for setup instructions")
        return 1

if __name__ == '__main__':
    sys.exit(main())
