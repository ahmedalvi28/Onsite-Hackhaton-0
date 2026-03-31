"""
Social Media MCP Server - Multi-platform social posting
Handles Facebook, Instagram, Twitter (X) integration
"""

import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from pathlib import Path
import yaml
import requests

# Load config
config_path = Path(__file__).parent.parent.parent / 'config' / 'social_config.yaml'

DEFAULT_CONFIG = {
    'facebook': {
        'access_token': '',
        'page_id': ''
    },
    'instagram': {
        'access_token': '',
        'user_id': ''
    },
    'twitter': {
        'access_token': '',
        'user_id': ''
    }
}

with open(config_path, 'r') as f:
    user_config = yaml.safe_load(f) or {}

for platform, config in DEFAULT_CONFIG.items():
    if platform in user_config:
        DEFAULT_CONFIG[platform].update(user_config[platform])

# Create MCP server
app = Server("social-mcp-server")


@app.tool()
def post_to_facebook(content):
    """
    Post content to Facebook page.

    Args:
        content: Text content to post
    """
    try:
        token = DEFAULT_CONFIG['facebook']['access_token']
        page_id = DEFAULT_CONFIG['facebook']['page_id']

        if not token:
            return "Facebook access token not configured"

        print(f"Posting to Facebook...")

        url = f"https://graph.facebook.com/v18.0/{page_id}/feed"
        headers = {'Authorization': f'Bearer {token}'}

        payload = {
            'message': content,
            'access_token': token
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code in [200, 201]:
            post_id = response.json().get('id', 'Unknown')
            print(f"✅ Posted to Facebook: {post_id}")
            log_action("post_facebook", {
                'content_length': len(content),
                'post_id': post_id,
                'success': True
            })
            return f"Facebook post successful: {post_id}"
        else:
            error_msg = response.text
            print(f"❌ Facebook post failed: {error_msg}")
            log_action("post_facebook", {
                'content_length': len(content),
                'success': False,
                'error': error_msg
            })
            return f"Failed: {error_msg}"

    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(f"❌ {error_msg}")
        log_action("error", {'error': str(e), 'platform': 'facebook'})
        return error_msg


@app.tool()
def post_to_instagram(content):
    """
    Post content to Instagram.

    Args:
        content: Text content (caption) to post
    """
    try:
        token = DEFAULT_CONFIG['instagram']['access_token']

        if not token:
            return "Instagram access token not configured"

        print(f"Posting to Instagram...")

        url = "https://graph.instagram.com/v12.0/me/media"
        headers = {'Authorization': f'Bearer {token}'}

        # First upload media (placeholder)
        media_payload = {
            'caption': content,
            'access_token': token
        }

        response = requests.post(url, headers=headers, json=media_payload)

        if response.status_code in [200, 201]:
            media_id = response.json().get('id', 'Unknown')
            print(f"✅ Posted to Instagram: {media_id}")
            log_action("post_instagram", {
                'content_length': len(content),
                'media_id': media_id,
                'success': True
            })
            return f"Instagram post successful: {media_id}"
        else:
            error_msg = response.text
            print(f"❌ Instagram post failed: {error_msg}")
            log_action("post_instagram", {
                'content_length': len(content),
                'success': False,
                'error': error_msg
            })
            return f"Failed: {error_msg}"

    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(f"❌ {error_msg}")
        log_action("error", {'error': str(e), 'platform': 'instagram'})
        return error_msg


@app.tool()
def post_to_twitter(content):
    """
    Post content to Twitter (X).

    Args:
        content: Text content to tweet
    """
    try:
        token = DEFAULT_CONFIG['twitter']['access_token']

        if not token:
            return "Twitter access token not configured"

        print(f"Posting to Twitter (X)...")

        url = "https://api.twitter.com/2/tweets"
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        payload = {
            'text': content
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code in [200, 201]:
            tweet_data = response.json()
            tweet_id = tweet_data.get('data', {}).get('id', 'Unknown')
            print(f"✅ Posted to Twitter: {tweet_id}")
            log_action("post_twitter", {
                'content_length': len(content),
                'tweet_id': tweet_id,
                'success': True
            })
            return f"Twitter post successful: {tweet_id}"
        else:
            error_msg = response.text
            print(f"❌ Twitter post failed: {error_msg}")
            log_action("post_twitter", {
                'content_length': len(content),
                'success': False,
                'error': error_msg
            })
            return f"Failed: {error_msg}"

    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(f"❌ {error_msg}")
        log_action("error", {'error': str(e), 'platform': 'twitter'})
        return error_msg


@app.tool()
def generate_social_summary(days=7):
    """
    Generate a summary of social media activity.

    Args:
        days: Number of days to look back
    """
    try:
        print(f"Generating social media summary for last {days} days...")

        # Read log files
        logs_path = Path(__file__).parent.parent / 'logs'
        summary = {
            'facebook': {'posts': 0, 'engagement': 0},
            'instagram': {'posts': 0, 'engagement': 0},
            'twitter': {'tweets': 0, 'engagement': 0},
            'total': 0
        }

        log_file = logs_path / 'social_mcp_actions.jsonl'
        if log_file.exists():
            with open(log_file, 'r') as f:
                for line in f:
                    try:
                        entry = json.loads(line)
                        platform = entry.get('details', {}).get('platform', '')
                        if 'facebook' in platform.lower() and entry.get('action') == 'post_facebook':
                            summary['facebook']['posts'] += 1
                            summary['total'] += 1
                        elif 'instagram' in platform.lower() and entry.get('action') == 'post_instagram':
                            summary['instagram']['posts'] += 1
                            summary['total'] += 1
                        elif 'twitter' in platform.lower() and entry.get('action') == 'post_twitter':
                            summary['twitter']['tweets'] += 1
                            summary['total'] += 1
                    except:
                        pass

        print(f"✅ Summary: {summary}")

        return summary

    except Exception as e:
        print(f"❌ Error generating summary: {str(e)}")
        return {'error': str(e)}


@app.tool()
def post_to_all_platforms(content):
    """
    Post the same content to all configured platforms.

    Args:
        content: Content to post
    """
    results = {}

    if DEFAULT_CONFIG['facebook']['access_token']:
        results['facebook'] = post_to_facebook(content)
    else:
        results['facebook'] = "Not configured"

    if DEFAULT_CONFIG['instagram']['access_token']:
        results['instagram'] = post_to_instagram(content)
    else:
        results['instagram'] = "Not configured"

    if DEFAULT_CONFIG['twitter']['access_token']:
        results['twitter'] = post_to_twitter(content)
    else:
        results['twitter'] = "Not configured"

    return results


def log_action(action, details):
    """Log all actions for audit purposes."""
    logs_path = Path(__file__).parent.parent / 'logs'
    logs_path.mkdir(parents=True, exist_ok=True)

    log_file = logs_path / 'social_mcp_actions.jsonl'
    from datetime import datetime

    entry = {
        'timestamp': datetime.now().isoformat(),
        'action': action,
        'details': details
    }

    with open(log_file, 'a') as f:
        f.write(json.dumps(entry) + '\n')

    print(f"📝 Logged action: {action}")


async def main():
    """Main entry point for MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
