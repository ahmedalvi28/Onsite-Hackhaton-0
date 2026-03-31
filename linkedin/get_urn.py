"""
Get your LinkedIn Person URN from profile URL
"""

import re

def get_urn_from_url(profile_url):
    """
    Extract person ID from LinkedIn profile URL.
    Note: This is a simplified approach.
    """
    # Remove trailing slash
    profile_url = profile_url.rstrip('/')

    # Extract the profile identifier from URL
    # Format: https://www.linkedin.com/in/username/
    match = re.search(r'linkedin\.com/in/([^/?]+)', profile_url)

    if match:
        username = match.group(1)
        return username
    return None

# Alternative: Use LinkedIn API to get URN if your app has proper permissions
# For now, you need to:
# 1. Find your LinkedIn Member ID (numeric)
# 2. Use format: urn:li:person:MEMBER_ID

# To find your Member ID:
# 1. Go to your LinkedIn profile
# 2. Open browser DevTools (F12)
# 3. Go to Network tab
# 4. Refresh page and look for API calls
# 5. Find "publicProfileIdentifier" or similar in response

# Or use LinkedIn's member ID lookup tool:
# https://www.linkedin.com/psettings/member-data

if __name__ == '__main__':
    url = input("Enter your LinkedIn profile URL: ")
    urn = get_urn_from_url(url)
    if urn:
        print(f"\nYour profile identifier: {urn}")
        print(f"Your URN format: urn:li:person:{urn}")
        print("\nNote: This may not be your numeric Member ID.")
        print("For posting, you need your actual numeric LinkedIn Member ID.")
    else:
        print("Invalid LinkedIn profile URL")
