"""
LinkedIn Post NOW - Uses "Next" button (not "Post")
"""

import yaml
from pathlib import Path
from datetime import datetime
import secrets
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

# Load config
config_path = Path(__file__).parent.parent / 'config' / 'linkedin_config.yaml'
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

LINKEDIN_EMAIL = config.get('linkedin_email', '')
LINKEDIN_PASSWORD = config.get('linkedin_password', '')

# Vault paths
vault_path = Path('C:/Users/alvia/OneDrive/Desktop/AI_Employee_Vault_Hackathon')
done_folder = vault_path / 'Done'
done_folder.mkdir(parents=True, exist_ok=True)

# Post content
content = """🚀 Building the Future of Work!

We're creating an autonomous AI assistant that:
• Monitors emails, LinkedIn, and WhatsApp
• Generates plans automatically
• Posts to LinkedIn daily
• Handles scheduling and approvals

This isn't about AI replacing humans—it's about AI amplifying human creativity and productivity.

The future of work = Human + AI, not Human vs AI.

What are you building today?

#AI #Automation #Productivity #FutureOfWork #Innovation
"""

def save_post_to_done():
    """Save posted content to Done folder."""
    post_id = secrets.token_hex(4)
    post_file = done_folder / f"LINKEDIN_POST_{datetime.now().strftime('%Y%m%d')}_{post_id}.md"

    post_content = f"""---
type: linkedin_post
source: Auto Post
created: {datetime.now().isoformat()}
status: posted
category: business
priority: medium
---

# LINKEDIN_POST_{datetime.now().strftime('%Y%m%d')}

## Posted Successfully

**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Content

{content}

---

*Auto-posted successfully*
"""

    post_file.write_text(post_content, encoding='utf-8')
    print(f"💾 Saved to: {post_file.name}")


def post_to_linkedin():
    """Post to LinkedIn automatically."""
    print("=" * 70)
    print(" LINKEDIN AUTO POST")
    print("=" * 70)
    print(content)
    print("=" * 70)
    print()

    chrome_options = Options()
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Open LinkedIn
        print("📝 Opening LinkedIn...")
        driver.get('https://www.linkedin.com/login')
        time.sleep(3)

        # Login
        print("🔐 Logging in...")
        email_field = driver.find_element(By.ID, 'username')
        email_field.send_keys(LINKEDIN_EMAIL)
        time.sleep(0.5)

        password_field = driver.find_element(By.ID, 'password')
        password_field.send_keys(LINKEDIN_PASSWORD)
        time.sleep(0.5)

        login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        login_button.click()
        print("⏳ Waiting for login...")
        time.sleep(15)

        # Go to post page
        print("📄 Opening post page...")
        driver.get('https://www.linkedin.com/post/new/')
        time.sleep(5)

        # Find text editor
        print("📝 Finding text editor...")
        textarea = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[contenteditable="true"]'))
        )
        print("✅ Found text editor")

        # Click to focus and type content
        textarea.click()
        time.sleep(1)
        print("📝 Typing content...")
        driver.execute_script("arguments[0].innerHTML = arguments[1];", textarea, content)
        print("✅ Content inserted")
        time.sleep(3)

        # Click "Next" button (not "Post"!)
        print("📤 Looking for 'Next' button...")
        post_clicked = False

        buttons = driver.find_elements(By.TAG_NAME, 'button')
        for btn in buttons:
            try:
                btn_text = btn.text.strip()
                # Look for "Next" button
                if btn_text == 'Next' and btn.is_enabled():
                    print(f"✅ Found 'Next' button! Clicking...")
                    btn.click()
                    time.sleep(5)
                    post_clicked = True
                    break
            except:
                continue

        if post_clicked:
            save_post_to_done()
            print("🎉 Successfully posted to LinkedIn!")
        else:
            print("❌ Could not find 'Next' button")
            print("⏸️  Browser will stay open for 30 seconds - click manually")
            time.sleep(30)

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        time.sleep(10)

    finally:
        print("\n🔐 Closing browser...")
        driver.quit()


if __name__ == '__main__':
    post_to_linkedin()
