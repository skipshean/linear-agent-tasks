"""
Linear API Client for fetching task details and updating issues.

Usage:
    client = LinearClient(api_key)
    issue = client.get_issue('TRA-56')
    client.update_issue('TRA-56', status='Done')
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
            raise ValueError("Linear API key required. Set LINEAR_API_KEY env var or pass api_key parameter.")
        
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
            raise Exception("Rate limit exceeded. Wait before making more requests.")
        
        payload = {"query": query}
        if variables:
            payload["variables"] = variables
        
        response = requests.post(
            self.base_url,
            headers=self.headers,
            json=payload
        )
        
        self.rate_limit_remaining -= 1
        
        response.raise_for_status()
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
        query = """
        query GetIssueByIdentifier($identifier: String!) {
            issue(identifier: $identifier) {
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
        
        variables = {"identifier": identifier}
        data = self._make_request(query, variables)
        return data.get('issue', {})
    
    def update_issue_status(self, issue_id: str, status_name: str) -> Dict:
        """
        Update issue status.
        
        Args:
            issue_id: Issue identifier
            status_name: Status name (e.g., 'Done', 'In Progress')
            
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
            raise ValueError(f"Status '{status_name}' not found. Available: {[s['name'] for s in states]}")
        
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
            raise ValueError(f"Issue {issue_id} not found")
        
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
