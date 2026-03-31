# Claude Code Configuration Notes

## Project Context

This project is building a **Personal AI Employee** for the Bronze Tier of the hackathon.

**Key Decisions Made:**
- Watcher Type: File System Watcher (simpler, no API keys)
- Focus Areas: Both Personal and Business
- User Setup: Obsidian not yet installed - needs installation

---

## Session Goals

This session focused on:
1. ✅ Understanding the Bronze Tier requirements
2. ✅ Clarifying user preferences and constraints
3. ✅ Creating architecture documentation (agent.md)
4. ✅ Creating setup documentation (README.md)
5. ⏳ Next: Implementation of components

---

## Next Steps for Implementation

### 1. Install Obsidian
Download from: https://obsidian.md/download

### 2. Create Vault Structure
**Actual Obsidian Vault Path:** `C:\Users\alvia\OneDrive\Desktop\AI_Employee_Vault_Hackathon`

```bash
mkdir -p AI_Employee_Vault_Hackathon/{Drop,Inbox,Needs_Action,In_Progress,Plans,Pending_Approval,Approved,Rejected,Done,Logs,References}
```

### 3. Create the File System Watcher
Write `watcher.py` that:
- Uses the `watchdog` library
- Monitors the `Drop/` folder
- Creates action files in `Needs_Action/`
- Logs all activity

### 4. Create Agent Skills
Place SKILL.md files in `.claude/skills/`:
- `process-tasks/` - Process all pending tasks
- `create-plan/` - Generate plans for individual tasks
- `update-dashboard/` - Update the dashboard status

### 5. Test the Workflow
1. Drop a test file into `Drop/`
2. Verify watcher creates action file
3. Run `process-tasks` skill
4. Verify plan is created
5. Check dashboard update

---

## Useful Commands

```bash
# Install Python dependencies
pip install watchdog pyyaml

# Run the watcher
python watcher.py

# Vault Path (already configured in watcher.py)
# C:\Users\alvia\OneDrive\Desktop\AI_Employee_Vault_Hackathon
```

---

## Files Created This Session

| File | Purpose | Status |
|------|---------|--------|
| `agent.md` | Architecture and design documentation | ✅ Created |
| `README.md` | Setup and usage guide | ✅ Created |

---

## Agent Skills Structure

To implement Agent Skills, create SKILL.md files:

```
.claude/skills/
├── process-tasks/
│   └── SKILL.md
├── create-plan/
│   └── SKILL.md
└── update-dashboard/
    └── SKILL.md
```

Each SKILL.md should follow the Claude Code Agent Skills format with:
- Description
- Usage examples
- Required parameters
- Expected output

---

## Important Notes

### File System Watcher Pattern
The watcher uses the Observer pattern from the `watchdog` library:
1. Create an `EventHandler` class
2. Define `on_created` method
3. Create an `Observer` and schedule the handler
4. Run in a continuous loop

### Action File Format
Action files use YAML frontmatter for metadata:
```yaml
---
type: file_drop
source: Drop folder
created: 2026-02-27T10:30:00Z
status: pending
file_type: document
---
```

### Obsidian Integration
- Obsidian automatically updates when files change on disk
- Use Obsidian for manual verification and review
- Claude Code can read/write files directly to the vault

---

## Meeting Information

**Weekly Research Meeting**
- **When:** Every Wednesday at 10:00 PM
- **Zoom:** https://us06web.zoom.us/j/87188707642
- **Meeting ID:** 871 8870 7642
- **Passcode:** 744832

---

*Last Updated: 2026-03-27*
