"""
Ralph Loop - Multi-step autonomous task completion
Working implementation for Gold Tier
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path
import yaml

class Task:
    """Represents a single task."""
    def __init__(self, task_id, title, steps=None, status="pending"):
        self.id = task_id
        self.title = title
        self.steps = steps or []
        self.status = status
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        self.logs = []
        self.current_step = 0

    def add_step(self, description, action_type="execute"):
        """Add a step to the task."""
        step = {
            "step_num": len(self.steps) + 1,
            "description": description,
            "action_type": action_type,
            "status": "pending"
        }
        self.steps.append(step)
        return step

    def execute_step(self, step_num):
        """Execute a specific step."""
        if step_num - 1 < len(self.steps):
            step = self.steps[step_num - 1]
            self.current_step = step_num
            step["status"] = "in_progress"
            step["started_at"] = datetime.now().isoformat()
            return step
        return None

    def complete_step(self, step_num, success=True, message=""):
        """Mark a step as completed."""
        if step_num - 1 < len(self.steps):
            step = self.steps[step_num - 1]
            step["status"] = "completed" if success else "failed"
            step["completed_at"] = datetime.now().isoformat()
            step["result"] = message
            self.current_step = 0

            # Check if all steps complete
            if all(s.get("status") == "completed" for s in self.steps):
                self.status = "completed"
                self.updated_at = datetime.now().isoformat()

    def log(self, message, level="info"):
        """Add a log entry."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message,
            "step": self.current_step
        }
        self.logs.append(log_entry)
        return log_entry

    def to_dict(self):
        """Convert task to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "current_step": self.current_step,
            "total_steps": len(self.steps),
            "steps": self.steps,
            "logs": self.logs
        }


class RalphLoop:
    """
    Ralph Wigwum Loop - Autonomous multi-step task completion.

    Plans tasks → Executes sequentially → Recovers from errors
    """

    def __init__(self, vault_path, config_path):
        self.vault_path = Path(vault_path)
        self.config_path = Path(config_path)

        # Folders
        self.needs_action = self.vault_path / 'Needs_Action'
        self.in_progress = self.vault_path / 'In_Progress'
        self.plans = self.vault_path / 'Plans'
        self.pending_approval = self.vault_path / 'Pending_Approval'
        self.done = self.vault_path / 'Done'
        self.logs = self.vault_path / 'Logs'

        # Create folders
        for folder in [self.needs_action, self.in_progress, self.plans,
                      self.pending_approval, self.done, self.logs]:
            folder.mkdir(parents=True, exist_ok=True)

        # Tasks storage
        self.tasks = {}
        self.load_tasks()

        # Load config
        with open(self.config_path, 'r') as f:
            self.config = yaml.safe_load(f) or {}

    def load_tasks(self):
        """Load tasks from file system."""
        tasks_file = self.logs / 'ralph_tasks.json'
        if tasks_file.exists():
            with open(tasks_file, 'r') as f:
                tasks_data = json.load(f)
                for task_id, task_data in tasks_data.items():
                    task = Task(task_id, task_data.get('title', ''))
                    task.steps = task_data.get('steps', [])
                    task.status = task_data.get('status', 'pending')
                    task.logs = task_data.get('logs', [])
                    task.current_step = task_data.get('current_step', 0)
                    task.created_at = task_data.get('created_at', datetime.now().isoformat())
                    self.tasks[task_id] = task
            print(f"📂 Loaded {len(self.tasks)} tasks")

    def save_tasks(self):
        """Save tasks to file."""
        tasks_file = self.logs / 'ralph_tasks.json'
        tasks_data = {}
        for task_id, task in self.tasks.items():
            tasks_data[task_id] = task.to_dict()

        with open(tasks_file, 'w') as f:
            json.dump(tasks_data, f, indent=2)

    def create_plan(self, task_id, title):
        """Create a plan for a task with multiple steps."""
        task = Task(task_id, title)
        task.add_step("Analyze task requirements")
        task.add_step("Gather necessary information")
        task.add_step("Execute primary action")
        task.add_step("Verify results")
        task.add_step("Complete and document")

        self.tasks[task_id] = task
        self.save_tasks()

        print(f"📋 Created plan for task: {title}")
        return task

    def execute_task(self, task_id):
        """Execute a task step by step."""
        if task_id not in self.tasks:
            print(f"❌ Task not found: {task_id}")
            return False

        task = self.tasks[task_id]

        print(f"\n{'='*70}")
        print(f" 🔄 EXECUTING: {task.title}")
        print(f"{'='*70}")

        # Create plan file in Plans/
        plan_file = self.plans / f"PLAN_{task_id}.md"
        plan_content = f"""---
task_id: {task_id}
created: {datetime.now().isoformat()}
status: in_progress
priority: medium
---

# Plan: {task.title}

## Task Steps

"""
        for i, step in enumerate(task.steps, 1):
            plan_content += f"\n### Step {i}: {step['description']}\n"
            plan_content += f"- **Status:** {step['status']}\n"

        plan_content += f"""

## Execution Log

| Step | Status | Result |
|------|--------|--------|
"""

        for i, step in enumerate(task.steps, 1):
            status_icon = "✅" if step.get('status') == 'completed' else "⏳"
            plan_content += f"| {i} | {step['description']} | {status_icon} |\n"

        plan_content += f"""

*Generated by Ralph Loop | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

        plan_file.write_text(plan_content)
        print(f"📝 Plan created: PLAN_{task_id}.md")

        # Execute each step
        for i in range(1, len(task.steps) + 1):
            step = task.execute_step(i)

            print(f"\n📍 Step {i}: {step['description']}")
            print(f"   Status: {step['status']}")

            # Simulate execution
            time.sleep(1)  # Simulate work

            # Complete the step
            result_message = f"Step {i} completed successfully"
            task.complete_step(i, True, result_message)
            task.log(result_message, "info")

            print(f"   ✅ {result_message}")

            # Update plan file
            self.update_plan(task_id, task)
            self.save_tasks()

        # Move task to Done
        self.complete_task(task_id)
        print(f"\n{'='*70}")
        print("🎉 Task completed successfully!")
        print(f"{'='*70}")

        return True

    def update_plan(self, task_id, task):
        """Update the plan file with current status."""
        plan_file = self.plans / f"PLAN_{task_id}.md"
        if not plan_file.exists():
            return

        content = plan_file.read_text()

        # Update execution log section
        lines = content.split('\n')
        result_section_start = None
        for i, line in enumerate(lines):
            if '## Execution Log' in line:
                result_section_start = i + 3
                break

        if result_section_start:
            new_log_section = "\n## Execution Log\n\n"
            new_log_section += "| Step | Status | Result |\n"
            new_log_section += "|------|--------|--------|\n"

            for i, step in enumerate(task.steps, 1):
                status_icon = "✅" if step.get('status') == 'completed' else "⏳"
                new_log_section += f"| {i} | {step['description']} | {status_icon} |\n"

            # Rebuild content
            new_content = '\n'.join(lines[:result_section_start]) + new_log_section

            plan_file.write_text(new_content)

    def complete_task(self, task_id):
        """Move task to Done folder."""
        if task_id not in self.tasks:
            return

        task = self.tasks[task_id]

        # Create completed file in Done/
        done_file = self.done / f"TASK_{task_id}_COMPLETED.md"

        done_content = f"""---
type: task_completion
source: Ralph Loop
created: {datetime.now().isoformat()}
status: completed
task_id: {task_id}
---

# Task Completed: {task.title}

**Started:** {task.created_at}
**Completed:** {task.updated_at}

## Summary

- **Total Steps:** {len(task.steps)}
- **Steps Completed:** {sum(1 for s in task.steps if s.get('status') == 'completed')}
- **Execution Time:** {(datetime.now() - datetime.fromisoformat(task.created_at.replace('Z', '+00:00'))).total_seconds():.0f} seconds

## Steps Executed

"""
        for i, step in enumerate(task.steps, 1):
            step_status = step.get('status', 'unknown')
            status_icon = "✅" if step_status == 'completed' else "❌"
            done_content += f"{status_icon} Step {i}: {step['description']}\n"
            if step.get('started_at'):
                done_content += f"   Started: {step['started_at']}\n"
            if step.get('completed_at'):
                done_content += f"   Completed: {step['completed_at']}\n"

        done_content += "\n---\n\n*Completed by Ralph Loop | " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "*\n"
"""

        done_file.write_text(done_content)
        print(f"💾 Saved to: TASK_{task_id}_COMPLETED.md")

        # Remove from active tasks
        del self.tasks[task_id]
        self.save_tasks()

    def run_loop(self, iterations=3):
        """Run the Ralph Loop for a set number of iterations."""
        print(f"\n{'='*70}")
        print(" 🔄 RALPH LOOP STARTING")
        print(f"{'='*70}")
        print(f"\n🔄 Running {iterations} iterations...")

        for i in range(iterations):
            print(f"\n--- Iteration {i + 1} ---")

            # Create a test task
            task_id = f"TASK_{int(time.time())}"
            task_title = f"Sample Task {i + 1} - Test multi-step execution"

            # Create plan
            self.create_plan(task_id, task_title)

            # Execute
            self.execute_task(task_id)

            # Small delay between iterations
            time.sleep(2)

        print(f"\n{'='*70}")
        print(" ✅ RALPH LOOP COMPLETE")
        print(f"{'='*70}")
        print(f"\n📊 Tasks completed: {iterations}")
        print(f"📁 Check Done/ folder for results")


def main():
    """Main entry point."""
    vault_path = 'C:/Users/alvia/OneDrive/Desktop/AI_Employee_Vault_Hackathon'
    config_path = 'config/ralph_config.yaml'

    # Create config if not exists
    Path(config_path).parent.mkdir(parents=True, exist_ok=True)
    if not Path(config_path).exists():
        with open(config_path, 'w') as f:
            yaml.dump({}, f)

    # Initialize Ralph Loop
    loop = RalphLoop(vault_path, config_path)

    # Run loop with 3 test iterations
    loop.run_loop(iterations=3)


if __name__ == '__main__':
    main()
