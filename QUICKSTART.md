# Quick Start Guide

## 5-Minute Setup

### 1. Install Dependencies

```bash
pip install -r main/requirements.txt
```

### 2. Configure Credentials

Edit these files with your credentials:
- `config/gmail_config.yaml`
- `config/linkedin_config.yaml`
- `config/email_config.yaml`

### 3. Create Vault

```bash
mkdir -p AI_Employee_Vault_Hackathon/{Drop,Needs_Action,In_Progress,Plans,Pending_Approval,Approved,Rejected,Done,Logs,Reports}
```

### 4. Run Watchers

```bash
# Terminal 1 - Email
python gmail/gmail_watcher.py

# Terminal 2 - LinkedIn
python linkedin/linkedin_watcher.py

# Terminal 3 - Files
python main/watcher.py
```

### 5. Use Skills (Claude Code)

```
/process-tasks          # Process all pending tasks
/linkedin-post          # Post to LinkedIn
/create-plan            # Create task plan
/update-dashboard       # Update dashboard
```

---

## Common Commands

### LinkedIn

```bash
# Post using Selenium (working)
python linkedin/auto_post.py

# Post using API (requires setup)
python linkedin/api_post.py
```

### OAuth Setup

```bash
# LinkedIn OAuth
python linkedin/oauth_flow.py

# Gmail OAuth
python gmail/oauth_setup.py
```

### Tasks

```bash
# Process all tasks
/process-tasks

# Create specific plan
/create-plan task_id="TASK_ID"

# Update dashboard
/update-dashboard
```

---

## File Locations

| Purpose | Path |
|---------|------|
| Vault | `AI_Employee_Vault_Hackathon/` |
| Configs | `config/` |
| Logs | `logs/` |
| Watchers | `gmail/`, `linkedin/`, `whatsapp/`, `main/` |
| Skills | `.claude/skills/` |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Watcher not starting | Check port availability |
| OAuth failed | Run OAuth flow again |
| Task stuck | Check task status in Needs_Action |
| API error | Verify credentials and permissions |

---

*Last Updated: 2026-03-31*
