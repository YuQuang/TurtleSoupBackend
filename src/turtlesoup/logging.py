from __future__ import annotations

import logging
import logging.config
from pathlib import Path

import yaml


_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_CONFIG_PATH = _PROJECT_ROOT / "src" / "config" / "logging.yaml"
_LOG_PATH = _PROJECT_ROOT / "logs" / "app.log"


def _configure_logging() -> None:
    _LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    with _CONFIG_PATH.open(encoding="utf-8") as config_file:
        config = yaml.safe_load(config_file)

    config["handlers"]["file"]["filename"] = str(_LOG_PATH)
    logging.config.dictConfig(config)


_configure_logging()


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)