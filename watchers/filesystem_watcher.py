"""
File System Watcher — monitors the /Inbox drop folder.

Any file dropped into AI_Employee_Vault/Inbox/ is automatically picked up,
a metadata .md action file is created in /Needs_Action/, and the original
file is moved there for Claude to process.

Usage:
    uv run python watchers/filesystem_watcher.py
    uv run python watchers/filesystem_watcher.py --vault /path/to/vault
"""

import argparse
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

# Allow running from project root
sys.path.insert(0, str(Path(__file__).parent.parent))
from watchers.base_watcher import BaseWatcher


IGNORED_NAMES = {".gitkeep", ".DS_Store", "desktop.ini"}
IGNORED_EXTENSIONS = {".tmp", ".part", ".crdownload"}


class InboxDropHandler(FileSystemEventHandler):
    """Handles new file events in the /Inbox folder."""

    def __init__(self, needs_action: Path, logs: Path, dry_run: bool = False):
        self.needs_action = needs_action
        self.logs = logs
        self.dry_run = dry_run
        self.processed: set[str] = set()

    def on_created(self, event):
        if event.is_directory:
            return
        source = Path(event.src_path)
        self._process(source)

    def on_moved(self, event):
        if event.is_directory:
            return
        dest = Path(event.dest_path)
        self._process(dest)

    def _process(self, source: Path):
        if source.name in IGNORED_NAMES:
            return
        if source.suffix.lower() in IGNORED_EXTENSIONS:
            return
        if str(source) in self.processed:
            return
        self.processed.add(str(source))

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_stem = source.stem.replace(" ", "_")
        action_stem = f"FILE_{safe_stem}_{timestamp}"

        dest_file = self.needs_action / source.name
        action_md = self.needs_action / f"{action_stem}.md"

        if self.dry_run:
            print(f"[DRY RUN] Would process: {source.name} → {action_stem}.md")
            return

        # Move original file to /Needs_Action
        shutil.move(str(source), str(dest_file))

        # Create metadata action file
        action_md.write_text(
            f"""---
type: file_drop
original_name: {source.name}
received: {datetime.now().isoformat()}
size_bytes: {dest_file.stat().st_size if dest_file.exists() else 0}
status: pending
priority: normal
---

## File Received

A new file has been dropped into the Inbox.

- **File:** `{source.name}`
- **Received:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Suggested Actions

- [ ] Review file contents
- [ ] Categorise and tag
- [ ] Move to /Done when processed

## Notes

_Add processing notes here._
"""
        )

        # Append to daily log
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = self.logs / f"{today}.md"
        with open(log_file, "a") as f:
            f.write(
                f"- `{datetime.now().isoformat()}` **file_drop**: Received `{source.name}` → `{action_md.name}`\n"
            )

        print(f"✓ Processed: {source.name} → {action_md.name}")


class FilesystemWatcher(BaseWatcher):
    """
    Watchdog-based watcher for the /Inbox drop folder.

    Inherits BaseWatcher but uses watchdog for real-time event detection
    instead of polling, making it much more responsive.
    """

    def __init__(self, vault_path: str, dry_run: bool = False):
        super().__init__(vault_path, check_interval=0)
        self.dry_run = dry_run

    def check_for_updates(self) -> list:
        # Not used — watchdog handles this via event callbacks
        return []

    def create_action_file(self, item) -> Path:
        # Not used — handled by InboxDropHandler
        return Path()

    def run(self):
        handler = InboxDropHandler(
            needs_action=self.needs_action,
            logs=self.logs,
            dry_run=self.dry_run,
        )
        observer = Observer()
        observer.schedule(handler, str(self.inbox), recursive=False)
        observer.start()

        mode = "[DRY RUN] " if self.dry_run else ""
        self.logger.info(f"{mode}Watching: {self.inbox}")
        self.logger.info("Drop files into the Inbox folder to trigger processing.")
        self.logger.info("Press Ctrl+C to stop.")

        try:
            import time
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            self.logger.info("Watcher stopped.")
        observer.join()


def main():
    parser = argparse.ArgumentParser(description="Digital FTE — File System Watcher")
    parser.add_argument(
        "--vault",
        default=os.getenv("VAULT_PATH", "AI_Employee_Vault"),
        help="Path to the Obsidian vault (default: AI_Employee_Vault)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=os.getenv("DRY_RUN", "false").lower() == "true",
        help="Log intended actions without executing (safe for testing)",
    )
    args = parser.parse_args()

    watcher = FilesystemWatcher(vault_path=args.vault, dry_run=args.dry_run)
    watcher.run()


if __name__ == "__main__":
    main()
