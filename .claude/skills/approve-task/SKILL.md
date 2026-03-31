---
description: Handle human-in-the-loop approval workflow for sensitive actions
---

# Approve Task Skill

## Description
Manages the approval workflow for plans that require human review before execution.

## Usage
Use this skill when:
- A plan has been created and needs approval
- A task is in Pending_Approval folder
- Human needs to review and approve/reject a sensitive action

## Parameters
- `plan_file`: Path to the plan file in Plans or Pending_Approval folder
- `action`: "approve", "reject", or "request-changes"
- `comments`: Optional feedback for rejection or changes

## Expected Actions

1. **Read the plan file** to understand the proposed action
2. **Assess sensitivity** - Does this require human approval?
   - Actions involving: sending emails, posting on LinkedIn, financial transactions, sensitive data
   - Always require approval for these

3. **For sensitive actions**:
   - Move plan to Pending_Approval folder
   - Create approval request file with summary
   - Wait for human decision

4. **When human responds**:
   - **Approve**: Move to Approved folder, mark as ready for execution
   - **Reject**: Move to Rejected folder, log reason
   - **Request Changes**: Keep in Plans folder, add comments

## Approval Request Format

```markdown
---
type: approval_request
plan_id: PLAN_ID
created: TIMESTAMP
status: awaiting_approval
---

# Approval Request: [Plan Title]

## Summary
[Brief description of what will be done]

## Action Type
- [ ] Send Email
- [ ] Post on LinkedIn
- [ ] Financial Transaction
- [ ] Other: ______

## Risk Assessment
- [ ] Low risk - Routine action
- [ ] Medium risk - Requires review
- [ ] High risk - Requires explicit approval

## Details of Action
[What will happen when this is executed]

## Approve Options
1. **Approve** - Execute as planned
2. **Reject** - Cancel this action
3. **Request Changes** - Send back for modification

---
*Awaiting your approval*
```

## User Response Format

When responding to an approval request:

```
approve - Proceed with the plan
reject - Cancel the plan, reason: [reason]
changes - Request these changes: [changes]
```

## Example

User: /approve-task Plans/PLAN_EMAIL_1234.md approve

Response: "Plan PLAN_EMAIL_1234 approved. Moved to Approved folder and ready for execution."
