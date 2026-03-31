---
name: start-file-watcher
description: |
  Start or stop the Digital FTE file system watcher that monitors the
  AI_Employee_Vault/Inbox folder. When a file is dropped into Inbox,
  the watcher automatically creates an action file in /Needs_Action.
  Use to launch the watcher in the background or check its status.
---

# Start File Watcher

Manage the filesystem watcher (`watchers/filesystem_watcher.py`).

## Setup (first time)

Install dependencies with uv:

```bash
uv sync
```

## Start Watcher

```bash
# Normal mode (processes real files)
uv run python watchers/filesystem_watcher.py --vault AI_Employee_Vault

# Dry-run mode (safe for testing — logs without moving files)
DRY_RUN=true uv run python watchers/filesystem_watcher.py --vault AI_Employee_Vault

# Custom vault path
uv run python watchers/filesystem_watcher.py --vault /path/to/your/vault
```

## Start in Background

```bash
uv run python watchers/filesystem_watcher.py --vault AI_Employee_Vault &
echo "Watcher PID: $!"
```

## Stop Watcher

```bash
# If running in foreground: Ctrl+C
# If running in background:
pkill -f "filesystem_watcher.py"
```

## Test It

1. Start the watcher.
2. Drop any file into `AI_Employee_Vault/Inbox/`.
3. Check `AI_Employee_Vault/Needs_Action/` — a new `FILE_<name>_<timestamp>.md` should appear.
4. Check `AI_Employee_Vault/Logs/<today>.md` for the log entry.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: watchdog` | Run `uv sync` first |
| No action file created | Check Inbox path, ensure watcher is running |
| Permission denied | Check folder permissions |
| Files not detected | Ensure files are fully written before checking |

## Completion Signal

Output after starting successfully:
```
<promise>TASK_COMPLETE</promise>
```
