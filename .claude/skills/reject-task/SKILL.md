---
name: reject-task
description: Reject a completed task from Pending_Approval folder
usage: /reject-task [task_name] [reason]
parameters:
  task_name: Optional, specify which task to reject (uses most recent if not provided)
  reason: Optional, reason for rejection
output: Moves task to Rejected folder
---

# Reject Task

Reject a completed task from Pending_Approval folder.

## Usage
/reject-task [task_name] [reason]

## Parameters
- task_name: Optional, specify which task to reject (uses most recent if not provided)
- reason: Optional, reason for rejection

## What it does

1. Reads task from Pending_Approval folder
2. Adds rejection reason to file (if provided)
3. Updates task status to: rejected
4. Moves task to Rejected folder
5. Logs rejection action

## Output
Moves task to Rejected folder

## Task Status Flow

Pending_Approval → Rejected
