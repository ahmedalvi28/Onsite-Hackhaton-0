# LinkedIn Complete Automation

## Overview

Fully automated LinkedIn system that:
- 📝 Posts daily content automatically
- 🔔 Monitors notifications and messages
- 🤝 Accepts connection requests
- 📊 Creates tasks in Obsidian vault

## Quick Start

### 1. Install Dependencies

```bash
pip install selenium pyperclip pyyaml
```

### 2. Configure

Edit `config/linkedin_config.yaml`:

```yaml
linkedin_email: your@email.com
linkedin_password: your_password
```

### 3. Test

```bash
# Test posting
python linkedin/linkedin_automation.py --post

# Test monitoring
python linkedin/linkedin_automation.py --monitor

# Test accepting connections
python linkedin/linkedin_automation.py --accept

# Run everything
python linkedin/linkedin_automation.py --full
```

## Usage

### Manual Commands

```bash
# Post today's content (auto-detects topic)
python linkedin/linkedin_automation.py --post

# Post with specific topic
python linkedin/linkedin_automation.py --post --topic ai

# Monitor notifications
python linkedin/linkedin_automation.py --monitor

# Accept all connection requests
python linkedin/linkedin_automation.py --accept

# Run all tasks
python linkedin/linkedin_automation.py --full
```

### Automated Scheduler

```bash
# Run scheduler continuously
python linkedin/linkedin_scheduler.py

# Run once and exit
python linkedin/linkedin_scheduler.py --once --task full

# Custom schedule
python linkedin/linkedin_scheduler.py --post-time 10:00 --check-time 15:00
```

### Windows Task Scheduler

```bash
# Run as administrator
linkedin/setup_linkedin_scheduler.bat
```

## Daily Topics

| Day | Topic |
|-----|-------|
| Monday | Motivation |
| Tuesday | Productivity |
| Wednesday | Sales |
| Thursday | AI |
| Friday | Business |
| Saturday | Leadership |
| Sunday | Innovation |

## File Structure

```
linkedin/
├── linkedin_automation.py      # Main automation script
├── linkedin_scheduler.py       # Continuous scheduler
├── setup_linkedin_scheduler.bat # Windows setup
└── LINKEDIN_AUTOMATION_README.md

config/
└── linkedin_config.yaml       # Configuration file

Vault/
├── Needs_Action/               # Auto-generated tasks
├── Done/                       # Posted content logs
└── Logs/                       # Activity logs
```

## Features

### Auto-Post
- Daily content based on day of week
- Engaging, business-focused posts
- Saves to Done folder for tracking

### Monitor
- Checks for new notifications
- Creates follow-up tasks
- Logs all activity

### Auto-Accept
- Automatically accepts connection requests
- Logs accepted connections

### Task Integration
- Creates Obsidian tasks for notifications
- Saves posted content to Done folder
- Maintains activity logs

## Troubleshooting

### "Element not found" errors
- LinkedIn UI may have changed
- Wait times may need adjustment
- Try running with --headless flag removed

### Login fails
- Check email/password in config
- Verify LinkedIn credentials are correct
- Check for 2FA requirements

### Browser doesn't close
- Script handles cleanup in finally block
- Force close: Task Manager → Chrome

## Customization

### Add Custom Topics
Edit `linkedin_automation.py` in `generate_post_content()` method:

```python
topics = {
    'your_topic': """Your post content here...
    """
}
```

### Change Schedule
Edit `linkedin_scheduler.py`:
```python
post_time: str = "09:00"  # Change post time
check_time: str = "14:00"  # Change check time
```

### Modify Posts
Edit `generate_post_content()` in `linkedin_automation.py`
to customize post templates.

## Security

⚠️ **Important:**
- Never commit `config/linkedin_config.yaml`
- Keep credentials secure
- Review auto-posted content before scheduling
- Consider using environment variables for production

## License

MIT License - Use freely for personal and commercial projects.

---

*LinkedIn Complete Automation | Last Updated: 2026-04-01*
