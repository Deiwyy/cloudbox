from __future__ import annotations

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


FORMAT = "[%(levelname)s] %(name)s: %(message)s"

RESET = "\033[0m"

COLORS = {
    logging.DEBUG: "\033[90m",
    logging.INFO: "\033[37m",
    logging.WARNING: "\033[33m",
    logging.ERROR: "\033[31m",
    logging.CRITICAL: "\033[1;31m",
}


class ExtraFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)

        standard_fields = {
            "name",
            "msg",
            "args",
            "levelname",
            "levelno",
            "pathname",
            "filename",
            "module",
            "exc_info",
            "exc_text",
            "stack_info",
            "lineno",
            "funcName",
            "created",
            "msecs",
            "relativeCreated",
            "thread",
            "threadName",
            "processName",
            "process",
            "message",
            "asctime",
        }

        extra = {
            key: value
            for key, value in record.__dict__.items()
            if key not in standard_fields and not key.startswith("_")
        }

        if extra:
            message += " | " + " ".join(
                f"{key}={value}"
                for key, value in extra.items()
            )

        return message


class ConsoleFormatter(ExtraFormatter):
    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)

        color = COLORS.get(record.levelno, RESET)

        return f"{color}{message}{RESET}"


def configure_logging(
    log_file: str | Path,
    *,
    level: int = logging.INFO,
) -> None:
    root = logging.getLogger()
    root.setLevel(level)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(
        ConsoleFormatter(FORMAT)
    )

    log_file = Path(log_file)
    log_file.parent.mkdir(parents=True, exist_ok=True)

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(
        ExtraFormatter(FORMAT)
    )

    root.addHandler(console_handler)
    root.addHandler(file_handler)