"""
LinkedIn Watcher - Monitors LinkedIn for notifications and messages.

Usage:
    python linkedin_watcher.py
"""

import os
import sys
import time
import argparse
import yaml
import requests
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List


class LinkedInWatcher:
    """Monitors LinkedIn for new notifications and messages."""

    def __init__(self, vault_path: str, config_file: str = 'config/linkedin_config.yaml'):
        """
        Initialize LinkedIn Watcher.

        Args:
            vault_path: Path to Obsidian vault
            config_file: Path to configuration YAML file
        """
        self.vault_path = Path(vault_path)
        self.config_file = config_file

        # Set up folder paths
        self.needs_action = self.vault_path / 'Needs_Action'
        self.needs_action.mkdir(parents=True, exist_ok=True)

        self.logs = self.vault_path / 'Logs'
        self.logs.mkdir(parents=True, exist_ok=True)

        # Configuration
        self.config = self._load_config()

        # LinkedIn API configuration
        self.access_token = self.config.get('access_token', '')
        self.client_id = self.config.get('client_id', '')

        # LinkedIn API endpoints
        self.api_base = "https://api.linkedin.com/v2"
        self.notifications_endpoint = f"{self.api_base}/notifications"
        self.messages_endpoint = f"{self.api_base}/messages"

        # Track processed items
        self.processed_notifications = set()
        self.processed_messages = set()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        default_config = {
            'check_interval': 600,  # 10 minutes in seconds
            'max_results': 10,
            'access_token': '',
            'client_id': '',
            'priority_threshold': 'medium'
        }

        if Path(self.config_file).exists():
            with open(self.config_file, 'r') as f:
                user_config = yaml.safe_load(f) or {}
            default_config.update(user_config)

        return default_config

    def _validate_config(self) -> tuple[bool, str]:
        """
        Validate LinkedIn configuration.

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.config.get('access_token'):
            return False, "Access token not configured"

        if not self.config.get('client_id'):
            return False, "Client ID not configured"

        return True, ""

    def get_headers(self) -> Dict[str, str]:
        """Get HTTP headers for LinkedIn API requests."""
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0',
            'LinkedIn-Version': '202305'
        }

    def get_notifications(self) -> List[Dict[str, Any]]:
        """
        Get new LinkedIn notifications.

        Returns:
            List of notification dictionaries
        """
        if not self.access_token:
            return []

        try:
            headers = self.get_headers()

            # Get notifications
            response = requests.get(
                self.notifications_endpoint,
                headers=headers,
                params={
                    'q': 'urn:li-notification:(INVITE,CONNECTION,MESSAGE)',
                    'count': self.config['max_results']
                }
            )

            if response.status_code == 200:
                data = response.json()
                return data.get('elements', [])
            elif response.status_code == 401:
                print("⚠️  Token expired. Please re-authenticate.")
                return []
            else:
                print(f"❌ Error fetching notifications: {response.status_code}")
                return []

        except Exception as e:
            print(f"❌ Error: {e}")
            return []

    def get_messages(self) -> List[Dict[str, Any]]:
        """
        Get new LinkedIn messages.

        Returns:
            List of message dictionaries
        """
        if not self.access_token:
            return []

        try:
            headers = self.get_headers()

            # Get message conversations
            response = requests.get(
                f"{self.api_base}/messaging/conversations",
                headers=headers,
                params={
                    'key': 'version',
                    'projected': 'true',
                    'count': self.config['max_results']
                }
            )

            if response.status_code == 200:
                data = response.json()
                return data.get('elements', [])
            elif response.status_code == 401:
                print("⚠️  Token expired. Please re-authenticate.")
                return []
            else:
                print(f"❌ Error fetching messages: {response.status_code}")
                return []

        except Exception as e:
            print(f"❌ Error: {e}")
            return []

    def determine_priority(self, notification_type: str) -> str:
        """
        Determine notification priority.

        Args:
            notification_type: Type of notification

        Returns:
            Priority level: low, medium, or high
        """
        # High priority notifications
        high_priority_types = ['INVITATION', 'INMAIL', 'JOBOFFER', 'ENDORSEMENT']

        if notification_type in high_priority_types:
            return 'high'

        # Medium priority notifications
        medium_priority_types = ['CONNECTION', 'MESSAGE', 'RECOMMENDATION']

        if notification_type in medium_priority_types:
            return 'medium'

        # Default to low
        return 'low'

    def determine_category(self, notification_type: str) -> str:
        """
        Determine notification category.

        Args:
            notification_type: Type of notification

        Returns:
            Category: business, other
        """
        # Business-related notifications
        business_types = [
            'INVITATION', 'CONNECTION', 'RECOMMENDATION',
            'JOB_APPLICATION', 'JOBALERT', 'ENDORSEMENT',
            'INMAIL', 'COMPANY_PAGE', 'COMPANYFOLLOW'
        ]

        if notification_type in business_types:
            return 'business'

        return 'other'

    def create_notification_task(self, notification: Dict[str, Any]) -> Optional[Path]:
        """
        Create a task file for a LinkedIn notification.

        Args:
            notification: Notification dictionary from LinkedIn API

        Returns:
            Path to created task file or None if error
        """
        try:
            notification_id = notification.get('entityUrn', notification.get('id', 'unknown'))

            # Skip if already processed
            if notification_id in self.processed_notifications:
                return None

            # Extract notification details
            notification_type = notification.get('type', 'UNKNOWN')
            actor_name = notification.get('actor', {}).get('name', 'Unknown')
            actor_avatar = notification.get('actor', {}).get('profilePicture', {}).get('displayImage', '')

            # Get notification text
            notification_text = notification.get('text', {}).get('text', 'No description available')

            # Determine priority and category
            priority = self.determine_priority(notification_type)
            category = self.determine_category(notification_type)

            # Generate task ID
            import secrets
            task_id = secrets.token_hex(4)

            # Create task content
            content = f"""---
type: linkedin_notification
source: LinkedIn Watcher
created: {datetime.now().isoformat()}
notification_id: {notification_id}
status: pending
category: {category}
priority: {priority}
---

# LINKEDIN_{task_id}

## Notification Details

**Type:** {notification_type}
**From:** {actor_name}
**Received:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Priority:** {priority}
**Category:** {category}

## Message

{notification_text}

---

## Suggested Actions

- [ ] Read full notification
- [ ] View sender's profile
- [ ] Reply if it's a message
- [ ] Accept if it's a connection request
- [ ] Review if it's an endorsement
- [ ] Schedule follow-up if business related
- [ ] Archive after processing

## Quick Actions

- [ ] View on LinkedIn: Go to https://linkedin.com/notifications
- [ ] Reply via: LinkedIn website
- [ ] Add to CRM if it's a lead

---

*Generated by LinkedIn Watcher | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

            # Write task file
            task_file = self.needs_action / f'LINKEDIN_{task_id}.md'

            task_file.write_text(content, encoding='utf-8')
            print(f"✅ LinkedIn task created: LINKEDIN_{task_id}")

            self.processed_notifications.add(notification_id)
            return task_file

        except Exception as e:
            print(f"❌ Error creating task: {e}")
            return None

    def create_message_task(self, message: Dict[str, Any]) -> Optional[Path]:
        """
        Create a task file for a LinkedIn message.

        Args:
            message: Message dictionary from LinkedIn API

        Returns:
            Path to created task file or None if error
        """
        try:
            message_id = message.get('id', 'unknown')

            # Skip if already processed
            if message_id in self.processed_messages:
                return None

            # Extract message details
            participants = message.get('participants', [])
            sender = participants[0].get('firstName', 'Unknown') if participants else 'Unknown'
            sender_profile = participants[0].get('profilePicture', {}).get('displayImage', '') if participants else ''

            # Get message text (last message in conversation)
            last_message = message.get('events', [])[-1] if message.get('events') else {}
            message_text = last_message.get('payload', {}).get('text', 'No message text')

            # Determine priority and category
            priority = 'medium'
            category = 'business'

            # Generate task ID
            import secrets
            task_id = secrets.token_hex(4)

            # Create task content
            content = f"""---
type: linkedin_message
source: LinkedIn Watcher
created: {datetime.now().isoformat()}
message_id: {message_id}
status: pending
category: {category}
priority: {priority}
---

# LINKEDIN_MSG_{task_id}

## Message Details

**From:** {sender}
**Received:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Priority:** {priority}
**Category:** {category}

## Message

{message_text}

---

## Suggested Actions

- [ ] Read full conversation
- [ ] Reply if appropriate
- [ ] View sender's profile
- [ ] Add to CRM if it's a lead
- [ ] Schedule callback if needed
- [ ] Archive after processing

## Quick Actions

- [ ] View on LinkedIn: Go to https://linkedin.com/messaging
- [ ] Reply via: LinkedIn messaging
- [ ] Connect on LinkedIn if it's a new contact

---

*Generated by LinkedIn Watcher | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

            # Write task file
            task_file = self.needs_action / f'LINKEDIN_MSG_{task_id}.md'

            task_file.write_text(content, encoding='utf-8')
            print(f"✅ LinkedIn message task created: LINKEDIN_MSG_{task_id}")

            self.processed_messages.add(message_id)
            return task_file

        except Exception as e:
            print(f"❌ Error creating message task: {e}")
            return None

    def log_activity(self, action: str, details: str = ""):
        """Log activity to vault."""
        log_file = self.logs / f'linkedin_watcher_{datetime.now().strftime("%Y%m%d")}.log'

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
        """Main watch loop."""
        print("💼 LinkedIn Watcher starting...")
        print(f"📁 Vault path: {self.vault_path}")
        print(f"📂 Needs Action: {self.needs_action}")
        print(f"⏰ Check interval: {self.config['check_interval']} seconds")
        print("Press Ctrl+C to stop\n")

        self.log_activity("WATCHER_STARTED", f"Interval={self.config['check_interval']}s")

        try:
            while True:
                # Check for new notifications
                notifications = self.get_notifications()

                if notifications:
                    print(f"\n📋 Found {len(notifications)} new notification(s)")

                    for notification in notifications:
                        self.create_notification_task(notification)

                # Check for new messages
                messages = self.get_messages()

                if messages:
                    print(f"\n💬 Found {len(messages)} new message(s)")

                    for message in messages:
                        self.create_message_task(message)

                if not notifications and not messages:
                    print(f"✨ No new LinkedIn items at {datetime.now().strftime('%H:%M:%S')}")

                # Wait for next check
                time.sleep(self.config['check_interval'])

        except KeyboardInterrupt:
            print("\n\n⏹️  LinkedIn Watcher stopped by user")
            self.log_activity("WATCHER_STOPPED", "User interrupt")
        except Exception as e:
            print(f"\n\n❌ LinkedIn Watcher crashed: {e}")
            self.log_activity("WATCHER_ERROR", str(e))
            raise


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='LinkedIn Watcher - Monitor LinkedIn for notifications and messages')
    parser.add_argument('--vault-path', type=str, default='C:/Users/alvia/OneDrive/Desktop/AI_Employee_Vault_Hackathon',
                       help='Path to Obsidian vault')
    parser.add_argument('--config', type=str, default='config/linkedin_config.yaml',
                       help='Path to LinkedIn config (default: config/linkedin_config.yaml)')

    args = parser.parse_args()

    # Create watcher instance
    watcher = LinkedInWatcher(
        vault_path=args.vault_path,
        config_file=args.config
    )

    # Validate configuration
    is_valid, error = watcher._validate_config()
    if not is_valid:
        print(f"❌ Configuration error: {error}")
        print("Please create config/linkedin_config.yaml with your LinkedIn API credentials")
        print("Note: LinkedIn API requires developer access and OAuth setup")
        return

    # Start watching
    watcher.watch()


if __name__ == '__main__':
    main()
