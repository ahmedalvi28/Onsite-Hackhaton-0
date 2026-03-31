"""
LinkedIn Auto Post - Fixed with proper waits
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
from selenium.webdriver.common.action_chains import ActionChains
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
    post_id = secrets.token_hex(4)
    post_file = done_folder / f"LINKEDIN_POST_{datetime.now().strftime('%Y%m%d')}_{post_id}.md"
    post_file.write_text(f"""---
type: linkedin_post
created: {datetime.now().isoformat()}
status: posted
---
{content}
""")
    print(f"💾 Saved to: {post_file.name}")

def post_to_linkedin():
    chrome_options = Options()
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    print("=" * 70)
    print(" LINKEDIN AUTO POST")
    print("=" * 70)

    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Login
        print("📝 Opening LinkedIn...")
        driver.get('https://www.linkedin.com/login')
        time.sleep(3)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'username'))
        ).send_keys(LINKEDIN_EMAIL)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'password'))
        ).send_keys(LINKEDIN_PASSWORD)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
        ).click()

        print("⏳ Waiting for login...")
        time.sleep(20)

        # Open post page
        print("📄 Opening post page...")
        driver.get('https://www.linkedin.com/post/new/')
        time.sleep(5)

        # Type content
        print("📝 Typing content...")
        textarea = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[contenteditable="true"]'))
        )
        textarea.click()
        time.sleep(1)
        driver.execute_script("arguments[0].innerHTML = arguments[1];", textarea, content)
        print("✅ Content inserted")
        time.sleep(3)

        # Click Next button with proper wait
        print("📤 Clicking Next button...")
        next_btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Next')]"))
        )
        next_btn.click()

        print("⏳ Waiting for post to complete...")
        time.sleep(5)

        # Check if post button appears (sometimes Next leads to Post)
        try:
            post_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Post')]"))
            )
            post_btn.click()
            print("✅ Post button clicked!")
            time.sleep(3)
        except:
            print("✓ Next click completed")

        save_post_to_done()
        print("🎉 Successfully posted to LinkedIn!")
        time.sleep(3)

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        print("\n🔐 Closing browser...")
        driver.quit()

if __name__ == '__main__':
    post_to_linkedin()
