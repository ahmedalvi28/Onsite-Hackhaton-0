# Personal AI Employee - Gold Tier

Your own autonomous AI assistant that manages personal and business tasks locally-first with full business integration.

> **Tagline:** Your life and business on autopilot. Local-first, agent-driven, human-in-the-loop.

---

## Overview

This project builds a **Digital FTE (Full-Time Equivalent)** - an AI agent that functions like a human employee, proactively managing tasks using Claude Code as reasoning engine and Obsidian as management dashboard.

**Current Document:** Gold (Autonomous Employee)
**Build Time:** 40+ hours
**Integration:** Full cross-domain (Personal + Business)

---

## Tiers Progress

| Tier | Status | Key Features |
|-------|--------|--------------|
| **Bronze** | ✅ Complete | File System Watcher, Basic task processing |
| **Silver** | ✅ Complete | Gmail, LinkedIn, WhatsApp, Email MCP |
| **Gold** | 🚧 In Progress | Odoo, FB, IG, Twitter, Ralph Loop, Audit |

---

## Gold Tier Requirements

### Completed (Silver)
- [x] File System Watcher
- [x] Gmail watcher and integration
- [x] LinkedIn auto-posting (working)
- [x] Email MCP server
- [x] Folder organization structure

### New (Gold)
- [ ] Odoo Community integration (self-hosted)
- [ ] Facebook integration (post + summary)
- [ ] Instagram integration (post + summary)
- [ ] Twitter (X) integration (post + summary)
- [ ] Multiple MCP servers (routing)
- [ ] Weekly Business & Accounting Audit
- [ ] CEO Briefing generation
- [ ] Error recovery system
- [ ] Ralph Wigwum loop (multi-step)
- [ ] Comprehensive audit logging
- [ ] Architecture documentation

---

## Quick Start

### 1. Project Structure

```
Onsite-Hackhaton-0/
├── main/                    # Core files
│   ├── watcher.py, base_watcher.py
│   ├── README.md, agent.md
│   └── credentials.json, token.json
├── gmail/                   # Gmail integration
├── linkedin/                 # LinkedIn (auto_post.py working!)
├── whatsapp/                  # WhatsApp
├── email/                    # Email MCP
├── gold_tier/                # 🆕 Gold Tier
│   ├── 1-odoo/           # Odoo integration
│   ├── 2-social/          # Social media
│   ├── 3-twitter/          # Twitter
│   ├── 4-integration/      # MCP routing
│   ├── 5-ralph/           # Ralph Loop
│   ├── 6-audit/            # Audit system
│   └── 7-docs/             # Documentation
├── config/                   # All configs
└── logs/                     # Log files
```

### 2. Complete LinkedIn Automation

```bash
# Post daily content
python linkedin/linkedin_automation.py --post

# Monitor notifications
python linkedin/linkedin_automation.py --monitor

# Accept connection requests
python linkedin/linkedin_automation.py --accept

# Run everything
python linkedin/linkedin_automation.py --full

# Run with scheduler (continuous)
python linkedin/linkedin_scheduler.py

# Setup Windows Task Scheduler (run as admin)
linkedin/setup_linkedin_scheduler.bat
```

✅ **Features:**
- Auto-post daily content (rotates by topic)
- Monitor notifications/messages
- Auto-accept connections
- Create Obsidian tasks
- Full documentation: `linkedin/LINKEDIN_AUTOMATION_README.md`

### 3. Gold Tier Progress

See `gold_tier/README.md` for detailed progress.

---

## How It Works (Gold Tier)

```
                    EXTERNAL INPUTS
                    ↓
          ┌─────────────────┬──────────────┐
          │                 │              │
    Email     LinkedIn      Facebook     Instagram     Twitter
      │          │            │              │            │
      ↓          ↓            ↓              ↓            ↓
┌──────────┴──────┴─────────────┴────────────┴──────────────┐
│                   MCP ROUTER LAYER                   │
│  ┌─────────────────────────────────────────────────┐ │
│  │      Routes to appropriate MCP server          │ │
│  └─────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────┐
│                   RALPH LOOP                       │
│  Multi-step autonomous task completion                │
│  Plan → Execute → Verify → Retry/Complete       │
└──────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────┐
│                   SYSTEMS                         │
│  ┌───────────┬───────────┬───────────┐  │
│  │    Odoo    │   Audit     │  Social    │  │
│  │ Community  │   System    │  Integration │  │
│  └───────────┴───────────┴───────────┘  │
└──────────────────────────────────────────────────────┘
                          ↓
                    CEO BRIEFS & REPORTS
```

---

## Claude Code Skills

### Bronze Skills (Complete)
| Skill | Description | Usage |
|--------|-------------|--------|
| `process-tasks` | Process all pending tasks | `/process-tasks` |
| `create-plan` | Generate plan for a task | `/create-plan` |
| `update-dashboard` | Update dashboard stats | `/update-dashboard` |
| `approve-task` | Approve completed tasks | `/approve-task` |
| `reject-task` | Reject tasks | `/reject-task` |
| `archive-done` | Archive approved tasks | `/archive-done` |

### Gold Skills (Planned)
| Skill | Description |
|--------|-------------|
| `odoo-invoice` | Create invoice in Odoo |
| `odoo-report` | Get accounting data |
| `social-post-fb` | Post to Facebook |
| `social-post-ig` | Post to Instagram |
| `social-post-x` | Post to Twitter |
| `social-summary` | Generate social summary |
| `weekly-audit` | Generate audit report |
| `ceo-briefing` | Generate CEO brief |

---

## Vault Structure

```
AI_Employee_Vault_Hackathon/
├── Dashboard.md              # Main status dashboard
├── Company_Handbook.md       # Rules and guidelines
├── Drop/                     # Drop zone for new files
├── Needs_Action/             # Tasks requiring attention
├── In_Progress/              # Currently processing tasks
├── Plans/                    # Generated plans for tasks
├── Pending_Approval/         # Items awaiting human review
├── Approved/                 # Approved actions
├── Rejected/                 # Rejected actions
├── Done/                     # Completed tasks
├── Logs/                     # Activity logs
└── Reports/                  # Weekly reports (Gold)
    ├── Business_Audit.md
    ├── Accounting_Audit.md
    └── CEO_Brief.md
```

---

## Gold Tier - Key Features

### 1. Odoo Community Integration
- Self-hosted Odoo 19+ (Community Edition)
- JSON-RPC MCP server
- Accounting data sync
- Invoice generation
- Journal entries

### 2. Social Media Integration
- **Facebook:** Page posts + engagement summary
- **Instagram:** Media posts + engagement summary
- **Twitter (X):** Tweets + engagement summary
- All via respective APIs

### 3. Multiple MCP Servers
- Routing layer for different action types
- Load balancing
- Error recovery
- Graceful degradation

### 4. Ralph Wigwum Loop
- Multi-step task planning
- Sequential execution
- Self-correction
- Audit logging for each step

### 5. Audit & Reporting
- Weekly Business Audit
- Weekly Accounting Audit
- CEO Brief generation
- Comprehensive logging
- Error tracking

---

## Resources

- [Requirements Document](./main/requirements.txt)
- [Architecture Documentation](./main/agent.md)
- [Gold Tier Plan](./gold_tier/SUBMISSION.md)
- [Claude Code Documentation](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Obsidian Documentation](https://help.obsidian.md/)

---

## Meeting Information

**Weekly Research Meeting**
- **When:** Every Wednesday at 10:00 PM
- **Zoom:** https://us06web.zoom.us/j/87188707642
- **Meeting ID:** 871 8870 7642
- **Passcode:** 744832

---

## Submission

**Submission Form:** [https://forms.gle/JR9T1SJq5rmQyGkGA](https://forms.gle/JR9T1SJq5rmQyGkGA)

---

*Built with Claude Code & Obsidian | Personal AI Employee - Gold Tier* | Updated: 2026-03-31*
