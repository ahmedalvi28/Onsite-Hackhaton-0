"""
Find your LinkedIn Member ID (numeric ID required for UGC posts)

Method 1: From LinkedIn Settings
1. Go to: https://www.linkedin.com/psettings/member-data
2. Scroll to "Data privacy" section
3. Find your Member ID there

Method 2: From Profile URL (may work for some)
1. Go to your LinkedIn profile
2. Right-click > "View Page Source"
3. Search for "profileMemberId" or "memberId:" in the source
4. Copy the numeric ID

Method 3: Browser DevTools (most reliable)
1. Go to your LinkedIn profile
2. Press F12 to open DevTools
3. Go to Network tab
4. Filter by "XHR" or "Fetch"
5. Reload the page
6. Look for API calls - find one containing your profile info
7. Check the response for "publicProfileIdentifier" or numeric ID

Your Person URN format will be:
    urn:li:person:YOUR_NUMERIC_MEMBER_ID

Example: If your Member ID is 123456789, your URN is:
    urn:li:person:123456789
"""

if __name__ == '__main__':
    print(__doc__)
    member_id = input("\nEnter your numeric LinkedIn Member ID: ").strip()
    if member_id.isdigit():
        print(f"\nYour Person URN: urn:li:person:{member_id}")
        print("\nAdd this to config/linkedin_config.yaml:")
        print(f"person_urn: urn:li:person:{member_id}")
    else:
        print("Invalid Member ID. Must be numeric.")
