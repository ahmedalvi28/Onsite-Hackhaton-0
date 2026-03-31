"""
LinkedIn API Auto Post - Using LinkedIn Marketing Developer API
No Selenium, faster, reliable, no risk of account ban
"""

import requests
import yaml
from pathlib import Path
from datetime import datetime
import secrets

# Load config
config_path = Path(__file__).parent.parent / 'config' / 'linkedin_config.yaml'
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

ACCESS_TOKEN = config.get('access_token', '')
PERSON_URN = config.get('person_urn', '')  # e.g., "urn:li:person:abc123"

# LinkedIn API v2 endpoints
BASE_URL = "https://api.linkedin.com/v2"
API_HEADERS = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Content-Type': 'application/json',
    'X-Restli-Protocol-Version': '2.0.0'
}

# Vault paths
vault_path = Path('C:/Users/alvia/OneDrive/Desktop/AI_Employee_Vault_Hackathon')
done_folder = vault_path / 'Done'
done_folder.mkdir(parents=True, exist_ok=True)

DEFAULT_CONTENT = """🚀 Building the Future of Work!

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


def get_person_urn():
    """Get the authenticated user's person URN if not configured."""
    if PERSON_URN:
        return PERSON_URN

    # Use member profile endpoint to get person URN
    response = requests.get(
        f"{BASE_URL}/me",
        headers={'Authorization': f'Bearer {ACCESS_TOKEN}'}
    )

    if response.status_code == 200:
        data = response.json()
        sub = data.get('sub', '')
        if sub:
            urn = f"urn:li:person:{sub}"
            # Save to config for future use
            config['person_urn'] = urn
            with open(config_path, 'w') as f:
                yaml.dump(config, f, default_flow_style=False)
            return urn
    return None


def create_ugc_post(content, person_urn):
    """
    Create and publish a UGC (User Generated Content) post on LinkedIn.

    API: POST /ugcPosts
    """
    # Build the UGC post payload
    post_payload = {
        "author": person_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": content
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    response = requests.post(
        f"{BASE_URL}/ugcPosts",
        headers=API_HEADERS,
        json=post_payload
    )

    return response


def post_to_linkedin(content=None):
    """Post content to LinkedIn using API."""

    if not ACCESS_TOKEN:
        print("❌ No access token found! Run linkedin_oauth_fix.py first.")
        return False

    if not content:
        content = DEFAULT_CONTENT

    print("=" * 70)
    print(" LINKEDIN API AUTO POST")
    print("=" * 70)

    # Get person URN
    print("\n📋 Getting user profile URN...")
    person_urn = get_person_urn()
    if not person_urn:
        print("❌ Failed to get person URN. Check access token.")
        return False
    print(f"✅ Person URN: {person_urn}")

    # Create and post
    print("\n📤 Creating post via LinkedIn API...")
    response = create_ugc_post(content, person_urn)

    if response.status_code == 201:
        post_data = response.json()
        post_id = post_data.get('id', '')
        print("\n" + "=" * 70)
        print(" ✓ POST SUCCESSFUL!")
        print("=" * 70)
        print(f"Post ID: {post_id}")
        print(f"Status: Published")
        print(f"Visibility: Public")

        # Save to done folder
        save_post_to_done(content, post_id)
        print(f"\n💾 Saved to Done folder")

        return True
    else:
        print("\n" + "=" * 70)
        print(" ❌ POST FAILED!")
        print("=" * 70)
        print(f"Status Code: {response.status_code}")
        print(f"Error: {response.text}")

        # Handle common errors
        if response.status_code == 401:
            print("\n⚠️  Access token expired or invalid. Run OAuth flow again:")
            print("   python linkedin/linkedin_oauth_fix.py")
        elif response.status_code == 403:
            print("\n⚠️  Permission denied. Check your app has w_member_social scope.")
        elif response.status_code == 429:
            print("\n⚠️  Rate limit exceeded. Wait before posting again.")

        return False


def save_post_to_done(content, post_id):
    """Save posted content to Done folder."""
    post_file = done_folder / f"LINKEDIN_POST_{datetime.now().strftime('%Y%m%d')}_{post_id[:8]}.md"
    post_file.write_text(f"""---
type: linkedin_post
created: {datetime.now().isoformat()}
status: posted
post_id: {post_id}
---
{content}
""")
    print(f"💾 Saved to: {post_file.name}")


def test_connection():
    """Test API connection and token validity."""
    print("=" * 70)
    print(" LINKEDIN API CONNECTION TEST")
    print("=" * 70)

    if not ACCESS_TOKEN:
        print("❌ No access token found!")
        return False

    # Test me endpoint
    response = requests.get(
        f"{BASE_URL}/me",
        headers={'Authorization': f'Bearer {ACCESS_TOKEN}'}
    )

    if response.status_code == 200:
        data = response.json()
        print("\n✅ Connection successful!")
        print(f"   Person URN: {data.get('sub', 'N/A')}")
        return True
    else:
        print(f"\n❌ Connection failed: {response.status_code}")
        print(f"   Error: {response.text}")
        return False


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        test_connection()
    else:
        post_to_linkedin()
