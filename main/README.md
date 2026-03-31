# Personal AI Employee - Bronze Tier

Your own autonomous AI assistant that manages personal and business tasks locally-first.

> **Tagline:** Your life and business on autopilot. Local-first, agent-driven, human-in-the-loop.

---

## Overview

This project builds a **Digital FTE (Full-Time Equivalent)** - an AI agent that functions like a human employee, proactively managing tasks using Claude Code as the reasoning engine and Obsidian as the management dashboard.

**Current Document:** Bronze (Foundation)
**Build Time:** 8-12 hours
**Watcher Type:** File System (no API keys required)

> **Next Tier:** See [README-SILVER.md](./README-SILVER.md) for Silver Tier features

---

## Quick Start

### 1. Prerequisites

Install the following software:

| Component | Download Link |
|-----------|---------------|
| [Obsidian](https://obsidian.md/download) | https://obsidian.md/download |
| [Python](https://www.python.org/downloads/) | https://www.python.org/downloads/ (3.13+) |
| [Claude Code](https://claude.com/product/claude-code) | https://claude.com/product/claude-code |

### 2. Setup Project

```bash
# Create vault folder
mkdir AI_Employee_Vault

# Create folder structure
mkdir -p AI_Employee_Vault/{Drop,Needs_Action,In_Progress,Plans,Pending_Approval,Approved,Rejected,Done,Logs}
```

### 3. Install Dependencies

```bash
pip install watchdog
```

### 4. Initialize Obsidian Vault

1. Open Obsidian
2. Click "Create new vault"
3. Name it `AI_Employee_Vault`
4. Select the folder you created above
5. Obsidian will open the empty vault

### 5. Start the Watcher

```bash
python watcher.py --vault-path ./AI_Employee_Vault
```

The watcher will now monitor the `/Drop` folder and create action files automatically.

---

## How It Works

```
User drops file → Watcher detects → Creates task → User processes → Done
     ↓                  ↓               ↓            ↓
  Drop/           Needs_Action/      Plans/      Done/
```

### Step by Step:

1. **Drop a file** into `Drop/` folder
2. **Watcher** detects the file and creates a task in `Needs_Action/`
3. **User** invokes `/process-tasks` in Claude Code
4. **Claude** analyzes the file and creates a plan
5. **User** reviews and approves the plan
6. **Claude** executes the plan and moves task to `Done/`

---

## Vault Structure

```
AI_Employee_Vault/
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
└── Logs/                     # Activity logs
```

---

## Claude Code Skills

### Available Skills

| Skill | Description | Usage |
|-------|-------------|--------|
| `process-tasks` | Process all pending tasks | `/process-tasks` |
| `create-plan` | Generate plan for a task | `/create-plan` |
| `execute-task` | Execute task based on plan | `/execute-task` |
| `update-dashboard` | Update dashboard stats | `/update-dashboard` |
| `approve-task` | Approve completed tasks | `/approve-task` |
| `reject-task` | Reject tasks | `/reject-task` |
| `archive-done` | Archive approved tasks | `/archive-done` |

---

## Dashboard.md Template

```markdown
---
last_updated: 2026-02-27T10:30:00Z
---

# Personal AI Employee Dashboard

## Quick Stats
| Metric | Value |
|--------|-------|
| Tasks Today | 0 |
| Pending | 0 |
| In Progress | 0 |
| Completed | 0 |
| Last Updated | 2026-02-27 10:30:00 |

## Pending Actions
*No pending actions*

## Recent Activity
*Welcome to your Personal AI Employee!*
```

---

## Company_Handbook.md Template

```markdown
---
version: 1.0
last_updated: 2026-02-27
---

# Company Handbook

## Task Processing Rules

**Auto-Process (No review needed):**
- Meeting notes
- Quick reminders
- Todo lists
- Shopping lists

**Requires Review:**
- Invoices
- Contracts
- Legal documents
- Payment requests

## File Handling
- Never delete files without explicit instruction
- Always move files to appropriate folders
- Create metadata for all processed files
```

---

## Project Structure

```
Onsite-Hackhaton-0/
├── README.md                      # This file
├── agent.md                       # Architecture documentation
├── watcher.py                     # File System Watcher
├── claude-code-skills-lab-main/   # Skills Lab
│   └── .claude/skills/
│       ├── process-tasks/         # Process all pending tasks
│       ├── create-plan/           # Generate plan for a task
│       ├── execute-task/          # Execute task based on plan
│       ├── update-dashboard/      # Update dashboard stats
│       ├── approve-task/          # Approve completed tasks
│       ├── reject-task/           # Reject tasks
│       └── archive-done/          # Archive approved tasks
└── AI_Employee_Vault/            # Obsidian vault
```

---

## Troubleshooting

### Watcher Not Detecting Files
- Ensure the watcher script is running
- Check that the vault path is correct
- Verify file permissions

### Claude Code Not Reading Files
- Ensure Claude Code is running from the correct directory
- Check file permissions on the vault folder

### Obsidian Files Not Updating
- Refresh the Obsidian app (Ctrl+R)
- Check that you're looking at the correct vault

---

## Features

| Feature | Description |
|---------|-------------|
| Local Knowledge Base | Obsidian vault stores all data on your machine |
| File System Watcher | Monitor a drop folder for new files automatically |
| Task Processing | Claude Code analyzes and processes incoming files |
| Status Dashboard | Real-time view of all tasks and activities |
| Agent Skills | All AI functionality as reusable Claude Code skills |

---

## Future Improvements

| Feature | Status |
|---------|--------|
| Gmail integration | Planned (Silver Tier) |
| WhatsApp integration | Planned (Silver Tier) |
| Email/Calendar MCP | Planned (Silver Tier) |
| Desktop notifications | Planned |
| Auto-processing for simple tasks | Planned |

---

## Meeting Information

**Weekly Research Meeting**
- **When:** Every Wednesday at 10:00 PM
- **Zoom:** https://us06web.zoom.us/j/87188707642
- **Meeting ID:** 871 8870 7642
- **Passcode:** 744832

---

## Resources

- [Requirements Document](./requirments.md) - Full hackathon spec
- [Architecture Documentation](./agent.md) - Detailed architecture
- [Claude Code Documentation](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Obsidian Documentation](https://help.obsidian.md/)

---

## Contributing

This is a personal project for the Personal AI Employee Hackathon.

**Submission Form:** [https://forms.gle/JR9T1SJq5rmQyGkGA](https://forms.gle/JR9T1SJq5rmQyGkGA)

---

*Built with Claude Code & Obsidian | Personal AI Employee Hackathon 2026*
