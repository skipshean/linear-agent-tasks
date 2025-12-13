#!/usr/bin/env python3
"""
Cloud Executor for submitting tasks to cloud agents.

This module handles submission of tasks to cloud execution environments
and tracking their status.
"""

import os
import json
import time
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime
from team_manager import TeamManager
from linear_client import LinearClient


class CloudExecutor:
    """Manages cloud task execution and status tracking."""
    
    def __init__(self, team_manager: TeamManager, queue_path: Optional[str] = None):
        """
        Initialize cloud executor.
        
        Args:
            team_manager: TeamManager instance
            queue_path: Path to task queue directory (defaults to .cloud-queue/)
        """
        self.team_manager = team_manager
        workspace_root = Path(__file__).parent.parent
        
        if queue_path is None:
            queue_path = workspace_root / ".cloud-queue"
        else:
            queue_path = Path(queue_path)
        
        self.queue_path = queue_path
        self.queue_path.mkdir(exist_ok=True)
        
        # Subdirectories for different queue states
        self.pending_path = self.queue_path / "pending"
        self.running_path = self.queue_path / "running"
        self.completed_path = self.queue_path / "completed"
        self.failed_path = self.queue_path / "failed"
        
        for path in [self.pending_path, self.running_path, self.completed_path, self.failed_path]:
            path.mkdir(exist_ok=True)
    
    def submit_task(self, team_id: str, task_id: str, task_data: Dict, 
                   execution_mode: str = "cloud") -> Dict:
        """
        Submit a task for cloud execution.
        
        Args:
            team_id: Team identifier
            task_id: Linear task identifier (e.g., 'TRA-56')
            task_data: Task data dictionary
            execution_mode: 'cloud' or 'local'
            
        Returns:
            Dictionary with submission details
        """
        if execution_mode != "cloud":
            return {
                'success': False,
                'error': f'Execution mode "{execution_mode}" not supported for cloud submission'
            }
        
        # Create task submission
        submission = {
            'task_id': task_id,
            'team_id': team_id,
            'submitted_at': datetime.utcnow().isoformat(),
            'status': 'pending',
            'task_data': task_data,
            'execution_mode': execution_mode
        }
        
        # Save to pending queue
        task_file = self.pending_path / f"{task_id}_{int(time.time())}.json"
        with open(task_file, 'w') as f:
            json.dump(submission, f, indent=2)
        
        # Update Linear issue with submission comment
        try:
            api_key = self.team_manager.get_linear_api_key(team_id)
            if api_key:
                client = LinearClient(api_key=api_key)
                comment = (
                    f"☁️ **Cloud Execution Submitted**\n\n"
                    f"Task has been submitted for cloud execution.\n\n"
                    f"**Submission Details:**\n"
                    f"- Submitted: {submission['submitted_at']}\n"
                    f"- Queue File: `{task_file.name}`\n"
                    f"- Status: Pending execution\n\n"
                    f"Execution will begin shortly. Status updates will be posted here."
                )
                client.add_comment(task_id, comment)
        except Exception as e:
            print(f"Warning: Could not add Linear comment: {e}")
        
        return {
            'success': True,
            'task_id': task_id,
            'submission_file': str(task_file),
            'status': 'pending',
            'message': f'Task {task_id} submitted for cloud execution'
        }
    
    def list_pending_tasks(self) -> List[Dict]:
        """List all pending tasks in the queue."""
        tasks = []
        for task_file in self.pending_path.glob("*.json"):
            try:
                with open(task_file, 'r') as f:
                    task = json.load(f)
                    task['queue_file'] = str(task_file)
                    tasks.append(task)
            except Exception as e:
                print(f"Warning: Could not read {task_file}: {e}")
        
        return sorted(tasks, key=lambda x: x.get('submitted_at', ''))
    
    def get_task_status(self, task_id: str) -> Optional[Dict]:
        """
        Get status of a submitted task.
        
        Args:
            task_id: Task identifier
            
        Returns:
            Task status dictionary or None if not found
        """
        # Check all queue directories
        for queue_dir in [self.pending_path, self.running_path, self.completed_path, self.failed_path]:
            for task_file in queue_dir.glob(f"{task_id}_*.json"):
                try:
                    with open(task_file, 'r') as f:
                        task = json.load(f)
                        task['queue_file'] = str(task_file)
                        task['queue_status'] = queue_dir.name
                        return task
                except Exception as e:
                    print(f"Warning: Could not read {task_file}: {e}")
        
        return None
    
    def generate_cloud_script(self, team_id: str, task_ids: List[str]) -> str:
        """
        Generate a script that can be run in a cloud environment to execute tasks.
        
        Args:
            team_id: Team identifier
            task_ids: List of task IDs to execute
            
        Returns:
            Script content as string
        """
        team_config = self.team_manager.get_team(team_id)
        if not team_config:
            raise ValueError(f"Team '{team_id}' not found")
        
        script = f"""#!/usr/bin/env python3
\"\"\"
Cloud execution script for team: {team_config.get('name', team_id)}
Generated: {datetime.utcnow().isoformat()}
\"\"\"

import os
import sys
import json
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent / 'scripts'))

from team_manager import TeamManager
from execute_tasks import TaskExecutor

# Set up environment from team config
team_id = "{team_id}"
task_ids = {json.dumps(task_ids)}

# Initialize
manager = TeamManager()
team_config = manager.get_team(team_id)

if not team_config:
    print(f"Error: Team '{{team_id}}' not found")
    sys.exit(1)

# Set environment variables
os.environ['LINEAR_API_KEY'] = manager.get_linear_api_key(team_id)

google_config = manager.get_google_config(team_id)
if google_config:
    if 'credentials_path' in google_config:
        os.environ['GOOGLE_CREDENTIALS_PATH'] = google_config['credentials_path']
    if 'drive_folder_id' in google_config:
        os.environ['GOOGLE_DRIVE_FOLDER_ID'] = google_config['drive_folder_id']

ac_config = manager.get_activecampaign_config(team_id)
if ac_config:
    if 'api_url' in ac_config:
        os.environ['ACTIVE_CAMPAIGN_API_URL'] = ac_config['api_url']
    if 'api_key' in ac_config:
        os.environ['ACTIVE_CAMPAIGN_API_KEY'] = ac_config['api_key']

# Execute tasks
executor = TaskExecutor(initialize_clients=True)

if not executor.clients_initialized:
    print("Error: Could not initialize API clients")
    sys.exit(1)

results = []
for task_id in task_ids:
    print(f"\\nExecuting: {{task_id}}")
    try:
        result = executor.execute_task(task_id)
        results.append({{
            'task_id': task_id,
            **result
        }})
        if result.get('success'):
            print(f"✅ {{task_id}} completed")
        else:
            print(f"⚠️  {{task_id}} had issues: {{result.get('error', 'Unknown')}}")
    except Exception as e:
        print(f"❌ Error executing {{task_id}}: {{e}}")
        results.append({{
            'task_id': task_id,
            'success': False,
            'error': str(e)
        }})

# Save results
output_file = Path(__file__).parent / 'cloud_execution_results.json'
with open(output_file, 'w') as f:
    json.dump(results, f, indent=2, default=str)

print(f"\\nResults saved to: {{output_file}}")
"""
        return script
    
    def create_cloud_package(self, team_id: str, task_ids: List[str], 
                            output_dir: Optional[str] = None) -> str:
        """
        Create a package for cloud execution.
        
        Args:
            team_id: Team identifier
            task_ids: List of task IDs to execute
            output_dir: Output directory (defaults to .cloud-packages/)
            
        Returns:
            Path to created package directory
        """
        if output_dir is None:
            workspace_root = Path(__file__).parent.parent
            output_dir = workspace_root / ".cloud-packages"
        else:
            output_dir = Path(output_dir)
        
        output_dir.mkdir(exist_ok=True)
        
        # Create package directory
        package_name = f"{team_id}_{int(time.time())}"
        package_path = output_dir / package_name
        package_path.mkdir(exist_ok=True)
        
        # Copy necessary files
        scripts_dir = Path(__file__).parent
        workspace_root = scripts_dir.parent
        
        # Files to include
        files_to_copy = [
            'team_manager.py',
            'task_analyzer.py',
            'linear_client.py',
            'google_client.py',
            'activecampaign_client.py',
            'execute_tasks.py',
        ]
        
        for file_name in files_to_copy:
            src = scripts_dir / file_name
            if src.exists():
                import shutil
                shutil.copy2(src, package_path / file_name)
        
        # Copy config (without credentials - will be generated)
        config_dir = package_path / "config"
        config_dir.mkdir(exist_ok=True)
        
        # Create minimal team config (just for this team)
        team_config = self.team_manager.get_team(team_id)
        if team_config:
            with open(config_dir / "teams.json", 'w') as f:
                json.dump({"teams": [team_config]}, f, indent=2)
        
        # Generate execution script
        script_content = self.generate_cloud_script(team_id, task_ids)
        script_path = package_path / "execute_cloud.py"
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        # Make executable
        os.chmod(script_path, 0o755)
        
        # Create README
        readme = f"""# Cloud Execution Package

Team: {team_config.get('name', team_id) if team_config else team_id}
Tasks: {', '.join(task_ids)}
Created: {datetime.utcnow().isoformat()}

## Usage

1. Upload this directory to your cloud environment
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python execute_cloud.py`

## Requirements

- Python 3.8+
- Dependencies from scripts/requirements.txt
- Team credentials configured in config/teams.json
"""
        
        with open(package_path / "README.md", 'w') as f:
            f.write(readme)
        
        # Copy requirements.txt if it exists
        req_file = scripts_dir / "requirements.txt"
        if req_file.exists():
            import shutil
            shutil.copy2(req_file, package_path / "requirements.txt")
        
        return str(package_path)


if __name__ == '__main__':
    # Test the cloud executor
    from team_manager import TeamManager
    
    manager = TeamManager()
    executor = CloudExecutor(manager)
    
    print("Cloud Executor Test")
    print("Pending tasks:", len(executor.list_pending_tasks()))
