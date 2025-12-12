"""
ActiveCampaign API Client.

Usage:
    client = ActiveCampaignClient(api_url, api_key)
    tags = client.list_tags()
    client.create_tag('My Tag')
"""

import os
import requests
from typing import Dict, List, Optional
import time


class ActiveCampaignClient:
    """Client for ActiveCampaign API."""
    
    def __init__(self, api_url: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initialize ActiveCampaign API client.
        
        Args:
            api_url: ActiveCampaign API URL (e.g., 'https://{account}.api-us1.com')
            api_key: ActiveCampaign API key
        """
        self.api_url = (api_url or os.getenv('ACTIVE_CAMPAIGN_API_URL')).rstrip('/')
        self.api_key = api_key or os.getenv('ACTIVE_CAMPAIGN_API_KEY')
        
        if not self.api_url or not self.api_key:
            raise ValueError(
                "ActiveCampaign API URL and key required. "
                "Set ACTIVE_CAMPAIGN_API_URL and ACTIVE_CAMPAIGN_API_KEY env vars."
            )
        
        self.headers = {
            'Api-Token': self.api_key,
            'Content-Type': 'application/json'
        }
        self.rate_limit_delay = 0.1  # Small delay to respect rate limits
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """
        Make API request.
        
        Args:
            method: HTTP method ('GET', 'POST', 'PUT', 'DELETE')
            endpoint: API endpoint (e.g., '/api/3/tags')
            data: Request body data
            
        Returns:
            Response data
        """
        url = f"{self.api_url}{endpoint}"
        
        response = requests.request(
            method=method,
            url=url,
            headers=self.headers,
            json=data
        )
        
        time.sleep(self.rate_limit_delay)  # Rate limiting
        
        response.raise_for_status()
        return response.json()
    
    def list_tags(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """
        List all tags.
        
        Args:
            limit: Maximum number of tags to return
            offset: Offset for pagination
            
        Returns:
            List of tag dictionaries
        """
        endpoint = f'/api/3/tags?limit={limit}&offset={offset}'
        response = self._make_request('GET', endpoint)
        return response.get('tags', [])
    
    def get_tag_by_name(self, tag_name: str) -> Optional[Dict]:
        """
        Get tag by name (case-insensitive).
        
        Args:
            tag_name: Tag name to search for
            
        Returns:
            Tag dictionary if found, None otherwise
        """
        tags = self.list_tags(limit=1000)  # Get all tags
        
        for tag in tags:
            if tag.get('tag', '').lower() == tag_name.lower():
                return tag
        
        return None
    
    def create_tag(self, tag_name: str, tag_type: str = 'contact', description: str = '') -> Dict:
        """
        Create a new tag.
        
        Args:
            tag_name: Tag name
            tag_type: Tag type ('contact', 'template', 'form', 'deal', 'account', 'site')
            description: Optional tag description
            
        Returns:
            Created tag dictionary
        """
        # Check if tag already exists
        existing = self.get_tag_by_name(tag_name)
        if existing:
            return existing  # Return existing tag instead of creating duplicate
        
        endpoint = '/api/3/tags'
        data = {
            'tag': {
                'tag': tag_name,
                'tagType': tag_type,
                'description': description
            }
        }
        
        response = self._make_request('POST', endpoint, data)
        return response.get('tag', {})
    
    def create_tags_batch(self, tag_names: List[str], tag_type: str = 'contact') -> Dict:
        """
        Create multiple tags in batch.
        
        Args:
            tag_names: List of tag names to create
            tag_type: Tag type for all tags
            
        Returns:
            Dictionary with created and skipped tags
        """
        created = []
        skipped = []
        
        for tag_name in tag_names:
            existing = self.get_tag_by_name(tag_name)
            if existing:
                skipped.append({'name': tag_name, 'reason': 'Already exists'})
            else:
                try:
                    tag = self.create_tag(tag_name, tag_type)
                    created.append(tag)
                except Exception as e:
                    skipped.append({'name': tag_name, 'reason': str(e)})
        
        return {
            'created': created,
            'skipped': skipped,
            'created_count': len(created),
            'skipped_count': len(skipped)
        }
    
    def list_automations(self) -> List[Dict]:
        """
        List all automations.
        
        Returns:
            List of automation dictionaries
        """
        endpoint = '/api/3/automations'
        response = self._make_request('GET', endpoint)
        return response.get('automations', [])
    
    def get_automation(self, automation_id: int) -> Dict:
        """
        Get automation details.
        
        Args:
            automation_id: Automation ID
            
        Returns:
            Automation dictionary
        """
        endpoint = f'/api/3/automations/{automation_id}'
        response = self._make_request('GET', endpoint)
        return response.get('automation', {})
    
    def create_goal(self, automation_id: int, goal_name: str, goal_type: str = 'contact') -> Dict:
        """
        Create a goal in automation.
        
        Note: ActiveCampaign API v3 does not support direct goal creation via POST.
        Goals must be created through the UI or by adding a goal block to an automation.
        This method documents the goal requirement and returns instructions.
        
        Args:
            automation_id: Automation ID
            goal_name: Goal name
            goal_type: Goal type ('contact', 'deal', 'account')
            
        Returns:
            Dictionary with goal information and manual steps required
        """
        # Get automation details
        automation = self.get_automation(automation_id)
        automation_name = automation.get('name', f'Automation {automation_id}')
        
        # Get automation blocks to find where goal should be added
        blocks_endpoint = f'/api/3/automations/{automation_id}/blocks'
        blocks_response = self._make_request('GET', blocks_endpoint)
        blocks = blocks_response.get('automationBlocks', [])
        
        # Return information about what needs to be done manually
        return {
            'goal_name': goal_name,
            'automation_id': automation_id,
            'automation_name': automation_name,
            'status': 'manual_required',
            'message': 'ActiveCampaign API does not support direct goal creation. Goal must be added manually in the UI.',
            'instructions': [
                f'1. Go to ActiveCampaign → Automations → {automation_name}',
                f'2. Add a "Goal" block to the automation',
                f'3. Name the goal: "{goal_name}"',
                f'4. Configure the goal trigger conditions',
                f'5. Save the automation'
            ],
            'automation_url': f'https://{self.api_url.split("//")[1].split("/")[0]}/app/automations/{automation_id}',
            'blocks_available': len(blocks) > 0
        }
    
    def add_email_to_automation(self, automation_id: int, email_data: Dict) -> Dict:
        """
        Add email step to automation.
        
        Args:
            automation_id: Automation ID
            email_data: Email configuration (subject, body, etc.)
            
        Returns:
            Created email step dictionary
        """
        # Note: ActiveCampaign API structure for adding emails to automations
        # may vary. This is a simplified version.
        endpoint = f'/api/3/automations/{automation_id}/actions'
        data = {
            'action': {
                'type': 'email',
                **email_data
            }
        }
        
        response = self._make_request('POST', endpoint, data)
        return response.get('action', {})
    
    def add_link_tag_trigger(self, link_url: str, tag_name: str) -> Dict:
        """
        Add tag trigger to link click.
        
        Args:
            link_url: URL to track
            tag_name: Tag to apply when link is clicked
            
        Returns:
            Created trigger dictionary
        """
        # Get tag ID
        tag = self.get_tag_by_name(tag_name)
        if not tag:
            raise ValueError(f"Tag '{tag_name}' not found. Create it first.")
        
        # Note: ActiveCampaign link tracking setup may require
        # configuring site tracking or using automation triggers
        # This is a simplified version - actual implementation
        # may need to use webhooks or automation conditions
        
        endpoint = '/api/3/contactAutomations'
        # This would need to be configured based on actual AC API structure
        # for link tracking and tag application
        
        return {'status': 'Link tag trigger configuration needed'}


if __name__ == '__main__':
    # Example usage
    print("ActiveCampaign API client initialized")
    print("Use this client to interact with ActiveCampaign")
