#!/usr/bin/env python3
"""
Task Analyzer for evaluating tasks across teams and projects.

This module provides functionality to analyze Linear tasks and determine
what can be automated or worked on by an agent.
"""

from typing import Dict, List, Optional
from linear_client import LinearClient
from team_manager import TeamManager


class TaskAnalyzer:
    """Analyzes tasks across teams and projects."""
    
    def __init__(self, team_manager: TeamManager):
        """
        Initialize task analyzer.
        
        Args:
            team_manager: TeamManager instance
        """
        self.team_manager = team_manager
        self._linear_clients = {}  # Cache clients per team
    
    def _get_linear_client(self, team_id: str) -> Optional[LinearClient]:
        """Get or create Linear client for a team."""
        if team_id in self._linear_clients:
            return self._linear_clients[team_id]
        
        api_key = self.team_manager.get_linear_api_key(team_id)
        if not api_key:
            return None
        
        client = LinearClient(api_key=api_key)
        self._linear_clients[team_id] = client
        return client
    
    def analyze_team_tasks(self, team_id: str, project_id: Optional[str] = None) -> Dict:
        """
        Analyze open tasks for a team (optionally filtered by project).
        
        Args:
            team_id: Team identifier
            project_id: Optional project identifier to filter tasks
            
        Returns:
            Dictionary with analysis results
        """
        client = self._get_linear_client(team_id)
        if not client:
            return {
                'error': f'No Linear API key configured for team: {team_id}',
                'team_id': team_id,
                'next_steps': [
                    'Run: python scripts/setup_team.py',
                    'Select the team and add Linear API key',
                    'Get API key from: https://linear.app/settings/api'
                ]
            }
        
        team_config = self.team_manager.get_team(team_id)
        team_name = team_config.get('name', team_id) if team_config else team_id
        
        # Get team key from Linear
        # First, get all teams to find the one matching our team_id
        teams_query = """
        query {
            teams {
                nodes {
                    id
                    key
                    name
                }
            }
        }
        """
        
        try:
            teams_data = client._make_request(teams_query)
            teams = teams_data.get('teams', {}).get('nodes', [])
            
            # Try to find team by name or use first team
            team_key = None
            for team in teams:
                if team.get('name', '').lower() == team_name.lower():
                    team_key = team.get('key')
                    break
            
            if not team_key and teams:
                # Use first team as fallback
                team_key = teams[0].get('key')
            
            if not team_key:
                return {
                    'error': f'Could not find team in Linear workspace',
                    'team_id': team_id,
                    'next_steps': [
                        'Verify team name matches Linear workspace',
                        'Check team exists in your Linear account',
                        'List teams: python scripts/agent_workflow.py --list-teams'
                    ]
                }
            
            # Get open issues for this team
            issues_query = """
            query GetTeamIssues($teamKey: String!, $first: Int!) {
                team(key: $teamKey) {
                    issues(first: $first, filter: { state: { type: { neq: completed } } }) {
                        nodes {
                            id
                            identifier
                            title
                            description
                            state {
                                id
                                name
                                type
                            }
                            priority
                            assignee {
                                id
                                name
                                email
                            }
                            project {
                                id
                                name
                            }
                            labels {
                                nodes {
                                    id
                                    name
                                }
                            }
                            createdAt
                            updatedAt
                        }
                    }
                }
            }
            """
            
            variables = {
                "teamKey": team_key,
                "first": 250  # Linear allows up to 250 per query
            }
            
            data = client._make_request(issues_query, variables)
            team_data = data.get('team', {})
            all_issues = team_data.get('issues', {}).get('nodes', [])
            
            # Filter by project if specified
            if project_id:
                issues = [issue for issue in all_issues 
                         if issue.get('project', {}).get('id') == project_id]
                project_name = next(
                    (issue.get('project', {}).get('name') for issue in all_issues 
                     if issue.get('project', {}).get('id') == project_id),
                    project_id
                )
            else:
                issues = all_issues
                project_name = None
            
            # Categorize tasks
            categorized = self._categorize_tasks(issues)
            
            return {
                'team_id': team_id,
                'team_name': team_name,
                'team_key': team_key,
                'project_id': project_id,
                'project_name': project_name,
                'total_tasks': len(issues),
                'categorized': categorized,
                'tasks': issues
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'team_id': team_id
            }
    
    def _categorize_tasks(self, issues: List[Dict]) -> Dict:
        """
        Categorize tasks by agent-suitability and other criteria.
        
        Args:
            issues: List of issue dictionaries
            
        Returns:
            Dictionary with categorized tasks
        """
        categories = {
            'agent_suitable': [],
            'needs_review': [],
            'blocked': [],
            'low_priority': [],
            'other': []
        }
        
        for issue in issues:
            state = issue.get('state', {})
            state_type = state.get('type', '').lower()
            priority = issue.get('priority', 0)
            assignee = issue.get('assignee')
            
            # Check if blocked
            if state_type == 'canceled' or state.get('name', '').lower() == 'blocked':
                categories['blocked'].append(issue)
            # Check if low priority
            elif priority >= 3:  # Linear priority: 0=urgent, 1=high, 2=normal, 3=low, 4=no priority
                categories['low_priority'].append(issue)
            # Check if agent-suitable (has clear description, not assigned, etc.)
            elif self._is_agent_suitable(issue):
                categories['agent_suitable'].append(issue)
            # Needs human review
            elif assignee or not issue.get('description'):
                categories['needs_review'].append(issue)
            else:
                categories['other'].append(issue)
        
        return categories
    
    def _is_agent_suitable(self, issue: Dict) -> bool:
        """
        Determine if a task is suitable for agent automation.
        
        Args:
            issue: Issue dictionary
            
        Returns:
            True if agent-suitable
        """
        description = issue.get('description', '')
        title = issue.get('title', '')
        
        # Must have description
        if not description or len(description) < 50:
            return False
        
        # Check for keywords that indicate automation potential
        automation_keywords = [
            'create', 'document', 'build', 'set up', 'configure',
            'add', 'implement', 'generate', 'export', 'import',
            'format', 'organize', 'update', 'sync'
        ]
        
        text = (title + ' ' + description).lower()
        has_keyword = any(keyword in text for keyword in automation_keywords)
        
        # Check for clear acceptance criteria
        has_criteria = any(marker in description.lower() 
                          for marker in ['acceptance', 'criteria', 'requirements', 'steps'])
        
        return has_keyword or has_criteria
    
    def analyze_all_teams(self) -> Dict:
        """
        Analyze tasks across all teams and provide summaries.
        
        Returns:
            Dictionary with analysis for each team
        """
        results = {}
        
        for team_id in self.team_manager.get_team_ids():
            team_config = self.team_manager.get_team(team_id)
            team_name = team_config.get('name', team_id) if team_config else team_id
            
            print(f"Analyzing team: {team_name} ({team_id})...")
            
            analysis = self.analyze_team_tasks(team_id)
            results[team_id] = analysis
        
        return results
    
    def generate_summary(self, analysis: Dict) -> str:
        """
        Generate a human-readable summary from analysis results.
        
        Args:
            analysis: Analysis dictionary from analyze_team_tasks or analyze_all_teams
            
        Returns:
            Formatted summary string
        """
        if 'error' in analysis:
            return f"❌ Error: {analysis['error']}"
        
        # Single team analysis
        if 'team_id' in analysis and 'team_name' in analysis:
            team_name = analysis['team_name']
            total = analysis['total_tasks']
            categorized = analysis['categorized']
            
            summary = f"\n{'='*60}\n"
            summary += f"Team: {team_name}\n"
            if analysis.get('project_name'):
                summary += f"Project: {analysis['project_name']}\n"
            summary += f"{'='*60}\n\n"
            summary += f"Total Open Tasks: {total}\n\n"
            
            summary += "📊 Task Breakdown:\n"
            summary += f"  🤖 Agent-Suitable: {len(categorized['agent_suitable'])}\n"
            summary += f"  👤 Needs Review: {len(categorized['needs_review'])}\n"
            summary += f"  🚫 Blocked: {len(categorized['blocked'])}\n"
            summary += f"  ⬇️  Low Priority: {len(categorized['low_priority'])}\n"
            summary += f"  📋 Other: {len(categorized['other'])}\n\n"
            
            if categorized['agent_suitable']:
                summary += "🤖 Agent-Suitable Tasks:\n"
                for task in categorized['agent_suitable'][:10]:  # Show first 10
                    summary += f"  - {task['identifier']}: {task['title']}\n"
                if len(categorized['agent_suitable']) > 10:
                    summary += f"  ... and {len(categorized['agent_suitable']) - 10} more\n"
                summary += "\n"
            
            return summary
        
        # Multiple teams analysis
        else:
            summary = f"\n{'='*60}\n"
            summary += "Multi-Team Analysis Summary\n"
            summary += f"{'='*60}\n\n"
            
            for team_id, team_analysis in analysis.items():
                if 'error' in team_analysis:
                    summary += f"❌ {team_id}: {team_analysis['error']}\n\n"
                    continue
                
                team_name = team_analysis.get('team_name', team_id)
                total = team_analysis.get('total_tasks', 0)
                categorized = team_analysis.get('categorized', {})
                agent_suitable = len(categorized.get('agent_suitable', []))
                
                summary += f"📁 {team_name}:\n"
                summary += f"   Total Tasks: {total}\n"
                summary += f"   Agent-Suitable: {agent_suitable}\n"
                summary += f"   Needs Review: {len(categorized.get('needs_review', []))}\n"
                summary += "\n"
            
            return summary


if __name__ == '__main__':
    # Test the analyzer
    manager = TeamManager()
    analyzer = TaskAnalyzer(manager)
    
    # Analyze all teams
    results = analyzer.analyze_all_teams()
    summary = analyzer.generate_summary(results)
    print(summary)
