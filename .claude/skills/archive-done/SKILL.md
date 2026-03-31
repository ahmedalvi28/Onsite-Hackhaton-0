---
name: archive-done
description: Archive approved tasks to Done folder for permanent storage
usage: /archive-done [task_name]
parameters:
  task_name: Optional, specify which task to archive (archives all if not provided)
output: Moves tasks from Approved to Done folder
---

# Archive Done

Archive approved tasks to Done folder for permanent storage.

## Usage
/archive-done [task_name]

## Parameters
- task_name: Optional, specify which task to archive (archives all if not provided)

## What it does

1. Reads task(s) from Approved folder
2. Updates task status to: done
3. Moves task(s) to Done folder
4. Logs archive action

## Output
Moves tasks from Approved to Done folder

## Task Status Flow

Approved → Done

## Notes

- Run this skill to clean up Approved folder after tasks are verified
- If no task_name provided, archives all approved tasks
