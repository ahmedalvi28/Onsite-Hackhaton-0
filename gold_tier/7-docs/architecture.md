# System Architecture

## Overview

The Personal AI Employee is a multi-tiered autonomous system built on Claude Code, designed to function as a digital Full-Time Equivalent (FTE). The system operates on a local-first architecture with human-in-the-loop verification.

## Core Components

```
┌─────────────────────────────────────────────────────────────────┐
│                         OBSIDIAN VAULT                          │
│              (Task Management & Dashboard)                      │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────┐ │
│  │   Drop   │ │  Tasks   │ │  Plans   │ │ Approved │ │  Done │ │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └───────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      WATCHER LAYER                               │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│  │  Gmail   │ │ LinkedIn │ │ WhatsApp │ │  Files   │            │
│  │ Watcher  │ │ Watcher  │ │ Watcher  │ │ Watcher  │            │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘            │
└───────┼─────────────┼─────────────┼─────────────┼──────────────┘
        │             │             │             │
        └─────────────┴─────────────┴─────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      MCP ROUTER                                  │
│              Routes actions to appropriate servers               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     RALPH WIGWUM LOOP                            │
│              Plan → Execute → Verify → Retry/Complete            │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│  │  Plan    │ │ Execute  │ │ Verify   │ │  Report  │            │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   INTEGRATION SYSTEMS                            │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│  │   Odoo   │ │   Email  │ │  Social  │ │  Audit   │            │
│  │ Community│ │   MCP    │ │  APIs    │ │  System  │            │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      OUTPUTS                                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│  │  Posts   │ │  Reports │ │  Emails  │ │  Actions │            │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘            │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

### Input Collection

1. **Email Watcher** (`gmail/gmail_watcher.py`)
   - Monitors Gmail inbox via API
   - Extracts actionable items
   - Creates task files in `Needs_Action/`

2. **LinkedIn Watcher** (`linkedin/linkedin_watcher.py`)
   - Monitors LinkedIn feed and messages
   - Tracks engagement metrics
   - Generates content suggestions

3. **WhatsApp Watcher** (`whatsapp/whatsapp_watcher.py`)
   - Monitors WhatsApp messages
   - Extracts business-related conversations
   - Creates follow-up tasks

4. **File System Watcher** (`main/watcher.py`)
   - Monitors `Drop/` folder
   - Creates tasks from dropped files
   - Categorizes by file type

### Task Processing Pipeline

```
1. INPUT → Needs_Action/
   ↓
2. ANALYZE → In_Progress/
   ↓
3. PLAN → Plans/
   ↓
4. EXECUTE → Pending_Approval/
   ↓
5. VERIFY → Approved/ OR Rejected/
   ↓
6. ARCHIVE → Done/
```

### MCP Server Architecture

The MCP (Model Context Protocol) layer routes requests to specialized servers:

| MCP Server | Purpose | Port | Endpoints |
|------------|---------|------|-----------|
| Email MCP | Gmail integration | 3000 | `/email/*` |
| LinkedIn MCP | Social posting | 3001 | `/linkedin/*` |
| WhatsApp MCP | Messaging | 3002 | `/whatsapp/*` |
| Odoo MCP | Business ERP | 3003 | `/odoo/*` |
| Social MCP | FB/IG/Twitter | 3004 | `/social/*` |

### Ralph Wigwum Loop

The Ralph Loop is the core reasoning engine that handles multi-step tasks:

```
┌─────────────┐
│  Receive    │
│   Task      │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Analyze    │  → Break down into steps
│  Task       │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Generate   │  → Create step-by-step plan
│   Plan      │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Execute    │  → Perform each step
│   Steps     │
└──────┬──────┘
       │
       ▼
┌─────────────┐    ┌─────────────┐
│  Verify     │──NO→│    Retry    │
│   Result    │    │   Adjust     │
└──────┬──────┘    └──────┬──────┘
       │                  │
      YES                 │
       │                  │
       ▼                  │
┌─────────────┐           │
│  Complete   │◄──────────┘
│   Task      │
└─────────────┘
```

## File Structure

```
Onsite-Hackhaton-0/
├── main/                          # Core components
│   ├── watcher.py                 # File system watcher
│   ├── base_watcher.py            # Base watcher class
│   ├── requirements.txt           # Python dependencies
│   ├── agent.md                   # Architecture documentation
│   └── credentials.json           # Service credentials
│
├── gmail/                         # Gmail integration
│   ├── gmail_watcher.py           # Email watcher
│   └── oauth_setup.py             # OAuth setup
│
├── linkedin/                      # LinkedIn integration
│   ├── auto_post.py               # Selenium auto poster
│   ├── api_post.py                # API-based poster
│   ├── linkedin_watcher.py        # LinkedIn watcher
│   ├── oauth_flow.py              # OAuth token generator
│   └── find_member_id.py          # Member ID finder
│
├── whatsapp/                      # WhatsApp integration
│   ├── whatsapp_watcher.py        # WhatsApp watcher
│   └── client.py                  # WhatsApp client
│
├── email/                         # Email MCP server
│   ├── server.py                  # MCP server
│   └── handlers/                  # Email handlers
│
├── gold_tier/                     # Gold Tier features
│   ├── 1-odoo/                    # Odoo integration
│   ├── 2-social/                  # Social media
│   ├── 3-twitter/                 # Twitter integration
│   ├── 4-integration/             # MCP routing
│   ├── 5-ralph/                   # Ralph Loop
│   ├── 6-audit/                   # Audit system
│   └── 7-docs/                    # Documentation
│
├── config/                        # Configuration files
│   ├── gmail_config.yaml          # Gmail settings
│   ├── linkedin_config.yaml       # LinkedIn settings
│   └── email_config.yaml          # Email MCP settings
│
├── logs/                          # Log files
│   ├── watcher_errors.log         # Watcher errors
│   ├── api_errors.log             # API errors
│   └── system.log                 # System logs
│
├── .claude/                       # Claude Code configuration
│   └── skills/                    # Agent skills
│
└── AI_Employee_Vault_Hackathon/   # Obsidian vault
    ├── Dashboard.md               # Status dashboard
    ├── Drop/                      # Input folder
    ├── Needs_Action/              # Pending tasks
    ├── In_Progress/               # Active tasks
    ├── Plans/                     # Generated plans
    ├── Pending_Approval/          # Awaiting review
    ├── Approved/                  # Approved actions
    ├── Rejected/                  # Rejected actions
    ├── Done/                      # Completed tasks
    ├── Logs/                      # Activity logs
    └── Reports/                   # Generated reports
```

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Core Engine | Claude Code | AI reasoning and planning |
| Dashboard | Obsidian | Task management and visualization |
| Email API | Gmail API | Email monitoring and processing |
| Social API | LinkedIn Marketing API | Social media posting |
| Business ERP | Odoo Community | Accounting and business management |
| Watchers | Python + watchdog | File and API monitoring |
| MCP Layer | Model Context Protocol | Service routing |
| OAuth 2.0 | Standard OAuth | Authentication for APIs |
| Selenium | Browser automation | Fallback for posting |

## Security Model

### Credential Storage

- Stored in `config/` directory
- YAML format for easy configuration
- Never committed to version control
- Encrypted in production environments

### Authentication Flow

1. OAuth 2.0 for external APIs
2. Service accounts for background processes
3. Token refresh on expiration (60 days)
4. Human approval for sensitive actions

### Data Protection

- Local-first architecture (data stays on device)
- No cloud storage for sensitive information
- Obsidian vault for task management
- Encrypted credentials in production

## Performance Considerations

### Concurrency

- Watchers run in separate processes
- MCP servers handle multiple concurrent requests
- Ralph Loop processes tasks sequentially (per task)

### Rate Limiting

- API requests include rate limit handling
- Exponential backoff for retries
- Request queuing for high-volume periods

### Error Recovery

- Automatic retry on transient errors
- Graceful degradation on service failures
- Human notification for critical errors

---

*Architecture Documentation | Gold Tier*
