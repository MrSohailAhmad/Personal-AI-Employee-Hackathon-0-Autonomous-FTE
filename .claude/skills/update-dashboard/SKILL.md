---
name: update-dashboard
description: |
  Update the AI_Employee_Vault/Dashboard.md with the current system status.
  Reads /Needs_Action, /Done, and /Logs to produce a live summary of:
  pending items, completed items today, and watcher status.
  Use after processing tasks or on demand to refresh the dashboard.
---

# Update Dashboard

Refresh `AI_Employee_Vault/Dashboard.md` with the current vault status.

## Steps

1. **Count pending items** — list all `.md` files in `/Needs_Action/` with `status: pending`.

2. **Count completions today** — list all `.md` files in `/Done/` modified today.

3. **Read today's log** — load `/Logs/YYYY-MM-DD.md` (today's date) for recent events.

4. **Rewrite the Dashboard** — update `Dashboard.md` with:
   - Status table (Inbox, Needs Action, Watcher)
   - List of pending items (file name + type + priority)
   - List of items completed today
   - Last 5 log events

5. **Preserve manual notes** — keep any content below the `## Notes` heading unchanged.

## Dashboard Format

```markdown
# AI Employee Dashboard

---
last_updated: <ISO timestamp>
generated_by: AI Employee v0.1
---

## Status Overview
| Area | Status | Count |
|------|--------|-------|
| Needs Action | 🟡 | N items |
| Done Today | ✅ | N items |

## Pending Items
- FILE_report_20260401.md (file_drop, normal)

## Done Today
- FILE_invoice_20260401.md ✅

## Recent Activity (last 5)
- ...

## Notes
<preserved manual content>
```

## Example Usage

```
/update-dashboard
```

## Completion Signal

Output after finishing:
```
<promise>TASK_COMPLETE</promise>
```
