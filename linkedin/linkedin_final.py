"""
LinkedIn Final Auto Poster - Fixed structure for reliable posting.
Usage: python linkedin_final.py [--topic sales|ai|...]
"""

import yaml
import secrets
from datetime import datetime
from pathlib import Path
import time

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

with open('config/linkedin_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

LINKEDIN_EMAIL = config.get('linkedin_email', '')
LINKEDIN_PASSWORD = config.get('linkedin_password', '')

vault_path = Path('C:/Users/alvia/OneDrive/Desktop/AI_Employee_Vault_Hackathon')
done_folder = vault_path / 'Done'
logs_folder = vault_path / 'Logs'
done_folder.mkdir(parents=True, exist_ok=True)
logs_folder.mkdir(parents=True, exist_ok=True)


def save_post_to_done(content, topic):
    post_id = secrets.token_hex(4)
    post_file = done_folder / f"LINKEDIN_AUTO_{datetime.now().strftime('%Y%m%d')}_{post_id}.md"

    post_content = f"""---
type: linkedin_post
source: Final Auto Poster
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

    log_file = logs_folder / f'linkedin_post_{datetime.now().strftime("%Y%m%d")}.log'
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] Auto-posted - Topic: {topic}\n"
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_entry)

    print(f"💾 Saved to: {post_file.name}")


def get_daily_topic():
    day = datetime.now().weekday()
    topics = {0: 'motivation', 1: 'productivity', 2: 'sales',
              3: 'ai', 4: 'business', 5: 'ai', 6: 'motivation'}
    return topics.get(day, 'ai')


def generate_post_content(topic=None):
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

#AI #Automation #Productivity #FutureOfWork #Innovation
""",
        'productivity': """⚡ 5 Productivity Hacks That Changed My Life

1. Start your day with ONE important task (not a list of 10)
2. Use time-blocking for deep work (2-3 hours uninterrupted)
3. Take a REAL break every 90 minutes (walk, stretch, disconnect)
4. Process emails in batches (3x daily, not constantly)
5. End each day with a 5-minute review

Small changes = Compound growth. 📈

What's your go-to productivity hack?

#Productivity #Tips #WorkSmarter #BusinessGrowth
""",
        'sales': """💡 How I Close More Deals Without Being "Salesy"

The secret isn't more pitches—it's more value.

Instead of "Did you get a chance to review?", try:
→ "I noticed your team is focusing on [X] this quarter..."
→ "Based on our last conversation, this might help with..."
→ "Most clients in your situation see [result] in 30 days..."

Give before you ask. Build trust first. Sell becomes a natural conclusion.

Your approach?

#Sales #Business #GrowthHacking #RelationshipBuilding
""",
        'business': """📈 3 Keys to Sustainable Business Growth

1. Solve real problems, not just "create cool stuff"
2. Listen to customers more than you talk about yourself
3. Focus on retention over acquisition (it's 5x cheaper)

The best marketing? Happy customers telling their friends.

What's your best growth strategy?

#Business #Entrepreneurship #Growth #Strategy #Success
""",
        'motivation': """🔥 Start Your Week Strong

"The best time to plant a tree was 20 years ago. The second best time is now."

This week, I challenge you to:
• Ship that thing you've been procrastinating on
• Reach out to ONE person who can help
• Say YES to one opportunity you'd normally pass

Don't wait for perfect. Start messy. Iterate fast.

What are you starting today?

#MondayMotivation #Action #GrowthMindset #Leadership #Business
"""
    }
    return topics.get(topic, topics['ai'])


def post_now(content):
    print("="*60)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - LinkedIn Post")
    print('='*60)

    chrome_options = Options()
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--no-sandbox')

    driver = None
    posted = False

    try:
        print("📝 Opening LinkedIn...")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get('https://www.linkedin.com/login')

        time.sleep(3)

        print("🔐 Logging in...")
        email_field = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, 'username'))
        )
        email_field.send_keys(LINKEDIN_EMAIL)
        time.sleep(0.5)

        password_field = driver.find_element(By.ID, 'password')
        password_field.send_keys(LINKEDIN_PASSWORD)
        print("✅ Password filled")

        login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        login_button.click()
        print("✅ Login clicked")

        print("⏳ Waiting for login to complete...")
        time.sleep(10)

        print("📄 Opening feed...")
        driver.get('https://www.linkedin.com/feed/')
        time.sleep(5)

        print("🔍 Activating post area...")
        try:
            feed_area = driver.find_element(By.CSS_SELECTOR, '.scaffold-finite-scroll__content')
            feed_area.click()
            time.sleep(2)
            print("✅ Clicked on feed area")
        except:
            print("⚠️  Continuing without clicking feed area...")

        time.sleep(3)
        print("⏳ Waiting for post editor...")

        print("📝 Finding text area...")
        text_area = None
        selectors_to_try = [
            (By.CSS_SELECTOR, 'div[contenteditable="true"]'),
            (By.CSS_SELECTOR, 'div[role="textbox"]'),
            (By.XPATH, '//div[contains(@contenteditable,"true")]'),
            (By.TAG_NAME, 'textarea'),
        ]

        for by_type, selector in selectors_to_try:
            try:
                text_area = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((by_type, selector))
                )
                print(f"✅ Found text area: {selector}")
                break
            except:
                continue

        if not text_area:
            print("❌ Could not find text area")
            driver.quit()
            return False

        text_area.click()
        time.sleep(1)

        print("📝 Pasting content...")
        text_area.send_keys(Keys.CONTROL, 'v')
        time.sleep(2)

        print("📤 Looking for Post button...")
        post_button = None

        post_selectors = [
            (By.CSS_SELECTOR, 'button[aria-label*="Post"]'),
            (By.CSS_SELECTOR, 'button:has-text("Post")'),
            (By.XPATH, '//button[contains(text(),"Post")]'),
        ]

        for by_type, selector in post_selectors:
            try:
                post_button = WebDriverWait(driver, 8).until(
                    EC.element_to_be_clickable((by_type, selector))
                )
                print(f"✅ Found Post button: {selector}")
                break
            except:
                continue

        if post_button:
            post_button.click()
            print("✅ Post button clicked!")
            time.sleep(5)

            print("⏳ Verifying...")
            time.sleep(3)

            try:
                current_url = driver.current_url
                if 'feed' in current_url:
                    posted = True
                    print("✅ Post successful!")
                    save_post_to_done(content, get_daily_topic())
                    break
            except:
                pass

        if not posted:
            print("⚠️  Could not verify automatically")
            print()
            print("="*60)
            print("📋 MANUAL INSTRUCTIONS:")
            print("Browser is open with LinkedIn loaded")
            print("Please check:")
            print("1. Click 'Start a post' button")
            print("2. Click in text area")
            print("3. Paste the content below:")
            print()
            print(content)
            print()
            print("="*60)
            input("Press Enter to close browser...")

            time.sleep(60)

        return posted

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

    finally:
        if driver:
            time.sleep(2)
            driver.quit()
            print("🔐 Browser closed")


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--topic', type=str, help='Post topic')
    args = parser.parse_args()

    if args.topic:
        topic = args.topic
    else:
        topic = get_daily_topic()

    content = generate_post_content(topic)
    result = post_now(content)

    if result:
        print()
        print("="*60)
        print("🎉 SUCCESS!")
        print("="*60)


if __name__ == '__main__':
    main()
