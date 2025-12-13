#!/usr/bin/env python3
"""
Unified Setup Script - First-time setup and health checks.

This script provides a guided setup experience for new users and
health checks for existing installations.

Usage:
    python scripts/setup.py          # Interactive setup
    python scripts/setup.py --check  # Health check
    python scripts/setup.py --status # Status dashboard
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Optional

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(__file__))


def check_dependencies() -> tuple[bool, List[str]]:
    """Check if Python dependencies are installed."""
    missing = []
    required = [
        'requests',
        'google-auth',
        'google-auth-oauthlib',
        'google-auth-httplib2',
        'google-api-python-client',
        'python-dotenv'
    ]
    
    for package in required:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    return len(missing) == 0, missing


def install_dependencies() -> bool:
    """Install Python dependencies."""
    req_file = Path(__file__).parent / "requirements.txt"
    if not req_file.exists():
        print("❌ requirements.txt not found")
        return False
    
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(req_file)])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False


def check_teams_config() -> tuple[bool, Optional[Dict]]:
    """Check if teams.json exists and is valid."""
    workspace_root = Path(__file__).parent.parent
    config_path = workspace_root / "config" / "teams.json"
    
    if not config_path.exists():
        return False, None
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        teams = config.get('teams', [])
        enabled_teams = [t for t in teams if t.get('enabled', True)]
        return len(enabled_teams) > 0, {'path': str(config_path), 'teams': enabled_teams}
    except Exception as e:
        return False, {'error': str(e)}


def health_check() -> Dict:
    """Perform comprehensive health check."""
    print("\n" + "=" * 60)
    print("Health Check")
    print("=" * 60 + "\n")
    
    results = {
        'dependencies': False,
        'teams_configured': False,
        'teams_valid': [],
        'issues': []
    }
    
    # Check dependencies
    print("📦 Checking dependencies...")
    deps_ok, missing = check_dependencies()
    if deps_ok:
        print("  ✅ All dependencies installed")
        results['dependencies'] = True
    else:
        print(f"  ❌ Missing dependencies: {', '.join(missing)}")
        results['issues'].append(f"Install dependencies: pip install -r scripts/requirements.txt")
    
    print()
    
    # Check teams configuration
    print("👥 Checking team configuration...")
    teams_ok, teams_info = check_teams_config()
    if teams_ok and teams_info:
        print(f"  ✅ Found {len(teams_info['teams'])} configured team(s)")
        results['teams_configured'] = True
        
        # Validate each team
        try:
            from team_manager import TeamManager
            manager = TeamManager()
            
            for team in teams_info['teams']:
                team_id = team.get('id')
                team_name = team.get('name', team_id)
                
                # Check Linear API key
                linear_key = manager.get_linear_api_key(team_id)
                if linear_key:
                    try:
                        from linear_client import LinearClient
                        client = LinearClient(api_key=linear_key)
                        # Test connection
                        query = "query { viewer { name } }"
                        response = client._make_request(query)
                        if 'viewer' in response:
                            print(f"    ✅ {team_name}: Linear API connected")
                            results['teams_valid'].append({
                                'id': team_id,
                                'name': team_name,
                                'linear': True,
                                'google': bool(manager.get_google_config(team_id)),
                                'activecampaign': bool(manager.get_activecampaign_config(team_id))
                            })
                        else:
                            print(f"    ⚠️  {team_name}: Linear API key invalid")
                            results['issues'].append(f"{team_name}: Linear API key not working")
                    except Exception as e:
                        print(f"    ⚠️  {team_name}: Linear API error - {str(e)[:50]}")
                        results['issues'].append(f"{team_name}: Linear API connection failed")
                else:
                    print(f"    ⚠️  {team_name}: No Linear API key")
                    results['issues'].append(f"{team_name}: Missing Linear API key")
        except Exception as e:
            print(f"  ⚠️  Could not validate teams: {e}")
    else:
        print("  ❌ No teams configured")
        results['issues'].append("Run: python scripts/setup.py to configure your first team")
    
    print()
    print("=" * 60)
    
    if not results['issues']:
        print("✅ All checks passed! System is ready to use.")
        return results
    else:
        print("⚠️  Some issues found:")
        for issue in results['issues']:
            print(f"  - {issue}")
        return results


def status_dashboard():
    """Show status dashboard with overview of system."""
    print("\n" + "=" * 60)
    print("System Status Dashboard")
    print("=" * 60 + "\n")
    
    # Check dependencies
    deps_ok, missing = check_dependencies()
    status_icon = "✅" if deps_ok else "❌"
    print(f"{status_icon} Dependencies: {'Installed' if deps_ok else f'Missing ({len(missing)} packages)'}")
    
    # Check teams
    teams_ok, teams_info = check_teams_config()
    if teams_ok and teams_info:
        print(f"✅ Teams: {len(teams_info['teams'])} configured")
        
        try:
            from team_manager import TeamManager
            from task_analyzer import TaskAnalyzer
            
            manager = TeamManager()
            analyzer = TaskAnalyzer(manager)
            
            print("\n📊 Team Overview:")
            print("-" * 60)
            
            for team in teams_info['teams']:
                team_id = team.get('id')
                team_name = team.get('name', team_id)
                
                # Quick analysis
                try:
                    analysis = analyzer.analyze_team_tasks(team_id)
                    if 'error' not in analysis:
                        total = analysis.get('total_tasks', 0)
                        agent_suitable = len(analysis.get('categorized', {}).get('agent_suitable', []))
                        print(f"\n  {team_name} ({team_id})")
                        print(f"    Total open tasks: {total}")
                        print(f"    Agent-suitable: {agent_suitable}")
                    else:
                        print(f"\n  {team_name} ({team_id})")
                        print(f"    ⚠️  {analysis.get('error', 'Unknown error')}")
                except Exception as e:
                    print(f"\n  {team_name} ({team_id})")
                    print(f"    ⚠️  Could not analyze: {str(e)[:50]}")
        except Exception as e:
            print(f"\n⚠️  Could not load team details: {e}")
    else:
        print("❌ Teams: None configured")
        print("\n  Run: python scripts/setup.py")
    
    print("\n" + "=" * 60)


def interactive_setup():
    """Interactive first-time setup."""
    print("\n" + "=" * 60)
    print("Linear Agent Tasks - First Time Setup")
    print("=" * 60 + "\n")
    
    # Check dependencies
    print("Step 1: Checking dependencies...")
    deps_ok, missing = check_dependencies()
    if not deps_ok:
        print(f"  Missing: {', '.join(missing)}")
        install = input("\n  Install dependencies now? (Y/n): ").strip().lower()
        if install != 'n':
            if not install_dependencies():
                print("\n❌ Setup failed. Please install dependencies manually:")
                print("   pip install -r scripts/requirements.txt")
                return False
        else:
            print("\n⚠️  Please install dependencies before continuing:")
            print("   pip install -r scripts/requirements.txt")
            return False
    else:
        print("  ✅ All dependencies installed")
    
    print("\nStep 2: Setting up your first team...")
    print("  (This will run the team setup wizard)\n")
    
    try:
        from setup_team import setup_team
        setup_team()
    except Exception as e:
        print(f"\n❌ Team setup failed: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("Setup Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Verify setup: python scripts/setup.py --check")
    print("  2. List teams: python scripts/agent_workflow.py --list-teams")
    print("  3. Analyze tasks: python scripts/agent_workflow.py --analyze-all")
    print("  4. Work on tasks: python scripts/agent_workflow.py --team YOUR_TEAM --work")
    print("\nSee README.md for more information.")
    
    return True


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Unified setup and health check',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive first-time setup
  python scripts/setup.py

  # Health check
  python scripts/setup.py --check

  # Status dashboard
  python scripts/setup.py --status
        """
    )
    
    parser.add_argument('--check', action='store_true',
                       help='Run health check')
    parser.add_argument('--status', action='store_true',
                       help='Show status dashboard')
    
    args = parser.parse_args()
    
    if args.check:
        health_check()
    elif args.status:
        status_dashboard()
    else:
        interactive_setup()


if __name__ == '__main__':
    main()
