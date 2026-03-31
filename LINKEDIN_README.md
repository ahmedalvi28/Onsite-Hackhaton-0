# LinkedIn Integration

## Overview

Two posting methods available:

| Method | File | Description |
|--------|------|-------------|
| Selenium | `auto_post.py` | Browser automation - working but slower |
| API | `api_post.py` | LinkedIn API - faster, requires proper setup |

## Quick Start

### Method 1: Selenium Auto-Post (Working)

```bash
python linkedin/auto_post.py
```

**Pros:**
- Works immediately
- No API approval needed
- Visual confirmation

**Cons:**
- Opens browser
- Slower
- Risk of bot detection

### Method 2: LinkedIn API (Recommended but requires setup)

1. Get OAuth token:
```bash
python linkedin/oauth_flow.py
```

2. Find your Member ID:
```bash
python linkedin/find_member_id.py
```

3. Add to `config/linkedin_config.yaml`:
```yaml
person_urn: urn:li:person:YOUR_NUMERIC_ID
```

4. Test:
```bash
python linkedin/api_post.py --test
python linkedin/api_post.py
```

## Files

| File | Purpose |
|------|---------|
| `auto_post.py` | Selenium-based auto poster |
| `api_post.py` | LinkedIn API poster |
| `oauth_flow.py` | OAuth token generator |
| `find_member_id.py` | Member ID finder |
| `linkedin_watcher.py` | LinkedIn content watcher |

## Configuration

Edit `config/linkedin_config.yaml`:

```yaml
access_token: YOUR_ACCESS_TOKEN
person_urn: urn:li:person:YOUR_MEMBER_ID
linkedin_email: your@email.com
linkedin_password: your_password
```

## LinkedIn Developer Portal

**Required Setup:**

1. Create app at: https://developer.linkedin.com/
2. Add Redirect URI: `http://localhost:8080/callback`
3. OAuth 2.0 Scopes: `w_member_social`
4. Apply for UGC API access

**Note:** API access requires LinkedIn Developer Program approval.

## Troubleshooting

### Selenium Issues
- `TimeOutError`: Increase wait times in `auto_post.py`
- `Element not found`: LinkedIn UI changed - update selectors

### API Issues
- `403 ACCESS_DENIED`: App lacks API permissions - apply for access
- `Invalid Person URN`: Check your Member ID is correct
- `401 Unauthorized`: Token expired - run OAuth flow again

## Usage with Skills

Use the `/linkedin-post` skill to post from Claude Code:

```
/linkedin-post topic="AI productivity" type=insight
```

## Security

⚠️ **Important:**
- Never commit `config/linkedin_config.yaml` to version control
- Use environment variables for production
- Rotate access tokens regularly
- Tokens expire after 60 days

---

*Last Updated: 2026-03-31*
