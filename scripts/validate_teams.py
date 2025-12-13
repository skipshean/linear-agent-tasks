#!/usr/bin/env python3
"""
Validate team configurations and API connections.

This is the updated validation script that works with teams.json
instead of .env files.

Usage:
    python scripts/validate_teams.py
    python scripts/validate_teams.py --team trade-ideas
"""

import sys
import os
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(__file__))

from team_manager import TeamManager


def validate_team(team_id: str, manager: TeamManager) -> Dict:
    """Validate a single team's configuration."""
    team_config = manager.get_team(team_id)
    if not team_config:
        return {
            'valid': False,
            'error': f'Team "{team_id}" not found'
        }
    
    team_name = team_config.get('name', team_id)
    results = {
        'team_id': team_id,
        'team_name': team_name,
        'valid': True,
        'linear': {'configured': False, 'working': False},
        'google': {'configured': False, 'working': False},
        'activecampaign': {'configured': False, 'working': False},
        'issues': []
    }
    
    # Validate Linear API
    linear_key = manager.get_linear_api_key(team_id)
    if linear_key:
        results['linear']['configured'] = True
        try:
            from linear_client import LinearClient
            client = LinearClient(api_key=linear_key)
            query = "query { viewer { name email } }"
            response = client._make_request(query)
            if 'viewer' in response:
                viewer = response['viewer']
                results['linear']['working'] = True
                results['linear']['user'] = viewer.get('name', 'Unknown')
                results['linear']['email'] = viewer.get('email', 'Unknown')
            else:
                results['linear']['working'] = False
                results['issues'].append('Linear API: Invalid response')
        except Exception as e:
            results['linear']['working'] = False
            results['issues'].append(f'Linear API: {str(e)[:100]}')
    else:
        results['issues'].append('Linear API key not configured')
    
    # Validate Google APIs
    google_config = manager.get_google_config(team_id)
    if google_config and google_config.get('credentials_path'):
        results['google']['configured'] = True
        creds_path = google_config.get('credentials_path')
        if Path(creds_path).exists():
            try:
                from google_client import GoogleDocsClient
                client = GoogleDocsClient(credentials_path=creds_path)
                # If we got here without exception, credentials work
                results['google']['working'] = True
            except Exception as e:
                results['google']['working'] = False
                error_msg = str(e)
                if 'credentials' in error_msg.lower() or 'auth' in error_msg.lower():
                    results['issues'].append('Google API: Authentication failed')
                else:
                    results['issues'].append(f'Google API: {error_msg[:100]}')
        else:
            results['google']['working'] = False
            results['issues'].append(f'Google credentials file not found: {creds_path}')
    else:
        results['google']['configured'] = False
    
    # Validate ActiveCampaign API
    ac_config = manager.get_activecampaign_config(team_id)
    if ac_config and ac_config.get('api_url') and ac_config.get('api_key'):
        results['activecampaign']['configured'] = True
        try:
            from activecampaign_client import ActiveCampaignClient
            client = ActiveCampaignClient(
                api_url=ac_config['api_url'],
                api_key=ac_config['api_key']
            )
            # Test with a simple API call
            tags = client.list_tags(limit=1)
            results['activecampaign']['working'] = True
        except Exception as e:
            results['activecampaign']['working'] = False
            error_msg = str(e)
            if '401' in error_msg or 'unauthorized' in error_msg.lower():
                results['issues'].append('ActiveCampaign API: Authentication failed')
            elif 'url' in error_msg.lower() or '404' in error_msg:
                results['issues'].append('ActiveCampaign API: Invalid URL')
            else:
                results['issues'].append(f'ActiveCampaign API: {error_msg[:100]}')
    else:
        results['activecampaign']['configured'] = False
    
    if results['issues']:
        results['valid'] = False
    
    return results


def main():
    """Main validation function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Validate team configurations')
    parser.add_argument('--team', help='Validate specific team (default: all teams)')
    
    args = parser.parse_args()
    
    try:
        manager = TeamManager()
    except FileNotFoundError as e:
        print("❌ Team configuration not found")
        print(f"   {e}\n")
        print("Next steps:")
        print("  1. Run: python scripts/setup.py")
        print("  2. This will create config/teams.json and guide you through setup")
        return 1
    
    teams = manager.list_teams()
    if not teams:
        print("❌ No teams configured\n")
        print("Next steps:")
        print("  1. Run: python scripts/setup.py")
        print("  2. Follow the interactive prompts to set up your first team")
        print("  3. At minimum, you need a Linear API key")
        return 1
    
    print("=" * 60)
    print("Team Configuration Validation")
    print("=" * 60 + "\n")
    
    if args.team:
        # Validate specific team
        results = validate_team(args.team, manager)
        print_team_results(results)
    else:
        # Validate all teams
        all_valid = True
        for team in teams:
            team_id = team.get('id')
            results = validate_team(team_id, manager)
            print_team_results(results)
            if not results['valid']:
                all_valid = False
            print()
        
        print("=" * 60)
        if all_valid:
            print("✅ All teams are properly configured!")
            return 0
        else:
            print("⚠️  Some teams have configuration issues")
            return 1


def print_team_results(results: Dict):
    """Print validation results for a team."""
    team_name = results.get('team_name', results.get('team_id', 'Unknown'))
    print(f"Team: {team_name} ({results.get('team_id', 'unknown')})")
    print("-" * 60)
    
    # Linear
    linear = results.get('linear', {})
    if linear.get('configured'):
        if linear.get('working'):
            user = linear.get('user', 'Unknown')
            print(f"  ✅ Linear API: Connected (User: {user})")
        else:
            print(f"  ❌ Linear API: Configured but not working")
    else:
        print(f"  ⚠️  Linear API: Not configured")
    
    # Google
    google = results.get('google', {})
    if google.get('configured'):
        if google.get('working'):
            print(f"  ✅ Google APIs: Connected")
        else:
            print(f"  ❌ Google APIs: Configured but not working")
    else:
        print(f"  ⏭️  Google APIs: Not configured (optional)")
    
    # ActiveCampaign
    ac = results.get('activecampaign', {})
    if ac.get('configured'):
        if ac.get('working'):
            print(f"  ✅ ActiveCampaign API: Connected")
        else:
            print(f"  ❌ ActiveCampaign API: Configured but not working")
    else:
        print(f"  ⏭️  ActiveCampaign API: Not configured (optional)")
    
    # Issues
    issues = results.get('issues', [])
    if issues:
        print(f"\n  Issues:")
        for issue in issues:
            print(f"    - {issue}")


if __name__ == '__main__':
    sys.exit(main())
