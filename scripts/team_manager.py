#!/usr/bin/env python3
"""
Team Manager for handling multiple Linear teams and their credentials.

This module manages team configurations, credentials, and provides access
to team-specific API clients.
"""

import os
import json
from typing import Dict, List, Optional
from pathlib import Path


class TeamManager:
    """Manages multiple teams and their configurations."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize team manager.
        
        Args:
            config_path: Path to teams.json config file. Defaults to config/teams.json
        """
        if config_path is None:
            # Default to config/teams.json in workspace root
            workspace_root = Path(__file__).parent.parent
            config_path = workspace_root / "config" / "teams.json"
        
        self.config_path = Path(config_path)
        self.teams = {}
        self._load_config()
    
    def _load_config(self):
        """Load team configurations from JSON file."""
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Team configuration file not found: {self.config_path}\n\n"
                "Next steps:\n"
                "1. Run setup: python scripts/setup.py\n"
                "   This will create config/teams.json and guide you through setup\n"
                "2. Or manually: Copy config/teams.json.template to config/teams.json\n"
                "   Then run: python scripts/setup_team.py"
            )
        
        with open(self.config_path, 'r') as f:
            config = json.load(f)
        
        for team_data in config.get('teams', []):
            team_id = team_data.get('id')
            if not team_id:
                continue
            
            # Only load enabled teams
            if team_data.get('enabled', True):
                self.teams[team_id] = team_data
    
    def get_team(self, team_id: str) -> Optional[Dict]:
        """
        Get team configuration by ID.
        
        Args:
            team_id: Team identifier
            
        Returns:
            Team configuration dict or None if not found
        """
        return self.teams.get(team_id)
    
    def list_teams(self) -> List[Dict]:
        """
        List all enabled teams.
        
        Returns:
            List of team configurations
        """
        return list(self.teams.values())
    
    def get_team_ids(self) -> List[str]:
        """Get list of all team IDs."""
        return list(self.teams.keys())
    
    def get_linear_api_key(self, team_id: str) -> Optional[str]:
        """Get Linear API key for a team."""
        team = self.get_team(team_id)
        if not team:
            return None
        return team.get('linear', {}).get('api_key')
    
    def get_google_config(self, team_id: str) -> Optional[Dict]:
        """Get Google API configuration for a team."""
        team = self.get_team(team_id)
        if not team:
            return None
        return team.get('google', {})
    
    def get_activecampaign_config(self, team_id: str) -> Optional[Dict]:
        """Get ActiveCampaign configuration for a team."""
        team = self.get_team(team_id)
        if not team:
            return None
        return team.get('activecampaign', {})
    
    def add_team(self, team_config: Dict) -> bool:
        """
        Add a new team configuration.
        
        Args:
            team_config: Team configuration dictionary
            
        Returns:
            True if successful
        """
        team_id = team_config.get('id')
        if not team_id:
            raise ValueError(
                "Team config must have an 'id' field.\n\n"
                "Next steps:\n"
                "1. Add 'id' field to team configuration\n"
                "2. Example: {\"id\": \"my-team\", \"name\": \"My Team\", ...}\n"
                "3. Or use setup script: python scripts/setup_team.py"
            )
        
        # Load current config
        with open(self.config_path, 'r') as f:
            config = json.load(f)
        
        # Check if team already exists
        teams = config.get('teams', [])
        for i, team in enumerate(teams):
            if team.get('id') == team_id:
                # Update existing team
                teams[i] = team_config
                break
        else:
            # Add new team
            teams.append(team_config)
        
        config['teams'] = teams
        
        # Write back
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        # Reload
        self._load_config()
        return True
    
    def update_team_credentials(self, team_id: str, service: str, credentials: Dict) -> bool:
        """
        Update credentials for a specific service on a team.
        
        Args:
            team_id: Team identifier
            service: Service name ('linear', 'google', 'activecampaign')
            credentials: Credentials dictionary
            
        Returns:
            True if successful
        """
        # Load current config
        with open(self.config_path, 'r') as f:
            config = json.load(f)
        
        # Find and update team
        teams = config.get('teams', [])
        for team in teams:
            if team.get('id') == team_id:
                if service not in team:
                    team[service] = {}
                team[service].update(credentials)
                break
        else:
            available = [t.get('id', 'unknown') for t in config.get('teams', [])]
            raise ValueError(
                f"Team '{team_id}' not found.\n\n"
                f"Available teams: {', '.join(available) if available else 'None'}\n\n"
                "Next steps:\n"
                "1. List teams: python scripts/agent_workflow.py --list-teams\n"
                "2. Add team: python scripts/setup_team.py\n"
                "3. Check team ID spelling (case-sensitive)"
            )
        
        # Write back
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        # Reload
        self._load_config()
        return True


if __name__ == '__main__':
    # Test the team manager
    manager = TeamManager()
    print("Available teams:")
    for team in manager.list_teams():
        print(f"  - {team['id']}: {team.get('name', 'Unnamed')}")
