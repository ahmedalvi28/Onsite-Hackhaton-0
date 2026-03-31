---
name: execute-task
description: Execute a task based on its execution plan
usage: /execute-task [task_name]
parameters:
  task_name: Optional, specify which task to execute (uses most recent if not provided)
output: Completes task and moves to Pending_Approval
---

# Execute Task

Execute a task based on its execution plan.

## Usage
/execute-task [task_name]

## Parameters
- task_name: Optional, specify which task to execute (uses most recent if not provided)

## What it does

1. Reads the task from Needs_Action or In_Progress
2. Reads the corresponding plan from Plans
3. Executes the plan steps
4. Generates output
5. Moves task to Pending_Approval folder
6. Updates task status to: pending_approval

## Output
Completes task and moves to Pending_Approval

## Task Status Flow

Needs_Action → In_Progress → Pending_Approval
