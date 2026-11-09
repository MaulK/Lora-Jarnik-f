from datetime import datetime
from pathlib import Path


class SystemLogger:
    __slots__ = "log_path"

    log_path: Path

    def __init__(self):
        self.log_path = Path("logs/system_log.txt")
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.log_event("[INFO]: Start program")

    def log_event(self, event: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"{timestamp} {event}\n"
        with self.log_path.open("a", encoding="utf-8") as f:
            f.write(log_line)
