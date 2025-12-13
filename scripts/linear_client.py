"""
Linear API Client for fetching task details and updating issues.

Usage:
    client = LinearClient(api_key)
    issue = client.get_issue('TRA-56')
    client.update_issue('TRA-56', status='In Review')
"""

import os
import requests
from typing import Dict, List, Optional
from datetime import datetime


class LinearClient:
    """Client for interacting with Linear API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Linear API client.
        
        Args:
            api_key: Linear API key. If None, reads from LINEAR_API_KEY env var.
        """
        self.api_key = api_key or os.getenv('LINEAR_API_KEY')
        if not self.api_key:
            raise ValueError(
                "Linear API key required.\n\n"
                "Next steps:\n"
                "1. Get your API key from: https://linear.app/settings/api\n"
                "2. Configure it in your team: python scripts/setup_team.py\n"
                "   Or set LINEAR_API_KEY environment variable"
            )
        
        self.base_url = "https://api.linear.app/graphql"
        self.headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json",
        }
        self.rate_limit_remaining = 1500  # Linear allows 1500 requests/hour
    
    def _make_request(self, query: str, variables: Optional[Dict] = None) -> Dict:
        """
        Make a GraphQL request to Linear API.
        
        Args:
            query: GraphQL query string
            variables: Query variables
            
        Returns:
            Response data
        """
        if self.rate_limit_remaining <= 0:
            raise Exception(
                "Rate limit exceeded. Wait before making more requests.\n\n"
                "Next steps:\n"
                "1. Wait 1 hour for rate limit to reset (1500 requests/hour)\n"
                "2. Use --limit to work on fewer tasks at once\n"
                "3. Consider cloud execution for large batches"
            )
        
        payload = {"query": query}
        if variables:
            payload["variables"] = variables
        
        response = requests.post(
            self.base_url,
            headers=self.headers,
            json=payload
        )
        
        self.rate_limit_remaining -= 1
        
        if response.status_code != 200:
            error_text = response.text
            try:
                error_json = response.json()
                if 'errors' in error_json:
                    raise Exception(f"Linear API errors: {error_json['errors']}")
            except:
                pass
            raise Exception(f"HTTP {response.status_code}: {error_text[:500]}")
        
        data = response.json()
        
        if 'errors' in data:
            raise Exception(f"Linear API errors: {data['errors']}")
        
        return data.get('data', {})
    
    def get_issue(self, issue_id: str) -> Dict:
        """
        Fetch issue details by ID.
        
        Args:
            issue_id: Issue identifier (e.g., 'TRA-56')
            
        Returns:
            Issue data dictionary
        """
        query = """
        query GetIssue($id: String!) {
            issue(id: $id) {
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
                labels {
                    nodes {
                        id
                        name
                    }
                }
                attachments {
                    nodes {
                        id
                        title
                        url
                    }
                }
                comments {
                    nodes {
                        id
                        body
                        createdAt
                        user {
                            name
                        }
                    }
                }
                relations {
                    nodes {
                        id
                        type
                        relatedIssue {
                            id
                            identifier
                            title
                        }
                    }
                }
                createdAt
                updatedAt
            }
        }
        """
        
        # Linear uses team key + issue number format
        # Need to find the issue by identifier
        variables = {"id": issue_id}
        data = self._make_request(query, variables)
        return data.get('issue', {})
    
    def get_issue_by_identifier(self, identifier: str) -> Dict:
        """
        Fetch issue by identifier (e.g., 'TRA-56').
        
        Args:
            identifier: Issue identifier
            
        Returns:
            Issue data dictionary
        """
        # Extract team key and issue number from identifier (e.g., 'TRA-56' -> 'TRA', '56')
        parts = identifier.split('-')
        if len(parts) != 2:
            raise ValueError(f"Invalid identifier format: {identifier}. Expected format: TEAM-NUMBER")
        
        team_key = parts[0]
        issue_number = parts[1]
        
        # First, get the team ID
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
        
        teams_data = self._make_request(teams_query)
        teams = teams_data.get('teams', {}).get('nodes', [])
        
        team_id = None
        for team in teams:
            if team.get('key') == team_key:
                team_id = team.get('id')
                break
        
        if not team_id:
            raise ValueError(
                f"Team '{team_key}' not found in Linear workspace.\n\n"
                "Next steps:\n"
                "1. Verify team key is correct (case-sensitive)\n"
                "2. Check team exists in your Linear workspace\n"
                "3. List available teams: python scripts/agent_workflow.py --list-teams"
            )
        
        # Now get issues for this team and find the one matching the identifier
        # Simplified query to avoid complexity limits - fetch basic info first
        query = """query GetTeamIssues($teamId: String!, $first: Int!) {
  team(id: $teamId) {
    issues(first: $first) {
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
        }
        createdAt
        updatedAt
      }
    }
  }
}"""
        
        variables = {
            "teamId": team_id,
            "first": 250  # Get up to 250 issues to find the one we need (Linear allows up to 250 per query)
        }
        
        data = self._make_request(query, variables)
        issues = data.get('team', {}).get('issues', {}).get('nodes', [])
        
        # Find the issue with matching identifier
        for issue in issues:
            if issue.get('identifier') == identifier:
                return issue
        
        return {}  # Not found
    
    def update_issue_status(self, issue_id: str, status_name: str) -> Dict:
        """
        Update issue status.
        
        Args:
            issue_id: Issue identifier
            status_name: Status name (e.g., 'In Review', 'In Progress', 'Done')
            
        Returns:
            Updated issue data
        """
        # First, get available states
        states_query = """
        query {
            workflowStates {
                nodes {
                    id
                    name
                    type
                }
            }
        }
        """
        
        states_data = self._make_request(states_query)
        states = states_data.get('workflowStates', {}).get('nodes', [])
        
        # Find state by name
        target_state = None
        for state in states:
            if state['name'].lower() == status_name.lower():
                target_state = state
                break
        
        if not target_state:
            available = [s['name'] for s in states]
            raise ValueError(
                f"Status '{status_name}' not found.\n\n"
                f"Available statuses: {', '.join(available)}\n\n"
                "Next steps:\n"
                "1. Check status name spelling (case-sensitive)\n"
                "2. Use one of the available statuses listed above\n"
                "3. Common statuses: 'In Review', 'In Progress', 'Done', 'Todo'"
            )
        
        # Get issue ID first
        issue = self.get_issue_by_identifier(issue_id)
        if not issue:
            raise ValueError(f"Issue {issue_id} not found")
        
        # Update issue
        update_query = """
        mutation UpdateIssue($id: String!, $stateId: String!) {
            issueUpdate(id: $id, input: { stateId: $stateId }) {
                success
                issue {
                    id
                    identifier
                    state {
                        name
                    }
                }
            }
        }
        """
        
        variables = {
            "id": issue['id'],
            "stateId": target_state['id']
        }
        
        data = self._make_request(update_query, variables)
        return data.get('issueUpdate', {}).get('issue', {})
    
    def add_comment(self, issue_id: str, comment: str) -> Dict:
        """
        Add comment to issue.
        
        Args:
            issue_id: Issue identifier
            comment: Comment text
            
        Returns:
            Created comment data
        """
        issue = self.get_issue_by_identifier(issue_id)
        if not issue:
            raise ValueError(
                f"Issue {issue_id} not found.\n\n"
                "Next steps:\n"
                "1. Verify issue ID is correct (format: TEAM-NUMBER, e.g., TRA-56)\n"
                "2. Check issue exists in Linear\n"
                "3. Verify you have access to the team/project"
            )
        
        query = """
        mutation CreateComment($issueId: String!, $body: String!) {
            commentCreate(input: { issueId: $issueId, body: $body }) {
                success
                comment {
                    id
                    body
                    createdAt
                }
            }
        }
        """
        
        variables = {
            "issueId": issue['id'],
            "body": comment
        }
        
        data = self._make_request(query, variables)
        return data.get('commentCreate', {}).get('comment', {})
    
    def get_team_issues(self, team_key: str, limit: int = 100) -> List[Dict]:
        """
        Get all issues for a team.
        
        Args:
            team_key: Team key (e.g., 'TRA')
            limit: Maximum number of issues to fetch
            
        Returns:
            List of issue dictionaries
        """
        query = """
        query GetTeamIssues($teamKey: String!, $first: Int!) {
            team(key: $teamKey) {
                issues(first: $first) {
                    nodes {
                        id
                        identifier
                        title
                        state {
                            name
                        }
                    }
                }
            }
        }
        """
        
        variables = {
            "teamKey": team_key,
            "first": limit
        }
        
        data = self._make_request(query, variables)
        team = data.get('team', {})
        issues = team.get('issues', {}).get('nodes', [])
        return issues


if __name__ == '__main__':
    # Example usage
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python linear_client.py <issue_id>")
        sys.exit(1)
    
    issue_id = sys.argv[1]
    
    try:
        client = LinearClient()
        issue = client.get_issue_by_identifier(issue_id)
        print(f"Issue: {issue.get('identifier')} - {issue.get('title')}")
        print(f"Status: {issue.get('state', {}).get('name')}")
        print(f"Description: {issue.get('description', 'No description')[:200]}...")
    except Exception as e:
        print(f"Error: {e}")
