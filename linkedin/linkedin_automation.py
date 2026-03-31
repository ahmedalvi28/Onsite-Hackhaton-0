"""
LinkedIn Complete Automation System
- Auto-post daily content
- Monitor notifications/messages
- Auto-accept connection requests
- Create follow-up tasks

Usage:
    python linkedin_automation.py --post        # Post today's content
    python linkedin_automation.py --monitor     # Monitor for new activity
    python linkedin_automation.py --accept      # Accept all connection requests
    python linkedin_automation.py --full        # Run all tasks
"""

import yaml
import secrets
import time
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
except ImportError:
    print("❌ Selenium not installed. Run: pip install selenium")
    exit(1)


class LinkedInAutomation:
    """Complete LinkedIn automation system."""

    def __init__(self, config_file: str = 'config/linkedin_config.yaml'):
        """Initialize LinkedIn automation."""
        self.config_file = config_file
        self.config = self._load_config()

        # Vault paths
        self.vault_path = Path('C:/Users/alvia/OneDrive/Desktop/AI_Employee_Vault_Hackathon')
        self.needs_action = self.vault_path / 'Needs_Action'
        self.done_folder = self.vault_path / 'Done'
        self.logs = self.vault_path / 'Logs'

        # Create folders
        self.needs_action.mkdir(parents=True, exist_ok=True)
        self.done_folder.mkdir(parents=True, exist_ok=True)
        self.logs.mkdir(parents=True, exist_ok=True)

        # Browser
        self.driver = None

    def _load_config(self) -> Dict:
        """Load configuration."""
        with open(self.config_file, 'r') as f:
            return yaml.safe_load(f)

    def _init_driver(self, headless: bool = False) -> webdriver.Chrome:
        """Initialize Chrome driver."""
        chrome_options = Options()
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        if headless:
            chrome_options.add_argument('--headless')
        else:
            chrome_options.add_argument('--start-maximized')
        return webdriver.Chrome(options=chrome_options)

    def _login(self) -> bool:
        """Login to LinkedIn."""
        if not self.driver:
            self.driver = self._init_driver()

        print("🔐 Logging in to LinkedIn...")
        self.driver.get('https://www.linkedin.com/login')
        time.sleep(3)

        try:
            email_field = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.ID, 'username'))
            )
            email_field.send_keys(self.config.get('linkedin_email', ''))
            time.sleep(0.5)

            password_field = self.driver.find_element(By.ID, 'password')
            password_field.send_keys(self.config.get('linkedin_password', ''))
            time.sleep(0.5)

            self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
            time.sleep(10)

            print("✅ Logged in successfully")
            return True
        except Exception as e:
            print(f"❌ Login failed: {e}")
            return False

    def get_daily_topic(self) -> str:
        """Get today's topic based on day of week."""
        day = datetime.now().weekday()
        topics = {
            0: 'motivation',  # Monday
            1: 'productivity',  # Tuesday
            2: 'sales',  # Wednesday
            3: 'ai',  # Thursday
            4: 'business',  # Friday
            5: 'leadership',  # Saturday
            6: 'innovation'  # Sunday
        }
        return topics.get(day, 'ai')

    def generate_post_content(self, topic: Optional[str] = None) -> str:
        """Generate post content based on topic."""
        if not topic:
            topic = self.get_daily_topic()

        topics = {
            'ai': """🚀 Building the Future of Work!

We're creating an autonomous AI assistant that:
• Monitors emails, LinkedIn, and WhatsApp
• Generates plans automatically
• Posts to LinkedIn daily
• Handles scheduling and approvals

This isn't about AI replacing humans—it's about AI amplifying human creativity and productivity.

The future of work = Human + AI, not Human vs AI.

What are you building today?

#AI #Automation #Productivity #FutureOfWork #Innovation""",

            'productivity': """⚡ 5 Productivity Hacks That Changed My Life

1. Start your day with ONE important task (not a list of 10)
2. Use time-blocking for deep work (2-3 hours uninterrupted)
3. Take a REAL break every 90 minutes (walk, stretch, disconnect)
4. Process emails in batches (3x daily, not constantly)
5. End each day with a 5-minute review

Small changes = Compound growth. 📈

What's your go-to productivity hack?

#Productivity #Tips #WorkSmarter #BusinessGrowth""",

            'sales': """💡 How I Close More Deals Without Being "Salesy"

The secret isn't more pitches—it's more value.

Instead of "Did you get a chance to review?", try:
→ "I noticed your team is focusing on [X] this quarter..."
→ "Based on our last conversation, this might help with..."
→ "Most clients in your situation see [result] in 30 days..."

Give before you ask. Build trust first. Sell becomes a natural conclusion.

Your approach?

#Sales #Business #GrowthHacking #RelationshipBuilding""",

            'business': """📈 3 Keys to Sustainable Business Growth

1. Solve real problems, not just "create cool stuff"
2. Listen to customers more than you talk about yourself
3. Focus on retention over acquisition (it's 5x cheaper)

The best marketing? Happy customers telling their friends.

What's your best growth strategy?

#Business #Entrepreneurship #Growth #Strategy #Success""",

            'motivation': """🔥 Start Your Week Strong

"The best time to plant a tree was 20 years ago. The second best time is now."

This week, I challenge you to:
• Ship that thing you've been procrastinating on
• Reach out to ONE person who can help
• Say YES to one opportunity you'd normally pass

Don't wait for perfect. Start messy. Iterate fast.

What are you starting today?

#MondayMotivation #Action #GrowthMindset #Leadership #Business""",

            'leadership': """🎯 What Great Leaders Actually Do

It's not about being the smartest person in the room.

Great leaders:
• Ask better questions than they give answers
• Admit when they're wrong (and learn from it)
• Give credit, take blame
• Remove obstacles for their team
• Listen more than they speak

Leadership isn't a title. It's how you make others feel.

What's the best leadership advice you've received?

#Leadership #Management #Teamwork #Growth""",

            'innovation': """💡 Innovation Isn't Just for Tech Companies

Every business can innovate:

• Service companies: Simplify your customer journey
• Retail: Create experiences, not just transactions
• Manufacturing: Solve problems customers didn't know they had

Innovation = Making things better, not just different.

Where can you innovate today?

#Innovation #Business #Creativity #Entrepreneurship"""
        }
        return topics.get(topic, topics['ai'])

    def post_content(self, content: str, topic: str) -> bool:
        """Post content to LinkedIn."""
        print(f"\n📝 Posting LinkedIn content - Topic: {topic}")
        print("=" * 60)

        if not self._login():
            return False

        try:
            # Go to feed
            print("📄 Opening feed...")
            self.driver.get('https://www.linkedin.com/feed/')
            time.sleep(5)

            # Find post box
            print("🔍 Finding post box...")
            selectors = [
                'div[role="textbox"]',
                'div[contenteditable="true"]',
                '.share-box-feed-entry__trigger'
            ]

            post_box = None
            for selector in selectors:
                try:
                    post_box = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue

            if not post_box:
                # Try clicking "Start a post" button
                try:
                    start_button = self.driver.find_element(By.XPATH, '//button[contains(text(),"Start a post")]')
                    start_button.click()
                    time.sleep(2)
                    post_box = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[role="textbox"]'))
                    )
                except:
                    print("❌ Could not find post box")
                    return False

            # Click and paste content
            post_box.click()
            time.sleep(1)

            # Copy content to clipboard and paste
            from pyperclip import copy as clipboard_copy
            clipboard_copy(content)
            post_box.send_keys(Keys.CONTROL, 'v')
            time.sleep(2)

            # Find and click Post button
            print("📤 Looking for Post button...")
            post_selectors = [
                'button[aria-label*="Post"]',
                'button.share-actions__primary-action',
                '//button[contains(@aria-label, "Post")]'
            ]

            for selector in post_selectors:
                try:
                    if selector.startswith('//'):
                        post_button = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                    else:
                        post_button = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                    post_button.click()
                    print("✅ Post button clicked!")
                    time.sleep(5)
                    break
                except:
                    continue

            # Save to Done folder
            self._save_post_to_done(content, topic)
            self._log_activity("POSTED", f"Topic: {topic}")

            print("✅ Post successful!")
            return True

        except Exception as e:
            print(f"❌ Post failed: {e}")
            import traceback
            traceback.print_exc()
            return False

    def monitor_notifications(self) -> List[Dict]:
        """Monitor LinkedIn for new notifications."""
        if not self._login():
            return []

        print("\n🔔 Monitoring notifications...")

        try:
            self.driver.get('https://www.linkedin.com/notifications/')
            time.sleep(5)

            notifications = []

            # Find notification items
            notif_items = self.driver.find_elements(
                By.CSS_SELECTOR,
                '.global-nav__notification-item, .notification-item'
            )

            for item in notif_items[:10]:  # Get last 10
                try:
                    text = item.text
                    if text:
                        notifications.append({
                            'text': text[:200],
                            'time': datetime.now().isoformat()
                        })
                except:
                    continue

            if notifications:
                print(f"📋 Found {len(notifications)} notification(s)")
                for notif in notifications:
                    self._create_notification_task(notif)
            else:
                print("✨ No new notifications")

            return notifications

        except Exception as e:
            print(f"❌ Error monitoring: {e}")
            return []

    def accept_connections(self) -> int:
        """Accept all pending connection requests."""
        if not self._login():
            return 0

        print("\n🤝 Checking for connection requests...")

        try:
            # Go to notifications page (connection requests appear there)
            self.driver.get('https://www.linkedin.com/mynetwork/invitation-manager/')
            time.sleep(5)

            accepted = 0
            requests = self.driver.find_elements(
                By.CSS_SELECTOR,
                '.invitation-card, [data-urn*="INVITATION"]'
            )

            print(f"📋 Found {len(requests)} connection request(s)")

            for req in requests:
                try:
                    # Find accept button
                    accept_btns = req.find_elements(
                        By.XPATH,
                        '//button[contains(@aria-label, "Accept") or contains(., "Accept")]'
                    )

                    if accept_btns:
                        accept_btns[0].click()
                        time.sleep(1)
                        accepted += 1
                        print(f"✅ Accepted connection request #{accepted + 1}")

                except Exception as e:
                    print(f"⚠️  Failed to accept request: {e}")
                    continue

            if accepted > 0:
                self._log_activity("ACCEPTED_CONNECTIONS", f"Count: {accepted}")

            return accepted

        except Exception as e:
            print(f"❌ Error accepting connections: {e}")
            return 0

    def _save_post_to_done(self, content: str, topic: str):
        """Save post to Done folder."""
        post_id = secrets.token_hex(4)
        post_file = self.done_folder / f"LINKEDIN_AUTO_{datetime.now().strftime('%Y%m%d')}_{post_id}.md"

        post_content = f"""---
type: linkedin_post
source: Auto Poster
created: {datetime.now().isoformat()}
status: posted
category: business
priority: medium
topic: {topic}
---

# LINKEDIN_AUTO_{datetime.now().strftime('%Y%m%d')}

## LinkedIn Post Content

**Posted:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Topic:** {topic}

## Content

{content}

---

*Auto-posted*
"""
        post_file.write_text(post_content, encoding='utf-8')
        print(f"💾 Saved to: {post_file.name}")

    def _create_notification_task(self, notification: Dict):
        """Create task for notification."""
        task_id = secrets.token_hex(4)
        task_file = self.needs_action / f'LINKEDIN_NOTIF_{task_id}.md'

        content = f"""---
type: linkedin_notification
source: Automation Monitor
created: {datetime.now().isoformat()}
status: pending
category: business
priority: medium
---

# LINKEDIN_NOTIF_{task_id}

## Notification

**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Content

{notification['text']}

---

## Suggested Actions

- [ ] Review notification
- [ ] Take appropriate action
- [ ] Archive when done

---

*Auto-generated*
"""
        task_file.write_text(content, encoding='utf-8')
        print(f"📝 Created task: {task_file.name}")

    def _log_activity(self, action: str, details: str = ""):
        """Log activity."""
        log_file = self.logs / f'linkedin_automation_{datetime.now().strftime("%Y%m%d")}.log'
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {action}"
        if details:
            log_entry += f" - {details}"

        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + '\n')

    def close(self):
        """Close browser."""
        if self.driver:
            self.driver.quit()
            self.driver = None
            print("🔐 Browser closed")


def main():
    parser = argparse.ArgumentParser(description='LinkedIn Complete Automation')
    parser.add_argument('--post', action='store_true', help='Post daily content')
    parser.add_argument('--monitor', action='store_true', help='Monitor notifications')
    parser.add_argument('--accept', action='store_true', help='Accept connection requests')
    parser.add_argument('--full', action='store_true', help='Run all tasks')
    parser.add_argument('--topic', type=str, help='Override daily topic')
    parser.add_argument('--headless', action='store_true', help='Run in headless mode')

    args = parser.parse_args()

    automation = LinkedInAutomation()

    try:
        if args.full:
            # Run all tasks
            print("=" * 60)
            print("🤖 LinkedIn Full Automation")
            print("=" * 60)

            topic = args.topic or automation.get_daily_topic()
            content = automation.generate_post_content(topic)

            automation.post_content(content, topic)
            time.sleep(2)

            automation.accept_connections()
            time.sleep(2)

            automation.monitor_notifications()

            print("\n" + "=" * 60)
            print("🎉 All tasks completed!")
            print("=" * 60)

        elif args.post:
            topic = args.topic or automation.get_daily_topic()
            content = automation.generate_post_content(topic)
            automation.post_content(content, topic)

        elif args.monitor:
            automation.monitor_notifications()

        elif args.accept:
            accepted = automation.accept_connections()
            print(f"\n✅ Accepted {accepted} connection request(s)")

        else:
            print("Please specify an action: --post, --monitor, --accept, or --full")
            print("Example: python linkedin_automation.py --full")

    finally:
        automation.close()


if __name__ == '__main__':
    main()
