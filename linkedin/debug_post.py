"""
LinkedIn Post Debug - Shows what's happening
"""

import yaml
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import time

# Load config
config_path = Path(__file__).parent.parent / 'config' / 'linkedin_config.yaml'
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

LINKEDIN_EMAIL = config.get('linkedin_email', '')
LINKEDIN_PASSWORD = config.get('linkedin_password', '')

content = """🚀 Test Post!

This is a test post.

#Test
"""

chrome_options = Options()
chrome_options.add_argument('--start-maximized')
driver = webdriver.Chrome(options=chrome_options)

try:
    driver.get('https://www.linkedin.com/login')
    time.sleep(3)

    # Login
    driver.find_element(By.ID, 'username').send_keys(LINKEDIN_EMAIL)
    driver.find_element(By.ID, 'password').send_keys(LINKEDIN_PASSWORD)
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    print("⏳ Waiting for login...")
    time.sleep(15)

    # Go to post page
    driver.get('https://www.linkedin.com/post/new/')
    time.sleep(5)

    # Save screenshot
    driver.save_screenshot('debug_1_post_page.png')
    print("💾 Saved: debug_1_post_page.png")

    # Find all buttons and print their text
    print("\n📤 ALL BUTTONS ON PAGE:")
    print("=" * 50)
    buttons = driver.find_elements(By.TAG_NAME, 'button')
    for i, btn in enumerate(buttons):
        btn_text = btn.text.strip() if btn.text else '(no text)'
        btn_class = btn.get_attribute('class') or ''
        btn_aria = btn.get_attribute('aria-label') or ''
        print(f"{i+1}. Text: '{btn_text}' | Class: '{btn_class[:50]}...' | Aria: '{btn_aria}'")

    print("=" * 50)

    # Find text editor
    try:
        textarea = driver.find_element(By.CSS_SELECTOR, 'div[contenteditable="true"]')
        textarea.click()
        time.sleep(1)
        textarea.send_keys(content)
        print("✅ Content typed")

        # Save screenshot
        driver.save_screenshot('debug_2_content_typed.png')
        print("💾 Saved: debug_2_content_typed.png")
        time.sleep(3)

        # Look for Post button again
        print("\n📤 LOOKING FOR 'Post' BUTTON:")
        print("=" * 50)
        for i, btn in enumerate(buttons):
            btn_text = btn.text.strip() if btn.text else ''
            if 'post' in btn_text.lower():
                print(f"FOUND {i+1}. Text: '{btn_text}'")
                print(f"   Enabled: {btn.is_enabled()}")
                print(f"   Clicking...")
                btn.click()
                time.sleep(5)
                driver.save_screenshot('debug_3_after_post_click.png')
                print("💾 Saved: debug_3_after_post_click.png")
                break
        print("=" * 50)

    except Exception as e:
        print(f"❌ Error: {e}")

    input("\nPress Enter to close...")

finally:
    driver.quit()
