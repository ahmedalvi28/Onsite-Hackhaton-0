# AI Employee - Workflow

**File Drop, Review, Approve, Execute**

---

## Quick Reference

| Step | Who | Action |
|------|-----|--------|
| 1. Start System | User | `python watcher.py` |
| 2. Drop File | User | File drop in Drop/ |
| 3. Create Task | AI (Auto) | Task in Needs_Action/ |
| 4. User Review | User | Review task in Obsidian |
| 5. User Approve | User | Run `/process-tasks` |
| 6. Execute | AI | Process and complete |
| 7. Update Dashboard | AI | Auto update |

---

## Complete Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                         USER ACTION                         │
├─────────────────────────────────────────────────────────────┤
│ 1. Start watcher                                           │
│    python watcher.py --vault-path ./AI_Employee_Vault      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                         USER ACTION                         │
├─────────────────────────────────────────────────────────────┤
│ 2. Drop file into Drop/ folder                            │
│    Example: "invoice.pdf", "notes.md", "todo.txt"         │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                         AUTOMATIC                           │
├─────────────────────────────────────────────────────────────┤
│ 3. Watcher detects file                                    │
│    - Creates task in Needs_Action/                         │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                         USER ACTION                         │
├─────────────────────────────────────────────────────────────┤
│ 4. Review task in Obsidian                                 │
│    - Open Needs_Action/ folder                              │
│    - Read the task file                                    │
│    - Check the suggested actions                           │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                         USER ACTION                         │
├─────────────────────────────────────────────────────────────┤
│ 5. Run: /process-tasks                                     │
│    (in Claude Code)                                        │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                         AUTOMATIC                           │
├─────────────────────────────────────────────────────────────┤
│ 6. AI processes task                                       │
│    - Reads file content                                     │
│    - Creates Plan.md in Plans/                             │
│    - Executes the plan                                      │
│    - Moves task to Done/                                   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                         AUTOMATIC                           │
├─────────────────────────────────────────────────────────────┤
│ 7. Update Dashboard.md                                     │
│    - Task counts update hote hain                           │
│    - Recent activity add hoti hai                           │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
                    ✅ TASK COMPLETE

                    
```

---

## Folder Transitions

```
Drop/ → Needs_Action/ → In_Progress/ → Done/
                                    ↓
                               Rejected/
```

---

## Example

### Setup (Once per day)

```bash
$ python watcher.py --vault-path ./AI_Employee_Vault
✅ Watcher started - monitoring Drop/ folder...
```

### Task Processing

```bash
1. [User] Drop "invoice_jan.pdf" into Drop/
2. [AI]   Task created in Needs_Action/
3. [User] Open Obsidian, review task
4. [User] Run: /process-tasks
5. [AI]   Invoice summarized and saved
6. [AI]   Moved to Done/
7. [AI]   Dashboard updated

✅ Done!
```

---

## What User Does

| # | Action |
|---|--------|
| 1 | Start watcher |
| 2 | Drop files |
| 3 | Review tasks |
| 4 | Run /process-tasks |

---

## What AI Does

| # | Action |
|---|--------|
| 1 | Detect files |
| 2 | Create tasks |
| 3 | Analyze content |
| 4 | Make plans |
| 5 | Execute tasks |
| 6 | Update status |
| 7 | Update dashboard |
| 8 | Log activity |

---

## Skills

| Skill | Trigger | Does What |
|-------|---------|-----------|
| `/process-tasks` | User command | Reads tasks, creates plans, executes, updates dashboard |
| `/create-plan` | Called by process-tasks | Generates detailed plan |
| `/execute-task` | Called by process-tasks | Executes task based on plan |
| `/update-dashboard` | Auto after completion | Updates dashboard stats |
| `/approve-task` | User command | Approves completed tasks from Pending_Approval/ |
| `/reject-task` | User command | Rejects tasks from Pending_Approval/ |
| `/archive-done` | User command | Archives approved tasks to Done/ |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Task not creating | Check watcher is running |
| Task stuck in Needs_Action | Run `/process-tasks` |
| Dashboard not updating | Check Logs/ for errors |
| File not processed | Verify file is supported format |

---

**File Drop → Review → Approve → Execute → Done**
