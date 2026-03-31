"""
Gmail Watcher - Monitors Gmail for new unread emails and creates tasks.

Usage:
    python gmail_watcher.py --auth          # First time authentication
    python gmail_watcher.py                # Start watching for emails
"""

import os
import sys
import time
import argparse
import yaml
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

# Google API imports
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Scopes for Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


class GmailWatcher:
    """Monitors Gmail for new unread emails."""

    def __init__(self, vault_path: str, credentials_file: str = 'credentials.json',
                 token_file: str = 'token.json', config_file: str = 'config/gmail_config.yaml'):
        """
        Initialize Gmail Watcher.

        Args:
            vault_path: Path to the Obsidian vault
            credentials_file: Path to OAuth credentials JSON
            token_file: Path to store/refresh token JSON
            config_file: Path to configuration YAML file
        """
        self.vault_path = Path(vault_path)
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.config_file = config_file

        # Set up folder paths
        self.needs_action = self.vault_path / 'Needs_Action'
        self.needs_action.mkdir(parents=True, exist_ok=True)

        self.logs = self.vault_path / 'Logs'
        self.logs.mkdir(parents=True, exist_ok=True)

        # Configuration
        self.config = self._load_config()

        # Gmail API service
        self.service = None

        # Track processed message IDs
        self.processed_ids = set()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        default_config = {
            'check_interval': 120,  # seconds
            'query': 'is:unread',
            'max_results': 10,
            'label': 'INBOX',
            'priority_threshold': 'medium'  # low, medium, high
        }

        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                user_config = yaml.safe_load(f) or {}
            default_config.update(user_config)

        return default_config

    def authenticate(self) -> bool:
        """
        Authenticate with Gmail API.

        Returns:
            True if authentication successful, False otherwise
        """
        creds = None

        # Load existing token if available
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, SCOPES)

        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    print("✅ Token refreshed successfully")
                except Exception as e:
                    print(f"⚠️  Token refresh failed: {e}")
                    creds = None

            if not creds:
                if not os.path.exists(self.credentials_file):
                    print(f"❌ Credentials file not found: {self.credentials_file}")
                    print("Please download it from Google Cloud Console")
                    return False

                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_file, SCOPES
                    )
                    creds = flow.run_local_server(port=0)
                    print("✅ Authentication successful")
                except Exception as e:
                    print(f"❌ Authentication failed: {e}")
                    return False

            # Save credentials for next run
            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())
            print(f"✅ Token saved to {self.token_file}")

        try:
            self.service = build('gmail', 'v1', credentials=creds)
            print("✅ Gmail API service initialized")
            return True
        except Exception as e:
            print(f"❌ Failed to build Gmail service: {e}")
            return False

    def get_new_messages(self) -> list:
        """
        Get new unread messages from Gmail.

        Returns:
            List of message dictionaries
        """
        if not self.service:
            return []

        try:
            results = self.service.users().messages().list(
                userId='me',
                q=self.config['query'],
                maxResults=self.config['max_results']
            ).execute()

            messages = results.get('messages', [])

            # Filter out already processed messages
            new_messages = [m for m in messages if m['id'] not in self.processed_ids]

            return new_messages

        except HttpError as e:
            print(f"❌ Gmail API error: {e}")
            return []
        except Exception as e:
            print(f"❌ Error fetching messages: {e}")
            return []

    def get_message_details(self, message_id: str) -> Optional[Dict[str, Any]]:
        """
        Get full details of a message.

        Args:
            message_id: The Gmail message ID

        Returns:
            Dictionary with message details or None if error
        """
        try:
            msg = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format='full'
            ).execute()

            return msg

        except HttpError as e:
            print(f"❌ Error fetching message {message_id}: {e}")
            return None
        except Exception as e:
            print(f"❌ Error fetching message {message_id}: {e}")
            return None

    def extract_body(self, payload: Dict[str, Any]) -> str:
        """
        Extract email body from payload.

        Args:
            payload: Email payload from Gmail API

        Returns:
            Email body as string
        """
        body = ""

        # Try to get body from different possible locations
        if 'body' in payload and 'data' in payload['body']:
            import base64
            body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8', errors='ignore')

        # Check multipart
        elif 'parts' in payload:
            for part in payload['parts']:
                # Prefer HTML
                if part.get('mimeType') == 'text/html':
                    import base64
                    if 'data' in part.get('body', {}):
                        body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')
                        break
                # Fall back to plain text
                elif part.get('mimeType') == 'text/plain':
                    import base64
                    if 'data' in part.get('body', {}):
                        body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')

        return body

    def determine_priority(self, headers: Dict[str, str]) -> str:
        """
        Determine email priority from headers.

        Args:
            headers: Email headers dictionary

        Returns:
            Priority level: low, medium, or high
        """
        subject = headers.get('Subject', '').lower()
        from_email = headers.get('From', '').lower()

        # High priority indicators
        high_priority_keywords = ['urgent', 'asap', 'important', 'deadline', 'emergency', 'critical']
        if any(keyword in subject for keyword in high_priority_keywords):
            return 'high'

        # Medium priority for business senders
        business_domains = ['@company.com', '@business.com', '@work.com']
        if any(domain in from_email for domain in business_domains):
            return 'medium'

        # Default to low
        return 'low'

    def determine_category(self, headers: Dict[str, str], body: str) -> str:
        """
        Determine email category.

        Args:
            headers: Email headers dictionary
            body: Email body text

        Returns:
            Category: personal, business, or other
        """
        subject = headers.get('Subject', '').lower()
        from_email = headers.get('From', '').lower()
        body_lower = body.lower()

        # Business indicators
        business_keywords = ['invoice', 'contract', 'proposal', 'meeting', 'project',
                           'deadline', 'client', 'invoice', 'payment', 'quote']
        if any(keyword in subject or keyword in body_lower for keyword in business_keywords):
            return 'business'

        # Personal indicators
        personal_domains = ['@gmail.com', '@yahoo.com', '@hotmail.com', '@outlook.com']
        if any(domain in from_email for domain in personal_domains):
            return 'personal'

        return 'other'

    def create_task_file(self, message: Dict[str, Any]) -> Optional[Path]:
        """
        Create a task file in Needs_Action folder.

        Args:
            message: Gmail message dictionary

        Returns:
            Path to created task file or None if error
        """
        message_id = message['id']
        msg = self.get_message_details(message_id)

        if not msg:
            return None

        # Extract headers
        headers = {h['name']: h['value'] for h in msg['payload']['headers']}

        from_email = headers.get('From', 'Unknown')
        subject = headers.get('Subject', 'No Subject')
        date = headers.get('Date', datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z'))

        # Extract body
        snippet = msg.get('snippet', '')
        body = self.extract_body(msg['payload'])

        # Determine priority and category
        priority = self.determine_priority(headers)
        category = self.determine_category(headers, body)

        # Clean body for markdown (basic HTML stripping)
        import re
        clean_body = re.sub(r'<[^>]+>', '', body)
        clean_body = re.sub(r'\s+', ' ', clean_body).strip()
        body_preview = clean_body[:500] if clean_body else snippet[:500]

        # Generate task ID
        task_id = message_id[:8]  # Use first 8 chars of message ID

        # Create task content
        content = f"""---
type: gmail_email
source: Gmail Watcher
created: {datetime.now().isoformat()}
message_id: {message_id}
status: pending
category: {category}
priority: {priority}
---

# EMAIL_{task_id}

## Email Details

**From:** {from_email}
**Subject:** {subject}
**Received:** {date}
**Priority:** {priority}
**Category:** {category}

## Content Preview

{body_preview}...

---

## Quick Actions

- [ ] Read full email content
- [ ] Draft reply
- [ ] Add to calendar (if contains meeting)
- [ ] Extract attachments (if any)
- [ ] Forward to relevant person
- [ ] Archive after processing

## Reply Options

Use the `/send-email` skill to reply:
```
/send-email --to "{from_email}" --subject "Re: {subject}" --body "Your response here"
```

---

*Generated by Gmail Watcher | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

        # Write task file
        task_file = self.needs_action / f'EMAIL_{task_id}.md'

        try:
            task_file.write_text(content, encoding='utf-8')
            print(f"✅ Task created: EMAIL_{task_id}")

            # Mark message as read (optional - comment out if you want to keep unread)
            # self.mark_as_read(message_id)

            self.processed_ids.add(message_id)
            return task_file

        except Exception as e:
            print(f"❌ Error creating task file: {e}")
            return None

    def mark_as_read(self, message_id: str) -> bool:
        """
        Mark a message as read in Gmail.

        Args:
            message_id: The Gmail message ID

        Returns:
            True if successful, False otherwise
        """
        try:
            self.service.users().messages().modify(
                userId='me',
                id=message_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            return True
        except Exception as e:
            print(f"❌ Error marking message as read: {e}")
            return False

    def log_activity(self, action: str, details: str = ""):
        """Log activity to the vault."""
        log_file = self.logs / f'gmail_watcher_{datetime.now().strftime("%Y%m%d")}.log'

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
        print(f"🔔 Gmail Watcher starting...")
        print(f"📁 Vault path: {self.vault_path}")
        print(f"📂 Needs Action: {self.needs_action}")
        print(f"⏰ Check interval: {self.config['check_interval']} seconds")
        print(f"🔍 Query: {self.config['query']}")
        print("Press Ctrl+C to stop\n")

        self.log_activity("WATCHER_STARTED", f"Interval={self.config['check_interval']}s")

        try:
            while True:
                # Get new messages
                new_messages = self.get_new_messages()

                if new_messages:
                    print(f"\n📧 Found {len(new_messages)} new email(s)")

                    for msg in new_messages:
                        task_file = self.create_task_file(msg)
                        if task_file:
                            self.log_activity("TASK_CREATED", str(task_file.name))

                    print(f"✅ All {len(new_messages)} task(s) created\n")
                else:
                    print(f"✨ No new emails at {datetime.now().strftime('%H:%M:%S')}")

                # Wait for next check
                time.sleep(self.config['check_interval'])

        except KeyboardInterrupt:
            print("\n\n⏹️  Gmail Watcher stopped by user")
            self.log_activity("WATCHER_STOPPED", "User interrupt")
        except Exception as e:
            print(f"\n\n❌ Gmail Watcher crashed: {e}")
            self.log_activity("WATCHER_ERROR", str(e))


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Gmail Watcher - Monitor Gmail for new emails')
    parser.add_argument('--auth', action='store_true',
                       help='Authenticate with Gmail (first time setup)')
    parser.add_argument('--vault-path', type=str, default='C:/Users/alvia/OneDrive/Desktop/AI_Employee_Vault_Hackathon',
                       help='Path to Obsidian vault')
    parser.add_argument('--credentials', type=str, default='credentials.json',
                       help='Path to OAuth credentials (default: credentials.json)')
    parser.add_argument('--token', type=str, default='token.json',
                       help='Path to OAuth token (default: token.json)')
    parser.add_argument('--config', type=str, default='config/gmail_config.yaml',
                       help='Path to config file (default: config/gmail_config.yaml)')

    args = parser.parse_args()

    # Create watcher instance
    watcher = GmailWatcher(
        vault_path=args.vault_path,
        credentials_file=args.credentials,
        token_file=args.token,
        config_file=args.config
    )

    # Authenticate if requested
    if args.auth:
        print("🔐 Starting authentication...")
        if watcher.authenticate():
            print("✅ Authentication complete! Run without --auth to start watching.")
        else:
            print("❌ Authentication failed!")
            sys.exit(1)
    else:
        # Start watching
        if watcher.authenticate():
            watcher.watch()
        else:
            print("❌ Could not authenticate. Run with --auth to set up credentials.")
            sys.exit(1)


if __name__ == '__main__':
    main()
