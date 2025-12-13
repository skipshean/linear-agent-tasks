#!/usr/bin/env python3
"""
Interactive script for setting up a new team configuration.

Usage:
    python setup_team.py
"""

import json
import os
from pathlib import Path
from team_manager import TeamManager


def setup_team():
    """Interactive team setup."""
    workspace_root = Path(__file__).parent.parent
    config_path = workspace_root / "config" / "teams.json"
    
    # Create config directory if it doesn't exist
    config_path.parent.mkdir(exist_ok=True)
    
    # Create teams.json from template if it doesn't exist
    if not config_path.exists():
        template_path = workspace_root / "config" / "teams.json.template"
        if template_path.exists():
            with open(template_path, 'r') as f:
                template = json.load(f)
            # Remove placeholder team
            template['teams'] = []
            with open(config_path, 'w') as f:
                json.dump(template, f, indent=2)
        else:
            # Create empty config
            with open(config_path, 'w') as f:
                json.dump({"teams": []}, f, indent=2)
    
    manager = TeamManager(config_path=str(config_path))
    
    print("=" * 60)
    print("Team Setup")
    print("=" * 60)
    print()
    
    # Get team details
    team_id = input("Team ID (e.g., 'trade-ideas', 'client-name'): ").strip()
    if not team_id:
        print("❌ Team ID is required")
        return
    
    # Check if team already exists
    if manager.get_team(team_id):
        overwrite = input(f"Team '{team_id}' already exists. Overwrite? (y/N): ").strip().lower()
        if overwrite != 'y':
            print("Cancelled.")
            return
    
    team_name = input(f"Team Name (default: {team_id.title()}): ").strip() or team_id.title()
    
    print("\n--- Linear API Configuration ---")
    print("📖 Need help? Get your API key from: https://linear.app/settings/api")
    print("   Click 'Create API Key' and copy it (you'll only see it once!)")
    linear_api_key = input("\nLinear API Key: ").strip()
    if not linear_api_key:
        print("⚠️  Warning: Linear API key is required for task management")
        print("   You can add it later by running this script again")
    
    print("\n--- Google API Configuration (Optional) ---")
    print("📖 Need help? See: https://console.cloud.google.com/")
    print("   1. Create/select a project")
    print("   2. Enable: Docs API, Sheets API, Drive API")
    print("   3. Create credentials (Service Account or OAuth)")
    print("   4. Download JSON file")
    use_google = input("\nConfigure Google APIs? (y/N): ").strip().lower() == 'y'
    google_config = {}
    if use_google:
        print("\n   Enter the path to your credentials JSON file")
        creds_path = input("Google Credentials JSON Path (or press Enter to skip): ").strip()
        if creds_path:
            google_config['credentials_path'] = creds_path
        folder_id = input("Google Drive Folder ID (or press Enter to skip): ").strip()
        if folder_id:
            google_config['drive_folder_id'] = folder_id
        
        print("\n--- Google Cloud Project Configuration ---")
        use_shared = input("Use shared Google Cloud project for all teams? (Y/n): ").strip().lower()
        use_shared_project = use_shared != 'n'
        
        if use_shared_project:
            shared_project = input("Shared Google Cloud Project ID (or press Enter to use default): ").strip()
            if shared_project:
                google_config['cloud_project_id'] = shared_project
            google_config['use_shared_project'] = True
        else:
            project_id = input("Team-specific Google Cloud Project ID (or press Enter to skip): ").strip()
            if project_id:
                google_config['cloud_project_id'] = project_id
            google_config['use_shared_project'] = False
    
    print("\n--- ActiveCampaign Configuration (Optional) ---")
    print("📖 Need help? Get credentials from: ActiveCampaign Settings → Developer")
    print("   You'll need: API URL and API Key")
    use_ac = input("\nConfigure ActiveCampaign API? (y/N): ").strip().lower() == 'y'
    ac_config = {}
    if use_ac:
        print("\n   Example API URL: https://your-account.api-us1.com")
        api_url = input("ActiveCampaign API URL: ").strip()
        if api_url:
            ac_config['api_url'] = api_url
        api_key = input("ActiveCampaign API Key: ").strip()
        if api_key:
            ac_config['api_key'] = api_key
    
    notes = input("\nNotes (optional): ").strip()
    
    # Build team config
    team_config = {
        "id": team_id,
        "name": team_name,
        "linear": {
            "api_key": linear_api_key
        },
        "enabled": True
    }
    
    if google_config:
        team_config['google'] = google_config
    
    if ac_config:
        team_config['activecampaign'] = ac_config
    
    if notes:
        team_config['notes'] = notes
    
    # Save
    try:
        manager.add_team(team_config)
        print(f"\n✅ Team '{team_name}' ({team_id}) configured successfully!")
        print(f"\nConfiguration saved to: {config_path}")
    except Exception as e:
        print(f"\n❌ Error saving team: {e}")


if __name__ == '__main__':
    setup_team()
