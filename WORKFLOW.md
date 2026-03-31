# Personal AI Employee - Complete Workflow

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    INPUT SOURCES                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Email   │  │ LinkedIn │  │ WhatsApp │  │ Files    │   │
│  │  Watcher │  │  Watcher │  │  Watcher │  │  Drop    │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
└───────┼─────────────┼─────────────┼─────────────┼──────────┘
        │             │             │             │
        └─────────────┴─────────────┴─────────────┘
                      │
              ┌───────▼────────┐
              │  MCP Router    │
              └───────┬────────┘
                      │
              ┌───────▼────────┐
              │  Ralph Loop    │
              │  (Plan → Exec  │
              │   → Verify)    │
              └───────┬────────┘
                      │
              ┌───────▼────────┐
              │  Agent Skills  │
              └───────┬────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
   ┌────▼────┐  ┌────▼────┐  ┌────▼────┐
   │  Plans  │  │ Actions │  │ Reports │
   └─────────┘  └─────────┘  └─────────┘
```

## Daily Workflow

### 1. Setup (One-time)

```bash
# Install dependencies
pip install -r main/requirements.txt

# Create vault structure
mkdir -p AI_Employee_Vault_Hackathon/{Drop,Needs_Action,In_Progress,Plans,Pending_Approval,Approved,Rejected,Done,Logs,Reports}

# Configure credentials
# Edit config/*.yaml files with your credentials
```

### 2. Run Watchers

```bash
# Email watcher
python gmail/gmail_watcher.py

# LinkedIn watcher
python linkedin/linkedin_watcher.py

# WhatsApp watcher
python whatsapp/whatsapp_watcher.py

# File system watcher
python main/watcher.py
```

### 3. Process Tasks

Using Claude Code skills:

```bash
# Process all pending tasks
/process-tasks

# Create plan for specific task
/create-plan task_id="TASK_ID"

# Update dashboard
/update-dashboard

# Approve completed task
/approve-task task_id="TASK_ID"

# Reject task
/reject-task task_id="TASK_ID"

# Archive approved tasks
/archive-done
```

### 4. Social Media Posting

```bash
# LinkedIn (Selenium - working)
python linkedin/auto_post.py

# LinkedIn (API - requires setup)
python linkedin/api_post.py

# LinkedIn via skill
/linkedin-post topic="your topic" type=insight
```

## Vault Workflow

### Task States

```
Drop → Needs_Action → In_Progress → Plans → Pending_Approval → Approved/Rejected → Done
```

### Task File Format

```yaml
---
type: task_type
created: 2026-03-31T10:00:00Z
status: pending
priority: medium
---

Task description here...
```

### Plan File Format

```yaml
---
type: plan
task_id: TASK_ID
created: 2026-03-31T10:00:00Z
status: ready
---

## Plan for [Task Title]

### Step 1: [Description]
- [ ] Action item
- [ ] Another action

### Step 2: [Description]
- [ ] Action item
```

## MCP Server Workflow

### Available MCP Servers

| Server | Purpose | Status |
|--------|---------|--------|
| Email | Gmail integration | ✅ Active |
| LinkedIn | Social posting | ✅ Active |
| WhatsApp | Messaging | 🚧 In Progress |
| Odoo | Business ERP | ⏳ Planned |
| Social | FB/IG/Twitter | ⏳ Planned |

### MCP Routing

Requests are routed based on action type:

```
email/* → Email MCP
linkedin/* → LinkedIn MCP
whatsapp/* → WhatsApp MCP
odoo/* → Odoo MCP
social/* → Social MCP
```

## Error Handling

### Watcher Errors

- Logged to `logs/watcher_errors.log`
- Auto-retry on network errors
- Email notification on critical failures

### API Errors

- Logged to `logs/api_errors.log`
- Token refresh on 401 errors
- Rate limit handling with backoff

### Task Errors

- Task marked as `error` status
- Error details saved in task file
- Dashboard shows error count

## Reporting

### Daily Reports

Generated at midnight:
- Activity summary
- Tasks completed
- Errors encountered
- System health

### Weekly Reports (Gold Tier)

- Business Audit (`Reports/Business_Audit.md`)
- Accounting Audit (`Reports/Accounting_Audit.md`)
- CEO Brief (`Reports/CEO_Brief.md`)

## Monitoring

### Dashboard

View in `AI_Employee_Vault_Hackathon/Dashboard.md`:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  PERSONAL AI EMPLOYEE - DASHBOARD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STATUS: 🟢 ONLINE

TASKS:
  Needs Action:    3
  In Progress:     2
  Pending Approval: 1
  Approved:        5
  Done:           42

WATCHERS:
  Email:    🟢 Active
  LinkedIn: 🟢 Active
  WhatsApp: 🟡 Inactive
  Files:    🟢 Active

RECENT ACTIVITY:
  ✓ LinkedIn post published
  ✓ Email processed: 5 new
  ⏳ Task awaiting approval

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Scheduling

### Cron Jobs

Use `/schedule` command:

```bash
# Process tasks every hour
/schedule "0 * * * *" /process-tasks

# Daily LinkedIn post
/schedule "0 9 * * *" /linkedin-post

# Weekly audit
/schedule "0 9 * * 0" /weekly-audit
```

## Security

### Credential Management

- Store in `config/` directory
- Never commit to git
- Use environment variables in production
- Rotate tokens regularly

### File Permissions

- Vault: Owner read/write only
- Config: Owner read/write only
- Logs: Group readable

## Troubleshooting

### Watcher Not Starting

```bash
# Check if port is in use
netstat -ano | findstr :8080

# Check logs
cat logs/watcher_errors.log
```

### API Authentication Failed

```bash
# Regenerate OAuth token
python linkedin/oauth_flow.py

# Or for Gmail:
python gmail/oauth_setup.py
```

### Task Not Processing

```bash
# Check task status in Needs_Action folder
# Verify task file has valid YAML frontmatter

# Manually process
/process-tasks --force
```

## Backup & Recovery

### Daily Backup

```bash
# Backup vault
cp -r AI_Employee_Vault_Hackathon backups/vault_$(date +%Y%m%d)

# Backup configs
cp -r config backups/config_$(date +%Y%m%d)
```

### Restore

```bash
# Restore from backup
cp -r backups/vault_20260331 AI_Employee_Vault_Hackathon
```

## Development

### Adding New Skills

1. Create `.claude/skills/your-skill/SKILL.md`
2. Define parameters and expected actions
3. Implement logic in `your-skill/`
4. Test with `/your-skill`

### Adding New Watchers

1. Create `your-service/watcher.py`
2. Implement `Watcher` class with `run()` method
3. Add to main workflow
4. Test with sample data

---

*Last Updated: 2026-03-31*
