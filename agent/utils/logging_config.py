import logging
import os
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from .env_util import get_env_var


def configure_logging() -> None:
    log_dir = get_env_var("LX_AICODING_LOG_DIR", "logs")
    log_level = get_env_var("LX_AICODING_LOG_LEVEL", "INFO").upper()
    retention_days = int(get_env_var("LX_AICODING_LOG_RETENTION_DAYS", "14"))
    log_when = get_env_var("LX_AICODING_LOG_WHEN", "midnight")
    log_interval = int(get_env_var("LX_AICODING_LOG_INTERVAL", "1"))

    os.makedirs(log_dir, exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.handlers.clear()

    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    backend_handler = TimedRotatingFileHandler(
        Path(log_dir) / "backend.log",
        when=log_when,
        interval=log_interval,
        backupCount=retention_days,
        encoding="utf-8",
    )
    backend_handler.setLevel(log_level)
    backend_handler.setFormatter(formatter)
    root_logger.addHandler(backend_handler)

    agent_handler = TimedRotatingFileHandler(
        Path(log_dir) / "agent-runs.log",
        when=log_when,
        interval=log_interval,
        backupCount=retention_days,
        encoding="utf-8",
    )
    agent_handler.setLevel(log_level)
    agent_handler.setFormatter(formatter)
    root_logger.addHandler(agent_handler)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
