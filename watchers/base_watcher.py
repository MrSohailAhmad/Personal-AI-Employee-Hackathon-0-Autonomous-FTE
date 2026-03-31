"""Base watcher template — all watchers inherit from this class."""

import time
import logging
import os
from pathlib import Path
from abc import ABC, abstractmethod
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
)


class BaseWatcher(ABC):
    """Abstract base class for all Digital FTE watchers."""

    def __init__(self, vault_path: str, check_interval: int = 60):
        self.vault_path = Path(vault_path)
        self.inbox = self.vault_path / "Inbox"
        self.needs_action = self.vault_path / "Needs_Action"
        self.done = self.vault_path / "Done"
        self.logs = self.vault_path / "Logs"
        self.check_interval = check_interval
        self.logger = logging.getLogger(self.__class__.__name__)
        self._running = False

        # Ensure required folders exist
        for folder in [self.inbox, self.needs_action, self.done, self.logs]:
            folder.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def check_for_updates(self) -> list:
        """Return list of new items to process."""
        pass

    @abstractmethod
    def create_action_file(self, item) -> Path:
        """Create a .md file in Needs_Action folder."""
        pass

    def log_event(self, event_type: str, details: str):
        """Write an event to the daily log file."""
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = self.logs / f"{today}.md"
        timestamp = datetime.now().isoformat()
        entry = f"- `{timestamp}` **{event_type}**: {details}\n"
        with open(log_file, "a") as f:
            if not log_file.exists() or log_file.stat().st_size == 0:
                f.write(f"# Log — {today}\n\n")
            f.write(entry)

    def run(self):
        """Main watcher loop."""
        self._running = True
        self.logger.info(f"Starting {self.__class__.__name__} (interval: {self.check_interval}s)")
        while self._running:
            try:
                items = self.check_for_updates()
                for item in items:
                    path = self.create_action_file(item)
                    self.logger.info(f"Created action file: {path.name}")
                    self.log_event("new_item", f"Created {path.name}")
            except KeyboardInterrupt:
                self.logger.info("Shutting down...")
                self._running = False
                break
            except Exception as e:
                self.logger.error(f"Error during check: {e}")
            time.sleep(self.check_interval)

    def stop(self):
        self._running = False
