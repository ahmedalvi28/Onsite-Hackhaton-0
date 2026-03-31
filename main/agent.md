# Personal AI Employee - Bronze Tier Architecture

## Project Summary

Building a Personal AI Employee (Digital FTE) that autonomously manages personal and business tasks.

| Attribute | Value |
|-----------|-------|
| **Tier** | Bronze (Foundation) |
| **Watcher** | File System Watcher |
| **Focus** | Personal & Business |
| **Status** | Planning Phase |

---

## Overview

This document describes the architecture for building a Personal AI Employee at the Bronze Tier level - a minimum viable deliverable that demonstrates the core concepts of autonomous task processing.

**Target Tier:** Bronze (Foundation)
**Estimated Build Time:** 8-12 hours
**Primary Watcher:** File System Watcher
**Focus Areas:** Personal & Business

---

## System Vision

A Personal AI Employee is an autonomous agent that monitors inputs, processes tasks, and maintains a persistent knowledge base. The Bronze Tier focuses on:

1. **Local-first architecture** using Obsidian as the knowledge base and GUI
2. **File System Watcher** as the primary input mechanism (no API keys required)
3. **Claude Code** as the reasoning engine
4. **Agent Skills** for implementing AI functionality

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    PERSONAL AI EMPLOYEE (BRONZE)                 │
└─────────────────────────────────────────────────────────────────┘

                              EXTERNAL INPUT
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                   PERCEPTION LAYER                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              File System Watcher (Python)                │  │
│  │  Monitors /Drop folder for new files                     │  │
│  │  Creates action files in /Needs_Action                    │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│              OBSIDIAN VAULT (Local Knowledge Base)              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ /Drop/    │ /Needs_Action/  │ /Done/  │ /Plans/          │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │ Dashboard.md    │ Company_Handbook.md                    │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                   REASONING LAYER                                │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                      CLAUDE CODE                           │ │
│  │   Read Files → Analyze → Create Plans → Write Results     │ │
│  │   (Implemented as Agent Skills)                           │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                   ACTION LAYER                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │            File System Operations                         │  │
│  │  Move files between folders, update status, write logs   │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Specifications

### 1. Obsidian Vault Structure

The vault serves as both as GUI and long-term memory. Create this folder structure:

```
AI_Employee_Vault/
├── Dashboard.md              # Main status dashboard
├── Company_Handbook.md       # Rules and guidelines
├── Drop/                     # Drop zone for new files
├── Inbox/                    # Incoming items (processed by watcher)
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

### 2. File System Watcher (Python)

A background process that monitors the `/Drop` folder for new files.

**Features:**
- Monitors for file creation events
- Creates action files with metadata
- Supports multiple file types (documents, images, audio)
- Generates markdown files for each dropped item

**Output Format:**
```markdown
---
type: file_drop
source: Drop folder
created: 2026-02-27T10:30:00Z
status: pending
file_type: [document|image|audio|other]
---

# FILE_<filename>

Original file dropped for processing.

**File Details:**
- Original Name: `<filename>`
- Size: `<size>`
- File Type: `<type>`
- Dropped At: `<timestamp>`

## Suggested Actions
- [ ] Analyze content
- [ ] Categorize (Personal/Business)
- [ ] Extract key information
- [ ] Create action plan
```

---

### 3. Claude Code Integration

Claude Code will operate as the reasoning engine through Agent Skills.

**Agent Skills to Implement:**

| Skill Name | Description | Trigger |
|------------|-------------|---------|
| `process-tasks` | Process all files in /Needs_Action | Manual command |
| `create-plan` | Generate a Plan.md for a task | Called by process-tasks |
| `execute-task` | Execute task based on plan | Called by process-tasks |
| `update-dashboard` | Update Dashboard.md with status | After task completion |
| `approve-task` | Approve completed tasks from Pending_Approval/ | Manual command |
| `reject-task` | Reject tasks from Pending_Approval/ | Manual command |
| `archive-done` | Archive approved tasks to Done/ | Manual command |

---

### 4. Dashboard.md Template

```markdown
---
last_updated: 2026-02-27T10:30:00Z
employee_name: My AI Employee
status: active
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

## In Progress
*No tasks in progress*

## Recent Activity
*Welcome to your Personal AI Employee!*

---

## Personal Focus Areas
- [ ] Inbox Management
- [ ] Calendar Scheduling
- [ ] Personal Notes

## Business Focus Areas
- [ ] Lead Capture
- [ ] Document Processing
- [ ] Task Management
```

---

### 5. Company_Handbook.md Template

```markdown
---
version: 1.0
last_updated: 2026-02-27
---

# Company Handbook

## Employee Guidelines

### Communication Style
- Be polite and professional
- Use clear, concise language
- Ask for clarification when uncertain
- Always identify as an AI assistant

### Task Processing Rules
1. **Classification**: Personal or Business
2. **Priority**: Important tasks first
3. **Approval**: All actions require review before execution

### Auto-Processing Rules

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
- External communications

### File Handling
- Never delete files without explicit instruction
- Always move files to appropriate folders
- Create metadata for all processed files
```

---

## Implementation Plan

### Phase 1: Foundation (This Week)

| Task | Status | Effort |
|------|--------|--------|
| Obsidian vault structure | ✅ Done | 1 hour |
| Basic watcher.py | ⏳ Pending | 2 hours |
| Dashboard template | ✅ Done | 30 min |
| Company Handbook template | ✅ Done | 30 min |
| Basic Agent Skills | ⏳ Pending | 3 hours |
| End-to-end testing | ⏳ Pending | 2 hours |

**Total:** ~9 hours

---

## Simple Workflow

```
1. User drops file into Drop/
       │
       ▼
2. Watcher detects file
       │
       ▼
3. Watcher creates action file in Needs_Action/
       │
       ▼
4. User invokes: /process-tasks
       │
       ▼
5. Claude reads and analyzes the file
       │
       ▼
6. Claude creates Plan.md
       │
       ▼
7. User reviews and approves plan
       │
       ▼
8. Claude executes plan
       │
       ▼
9. Task moved to Done/
       │
       ▼
10. Dashboard updated
```

---

## Project Structure

```
Onsite-Hackhaton-0/
├── README.md                      # This file
├── agent.md                       # Architecture documentation
├── Claude.md                      # Claude-specific notes
├── requirments.md                # Full hackathon requirements
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
└── AI_Employee_Vault/            # Obsidian vault (create this)
    ├── Dashboard.md
    ├── Company_Handbook.md
    ├── Drop/
    ├── Needs_Action/
    ├── In_Progress/
    ├── Plans/
    ├── Pending_Approval/
    ├── Approved/
    ├── Rejected/
    ├── Done/
    └── Logs/
```

---

## Quick Start

### 1. Setup Vault

```bash
mkdir AI_Employee_Vault
cd AI_Employee_Vault
mkdir -p {Drop,Needs_Action,In_Progress,Plans,Pending_Approval,Approved,Rejected,Done,Logs}
```

### 2. Install Dependencies

```bash
pip install watchdog
```

### 3. Start Watcher

```bash
python watcher.py --vault-path ./AI_Employee_Vault
```

### 4. Test It

Drop a file into `Drop/` folder and check `Needs_Action/` for the task file.

---

## Meeting Information

**Weekly Research Meeting**
- **When:** Every Wednesday at 10:00 PM
- **Zoom:** https://us06web.zoom.us/j/87188707642
- **Meeting ID:** 871 8870 7642
- **Passcode:** 744832

---

*Last Updated: 2026-02-27*
*Bronze Tier - Simple Foundation*
