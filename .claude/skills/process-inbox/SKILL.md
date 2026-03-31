---
name: process-inbox
description: |
  Process all pending items in the Digital FTE vault's /Needs_Action folder.
  Reads each .md action file, reasons about the required action based on
  Company_Handbook.md rules, takes the appropriate action (or writes an
  approval request), and moves completed items to /Done.
  Use when there are unprocessed items in /Needs_Action.
---

# Process Inbox

Read and process all pending action files in the vault's `/Needs_Action` folder.

## Steps

1. **Read the handbook** — load `AI_Employee_Vault/Company_Handbook.md` to understand the rules of engagement.

2. **Scan /Needs_Action** — list all `.md` files with `status: pending`.

3. **For each pending item:**
   - Read the file to understand the type and content.
   - Apply the appropriate rule from Company_Handbook.md.
   - Decide: auto-handle OR create an approval request.

4. **Auto-handle (safe actions):**
   - File drops → add a summary note, update status to `processed`.
   - Low-priority informational items → summarise and archive.

5. **Approval-required actions (sensitive):**
   - Write `APPROVAL_REQUIRED_<action>_<date>.md` in `/Needs_Action/`.
   - Do NOT execute the action until the file is moved to `/Done/Approved/`.

6. **Move processed items** → move the action file to `/Done/` with a completion timestamp.

7. **Update Dashboard** — call the `update-dashboard` skill after processing.

## Example Usage

```
/process-inbox
```

Or trigger automatically when /Needs_Action is non-empty.

## Rules

- Never delete files — only move them to /Done.
- Log every action taken to `/Logs/YYYY-MM-DD.md`.
- If unsure about an action, always escalate to approval workflow.
- Respect priority levels from Company_Handbook.md.

## Completion Signal

After processing all items, output:
```
<promise>TASK_COMPLETE</promise>
```
