#!/usr/bin/env python3
"""
Agent Workflow - Multi-team task management and execution.

This script provides commands for working with tasks across multiple teams and projects.

Usage:
    # Analyze all teams and get summaries
    python agent_workflow.py --analyze-all

    # Work on open tasks for a specific team
    python agent_workflow.py --team trade-ideas --work

    # Analyze tasks for a team
    python agent_workflow.py --team trade-ideas --analyze

    # Work on tasks in a specific project
    python agent_workflow.py --team trade-ideas --project PROJECT_ID --work

    # List available teams
    python agent_workflow.py --list-teams
"""

import os
import sys
import argparse
import json
from typing import List, Dict, Optional
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(__file__))

from team_manager import TeamManager
from task_analyzer import TaskAnalyzer
from linear_client import LinearClient
from execute_tasks import TaskExecutor
from cloud_executor import CloudExecutor


class AgentWorkflow:
    """Main workflow handler for multi-team agent operations."""
    
    def __init__(self):
        """Initialize workflow with team manager."""
        self.team_manager = TeamManager()
        self.analyzer = TaskAnalyzer(self.team_manager)
        self.cloud_executor = CloudExecutor(self.team_manager)
    
    def list_teams(self):
        """List all configured teams."""
        teams = self.team_manager.list_teams()
        
        if not teams:
            print("No teams configured.")
            print("\nTo add a team, run: python scripts/setup_team.py")
            return
        
        print("\n" + "=" * 60)
        print("Configured Teams")
        print("=" * 60 + "\n")
        
        for team in teams:
            status = "✅ Enabled" if team.get('enabled', True) else "❌ Disabled"
            print(f"  {team['id']}: {team.get('name', 'Unnamed')} [{status}]")
            if team.get('notes'):
                print(f"    Notes: {team['notes']}")
            print()
    
    def analyze_all_teams(self):
        """Analyze all teams and provide summaries."""
        print("\nAnalyzing all teams...\n")
        
        results = self.analyzer.analyze_all_teams()
        summary = self.analyzer.generate_summary(results)
        
        print(summary)
        
        # Also save detailed results to file
        output_file = Path(__file__).parent.parent / "analysis_results.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n📄 Detailed results saved to: {output_file}")
    
    def analyze_team(self, team_id: str, project_id: Optional[str] = None):
        """Analyze tasks for a specific team (optionally filtered by project)."""
        print(f"\nAnalyzing tasks for team: {team_id}")
        if project_id:
            print(f"  Project filter: {project_id}")
        print()
        
        analysis = self.analyzer.analyze_team_tasks(team_id, project_id)
        
        if 'error' in analysis:
            print(f"❌ Error: {analysis['error']}\n")
            if 'next_steps' in analysis:
                print("Next steps:")
                for step in analysis['next_steps']:
                    print(f"  - {step}")
            return
        
        summary = self.analyzer.generate_summary(analysis)
        print(summary)
        
        # Show detailed task list
        categorized = analysis.get('categorized', {})
        agent_suitable = categorized.get('agent_suitable', [])
        
        if agent_suitable:
            print("\n🤖 Agent-Suitable Tasks (Detailed):")
            for task in agent_suitable:
                print(f"\n  {task['identifier']}: {task['title']}")
                print(f"    Status: {task.get('state', {}).get('name', 'Unknown')}")
                print(f"    Priority: {self._format_priority(task.get('priority', 0))}")
                desc = task.get('description', '')[:200]
                if desc:
                    print(f"    Description: {desc}...")
        
        return analysis
    
    def work_on_team(self, team_id: str, project_id: Optional[str] = None, 
                     limit: Optional[int] = None, execution_mode: str = "local"):
        """
        Work on open tasks for a team.
        
        Args:
            team_id: Team identifier
            project_id: Optional project filter
            limit: Maximum number of tasks to work on
            execution_mode: 'local' or 'cloud' - where to execute tasks
        """
        print(f"\n{'='*60}")
        print(f"Working on tasks for team: {team_id}")
        if project_id:
            print(f"  Project filter: {project_id}")
        print(f"{'='*60}\n")
        
        # First, analyze to find agent-suitable tasks
        analysis = self.analyzer.analyze_team_tasks(team_id, project_id)
        
        if 'error' in analysis:
            print(f"❌ Error: {analysis['error']}")
            return
        
        categorized = analysis.get('categorized', {})
        agent_suitable = categorized.get('agent_suitable', [])
        
        if not agent_suitable:
            print("No agent-suitable tasks found.\n")
            print("Tasks may need:")
            print("  - More detailed descriptions (50+ characters)")
            print("  - Clear acceptance criteria")
            print("  - Automation keywords (create, build, document, etc.)")
            print("  - Not assigned to someone else")
            print("\nNext steps:")
            print("  1. Try a different team: --team OTHER_TEAM")
            print("  2. Try a specific project: --project PROJECT_ID")
            print("  3. Add more detail to tasks in Linear")
            return
        
        # Limit number of tasks if specified
        tasks_to_work = agent_suitable[:limit] if limit else agent_suitable
        
        print(f"Found {len(agent_suitable)} agent-suitable tasks")
        if limit:
            print(f"Working on first {len(tasks_to_work)} tasks")
        print(f"Execution mode: {execution_mode}\n")
        
        # Handle cloud execution
        if execution_mode == "cloud":
            return self._work_on_team_cloud(team_id, tasks_to_work)
        
        # Local execution
        # Initialize executor with team-specific credentials
        team_config = self.team_manager.get_team(team_id)
        if not team_config:
            print(f"❌ Team '{team_id}' not found\n")
            print("Next steps:")
            print("  1. List teams: python scripts/agent_workflow.py --list-teams")
            print("  2. Add team: python scripts/setup_team.py")
            print("  3. Check team ID spelling (case-sensitive)")
            return
        
        # Set environment variables for this team's credentials
        # This allows existing TaskExecutor to work with team credentials
        os.environ['LINEAR_API_KEY'] = self.team_manager.get_linear_api_key(team_id)
        
        google_config = self.team_manager.get_google_config(team_id)
        if google_config:
            if 'credentials_path' in google_config:
                os.environ['GOOGLE_CREDENTIALS_PATH'] = google_config['credentials_path']
            if 'drive_folder_id' in google_config:
                os.environ['GOOGLE_DRIVE_FOLDER_ID'] = google_config['drive_folder_id']
            # Set Google Cloud project ID if configured
            if 'cloud_project_id' in google_config:
                os.environ['GOOGLE_CLOUD_PROJECT_ID'] = google_config['cloud_project_id']
            # If using shared project, check for shared project ID
            elif google_config.get('use_shared_project', False):
                # Could set a default shared project ID here
                # For now, leave it to use default from credentials
                pass
        
        ac_config = self.team_manager.get_activecampaign_config(team_id)
        if ac_config:
            if 'api_url' in ac_config:
                os.environ['ACTIVE_CAMPAIGN_API_URL'] = ac_config['api_url']
            if 'api_key' in ac_config:
                os.environ['ACTIVE_CAMPAIGN_API_KEY'] = ac_config['api_key']
        
        # Initialize executor
        executor = TaskExecutor(initialize_clients=True)
        
        if not executor.clients_initialized:
            print("⚠️  Warning: Could not initialize API clients")
            print("   Some tasks may not be executable\n")
            print("Next steps:")
            print("  1. Run health check: python scripts/setup.py --check")
            print("  2. Validate teams: python scripts/validate_teams.py")
            print("  3. Check credentials in config/teams.json")
            print()
        
        # Work on each task
        results = []
        for task in tasks_to_work:
            task_id = task['identifier']
            print(f"\n{'─'*60}")
            print(f"Working on: {task_id} - {task['title']}")
            print(f"{'─'*60}")
            
            try:
                # For now, we'll need to extend TaskExecutor to handle arbitrary tasks
                # For tasks that match known patterns (like TRA-*), use existing executors
                # For others, we'll need a generic task handler
                
                # Check if this is a known task pattern
                if task_id.startswith('TRA-'):
                    result = executor.execute_task(task_id)
                else:
                    # Generic task - analyze and attempt basic operations
                    result = self._handle_generic_task(executor, task)
                
                results.append({
                    'task_id': task_id,
                    'task_title': task['title'],
                    **result
                })
                
                if result.get('success'):
                    print(f"✅ {task_id} completed (marked as 'In Review')")
                else:
                    print(f"⚠️  {task_id} had issues: {result.get('error', 'Unknown error')}")
                    
            except Exception as e:
                print(f"❌ Error working on {task_id}: {e}")
                results.append({
                    'task_id': task_id,
                    'task_title': task['title'],
                    'success': False,
                    'error': str(e)
                })
        
        # Summary
        print(f"\n{'='*60}")
        print("Work Summary")
        print(f"{'='*60}\n")
        
        successful = sum(1 for r in results if r.get('success'))
        print(f"Tasks worked on: {len(results)}")
        print(f"Successful: {successful}")
        print(f"Had issues: {len(results) - successful}")
        
        return results
    
    def _handle_generic_task(self, executor: TaskExecutor, task: Dict) -> Dict:
        """
        Handle a generic task that doesn't match known patterns.
        
        This is a placeholder for future generic task handling.
        For now, we'll just add a comment indicating the task was reviewed.
        """
        task_id = task['identifier']
        description = task.get('description', '')
        
        # Try to determine what kind of task this is
        # For now, just add a comment
        try:
            comment = (
                f"🤖 Agent Review:\n\n"
                f"This task has been reviewed by the agent workflow system.\n\n"
                f"**Task Analysis:**\n"
                f"- Description length: {len(description)} characters\n"
                f"- Status: {task.get('state', {}).get('name', 'Unknown')}\n"
                f"- Priority: {self._format_priority(task.get('priority', 0))}\n\n"
                f"**Note:** This task may require manual execution or additional context.\n"
                f"Please review and provide more details if agent automation is desired."
            )
            
            executor.linear.add_comment(task_id, comment)
            
            return {
                'success': True,
                'message': 'Task reviewed and comment added',
                'action': 'commented'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _work_on_team_cloud(self, team_id: str, tasks: List[Dict]) -> List[Dict]:
        """
        Submit tasks for cloud execution.
        
        Args:
            team_id: Team identifier
            tasks: List of task dictionaries
            
        Returns:
            List of submission results
        """
        print("☁️  Submitting tasks for cloud execution...\n")
        
        task_ids = [task['identifier'] for task in tasks]
        results = []
        
        # Submit each task
        for task in tasks:
            task_id = task['identifier']
            print(f"Submitting: {task_id} - {task['title']}")
            
            try:
                submission = self.cloud_executor.submit_task(
                    team_id=team_id,
                    task_id=task_id,
                    task_data={
                        'title': task.get('title'),
                        'description': task.get('description'),
                        'state': task.get('state', {}).get('name'),
                        'priority': task.get('priority')
                    },
                    execution_mode='cloud'
                )
                results.append({
                    'task_id': task_id,
                    'task_title': task['title'],
                    **submission
                })
                
                if submission.get('success'):
                    print(f"  ✅ Submitted (queue: {submission.get('submission_file', 'N/A')})")
                else:
                    print(f"  ❌ Submission failed: {submission.get('error')}")
            except Exception as e:
                print(f"  ❌ Error submitting {task_id}: {e}")
                results.append({
                    'task_id': task_id,
                    'task_title': task['title'],
                    'success': False,
                    'error': str(e)
                })
        
        # Create cloud package for execution
        print(f"\n📦 Creating cloud execution package...")
        try:
            package_path = self.cloud_executor.create_cloud_package(team_id, task_ids)
            print(f"✅ Package created: {package_path}")
            print(f"\n📋 Next steps:")
            print(f"  1. Upload the package directory to your cloud environment")
            print(f"  2. Install dependencies: pip install -r requirements.txt")
            print(f"  3. Run: python execute_cloud.py")
            print(f"\n  Or use the queue files in .cloud-queue/pending/ for your cloud agent")
        except Exception as e:
            print(f"⚠️  Warning: Could not create package: {e}")
        
        # Summary
        print(f"\n{'='*60}")
        print("Cloud Submission Summary")
        print(f"{'='*60}\n")
        
        successful = sum(1 for r in results if r.get('success'))
        print(f"Tasks submitted: {len(results)}")
        print(f"Successful: {successful}")
        print(f"Failed: {len(results) - successful}")
        print(f"\nCheck task status with: --check-status")
        
        return results
    
    def check_cloud_status(self, task_id: Optional[str] = None):
        """
        Check status of cloud-executed tasks.
        
        Args:
            task_id: Optional specific task ID, or None for all tasks
        """
        if task_id:
            status = self.cloud_executor.get_task_status(task_id)
            if status:
                print(f"\n{'='*60}")
                print(f"Task Status: {task_id}")
                print(f"{'='*60}\n")
                print(f"Status: {status.get('status', 'unknown')}")
                print(f"Queue Status: {status.get('queue_status', 'unknown')}")
                print(f"Submitted: {status.get('submitted_at', 'unknown')}")
                if 'completed_at' in status:
                    print(f"Completed: {status['completed_at']}")
                if 'error' in status:
                    print(f"Error: {status['error']}")
            else:
                print(f"Task {task_id} not found in queue")
        else:
            pending = self.cloud_executor.list_pending_tasks()
            print(f"\n{'='*60}")
            print("Cloud Queue Status")
            print(f"{'='*60}\n")
            print(f"Pending tasks: {len(pending)}")
            if pending:
                print("\nPending:")
                for task in pending:
                    print(f"  - {task['task_id']}: {task.get('task_data', {}).get('title', 'N/A')}")
                    print(f"    Submitted: {task.get('submitted_at', 'unknown')}")
    
    def interactive_mode(self):
        """Interactive mode with guided prompts."""
        print("\n" + "=" * 60)
        print("Interactive Agent Workflow")
        print("=" * 60 + "\n")
        
        # Check if teams are configured
        teams = self.team_manager.list_teams()
        if not teams:
            print("❌ No teams configured.")
            print("\nLet's set up your first team...\n")
            try:
                from setup_team import setup_team
                setup_team()
                teams = self.team_manager.list_teams()
                if not teams:
                    print("\n❌ Setup incomplete. Please run: python scripts/setup.py")
                    return
            except Exception as e:
                print(f"\n❌ Setup failed: {e}")
                print("Please run: python scripts/setup.py")
                return
        
        while True:
            print("\n" + "=" * 60)
            print("What would you like to do?")
            print("=" * 60)
            print("\n1. List teams")
            print("2. Analyze all teams")
            print("3. Analyze specific team")
            print("4. Work on tasks (local)")
            print("5. Submit tasks for cloud execution")
            print("6. Check cloud execution status")
            print("7. Exit")
            
            choice = input("\nEnter choice (1-7): ").strip()
            
            if choice == '1':
                self.list_teams()
            
            elif choice == '2':
                self.analyze_all_teams()
            
            elif choice == '3':
                print("\nAvailable teams:")
                for i, team in enumerate(teams, 1):
                    print(f"  {i}. {team.get('name', team['id'])} ({team['id']})")
                
                team_choice = input("\nSelect team (number or ID): ").strip()
                
                # Try to match by number or ID
                selected_team = None
                try:
                    team_num = int(team_choice)
                    if 1 <= team_num <= len(teams):
                        selected_team = teams[team_num - 1]['id']
                except ValueError:
                    # Try as ID
                    for team in teams:
                        if team['id'] == team_choice:
                            selected_team = team_choice
                            break
                
                if selected_team:
                    project_id = input("Project ID (optional, press Enter to skip): ").strip() or None
                    self.analyze_team(selected_team, project_id)
                else:
                    print("❌ Invalid team selection")
            
            elif choice == '4':
                print("\nAvailable teams:")
                for i, team in enumerate(teams, 1):
                    print(f"  {i}. {team.get('name', team['id'])} ({team['id']})")
                
                team_choice = input("\nSelect team (number or ID): ").strip()
                
                selected_team = None
                try:
                    team_num = int(team_choice)
                    if 1 <= team_num <= len(teams):
                        selected_team = teams[team_num - 1]['id']
                except ValueError:
                    for team in teams:
                        if team['id'] == team_choice:
                            selected_team = team_choice
                            break
                
                if selected_team:
                    project_id = input("Project ID (optional, press Enter to skip): ").strip() or None
                    limit_str = input("Limit number of tasks (optional, press Enter for all): ").strip()
                    limit = int(limit_str) if limit_str else None
                    self.work_on_team(selected_team, project_id, limit, "local")
                else:
                    print("❌ Invalid team selection")
            
            elif choice == '5':
                print("\nAvailable teams:")
                for i, team in enumerate(teams, 1):
                    print(f"  {i}. {team.get('name', team['id'])} ({team['id']})")
                
                team_choice = input("\nSelect team (number or ID): ").strip()
                
                selected_team = None
                try:
                    team_num = int(team_choice)
                    if 1 <= team_num <= len(teams):
                        selected_team = teams[team_num - 1]['id']
                except ValueError:
                    for team in teams:
                        if team['id'] == team_choice:
                            selected_team = team_choice
                            break
                
                if selected_team:
                    project_id = input("Project ID (optional, press Enter to skip): ").strip() or None
                    limit_str = input("Limit number of tasks (optional, press Enter for all): ").strip()
                    limit = int(limit_str) if limit_str else None
                    self.work_on_team(selected_team, project_id, limit, "cloud")
                else:
                    print("❌ Invalid team selection")
            
            elif choice == '6':
                task_id = input("Task ID (optional, press Enter for all): ").strip() or None
                if task_id:
                    self.check_cloud_status(task_id)
                else:
                    self.check_cloud_status()
            
            elif choice == '7':
                print("\n👋 Goodbye!")
                break
            
            else:
                print("❌ Invalid choice. Please enter 1-7.")
    
    def _format_priority(self, priority: int) -> str:
        """Format Linear priority number to readable string."""
        priority_map = {
            0: 'Urgent',
            1: 'High',
            2: 'Normal',
            3: 'Low',
            4: 'No Priority'
        }
        return priority_map.get(priority, f'Unknown ({priority})')


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Agent Workflow - Multi-team task management',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # First time? Run setup first:
  python scripts/setup.py

  # List all configured teams
  python agent_workflow.py --list-teams

  # Analyze all teams and get summaries
  python agent_workflow.py --analyze-all

  # Analyze tasks for a specific team
  python agent_workflow.py --team trade-ideas --analyze

  # Work on open tasks for a team
  python agent_workflow.py --team trade-ideas --work

  # Work on tasks in a specific project
  python agent_workflow.py --team trade-ideas --project PROJECT_ID --work

  # Work on limited number of tasks
  python agent_workflow.py --team trade-ideas --work --limit 5

  # Submit tasks for cloud execution
  python agent_workflow.py --team trade-ideas --work --cloud

  # Check cloud execution status
  python agent_workflow.py --check-status
  python agent_workflow.py --check-status TRA-56

  # Interactive mode (guided prompts)
  python agent_workflow.py --interactive
  python agent_workflow.py -i
        """
    )
    
    parser.add_argument('--list-teams', action='store_true',
                       help='List all configured teams')
    parser.add_argument('--analyze-all', action='store_true',
                       help='Analyze all teams and provide summaries')
    parser.add_argument('--team', help='Team identifier')
    parser.add_argument('--project', help='Project ID to filter tasks')
    parser.add_argument('--analyze', action='store_true',
                       help='Analyze tasks (requires --team)')
    parser.add_argument('--work', action='store_true',
                       help='Work on agent-suitable tasks (requires --team)')
    parser.add_argument('--limit', type=int,
                       help='Limit number of tasks to work on')
    parser.add_argument('--cloud', action='store_true',
                       help='Submit tasks for cloud execution instead of local')
    parser.add_argument('--check-status', type=str, nargs='?', const='all',
                       help='Check status of cloud-executed tasks (optionally specify task ID)')
    parser.add_argument('--interactive', '-i', action='store_true',
                       help='Run in interactive mode with guided prompts')
    
    args = parser.parse_args()
    
    workflow = AgentWorkflow()
    
    if args.interactive:
        workflow.interactive_mode()
    elif args.list_teams:
        workflow.list_teams()
    elif args.analyze_all:
        workflow.analyze_all_teams()
    elif args.check_status:
        if args.check_status == 'all':
            workflow.check_cloud_status()
        else:
            workflow.check_cloud_status(args.check_status)
    elif args.team:
        if args.analyze:
            workflow.analyze_team(args.team, args.project)
        elif args.work:
            execution_mode = "cloud" if args.cloud else "local"
            workflow.work_on_team(args.team, args.project, args.limit, execution_mode)
        else:
            print("Error: --analyze or --work required when using --team\n")
            print("Examples:")
            print("  python agent_workflow.py --team trade-ideas --analyze")
            print("  python agent_workflow.py --team trade-ideas --work")
            print("  python agent_workflow.py --interactive  # Guided mode")
            parser.print_help()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
