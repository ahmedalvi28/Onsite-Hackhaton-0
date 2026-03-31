"""
Base Watcher - Abstract base class for all watchers.

All watchers should inherit from this class and implement the required methods.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict, Any


class BaseWatcher(ABC):
    """Abstract base class for watchers."""

    def __init__(self, vault_path: str, check_interval: int = 120):
        """
        Initialize the watcher.

        Args:
            vault_path: Path to the Obsidian vault
            check_interval: How often to check for updates (in seconds)
        """
        self.vault_path = Path(vault_path)
        self.check_interval = check_interval

        # Set up folder paths
        self.needs_action = self.vault_path / 'Needs_Action'
        self.in_progress = self.vault_path / 'In_Progress'
        self.plans = self.vault_path / 'Plans'
        self.pending_approval = self.vault_path / 'Pending_Approval'
        self.approved = self.vault_path / 'Approved'
        self.rejected = self.vault_path / 'Rejected'
        self.done = self.vault_path / 'Done'
        self.logs = self.vault_path / 'Logs'

        # Create folders
        for folder in [self.needs_action, self.in_progress, self.plans,
                      self.pending_approval, self.approved, self.rejected,
                      self.done, self.logs]:
            folder.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def check_for_updates(self) -> List[Any]:
        """
        Check for new updates.

        Returns:
            List of new items to process
        """
        pass

    @abstractmethod
    def create_action_file(self, item: Any) -> Optional[Path]:
        """
        Create an action file for an item.

        Args:
            item: The item to create an action file for

        Returns:
            Path to the created file, or None if failed
        """
        pass

    def log_activity(self, action: str, details: str = ""):
        """
        Log activity to the vault.

        Args:
            action: The action performed
            details: Additional details
        """
        log_file = self.logs / f'{self.__class__.__name__.lower()}_{datetime.now().strftime("%Y%m%d")}.log'

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {action}"

        if details:
            log_entry += f" - {details}"

        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry + '\n')
        except Exception as e:
            print(f"⚠️  Could not write to log: {e}")

    def watch(self):
        """
        Main watch loop.

        Subclasses can override this for custom behavior.
        """
        print(f"🔔 {self.__class__.__name__} starting...")
        print(f"📁 Vault path: {self.vault_path}")
        print(f"⏰ Check interval: {self.check_interval} seconds")
        print("Press Ctrl+C to stop\n")

        self.log_activity("WATCHER_STARTED", f"Interval={self.check_interval}s")

        try:
            while True:
                # Check for updates
                new_items = self.check_for_updates()

                if new_items:
                    print(f"\n📋 Found {len(new_items)} new item(s)")

                    for item in new_items:
                        file_path = self.create_action_file(item)
                        if file_path:
                            self.log_activity("TASK_CREATED", str(file_path.name))
                        else:
                            print(f"⚠️  Failed to create task for item")

                    print(f"✅ All {len(new_items)} task(s) created\n")
                else:
                    print(f"✨ No new items at {datetime.now().strftime('%H:%M:%S')}")

                # Wait for next check
                import time
                time.sleep(self.check_interval)

        except KeyboardInterrupt:
            print("\n\n⏹️  Watcher stopped by user")
            self.log_activity("WATCHER_STOPPED", "User interrupt")
        except Exception as e:
            print(f"\n\n❌ Watcher crashed: {e}")
            self.log_activity("WATCHER_ERROR", str(e))
            raise
