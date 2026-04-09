"""Shared settings for dere-persona."""

from __future__ import annotations

import json
from pathlib import Path


CONFIG_PATH = Path(__file__).resolve().parent.parent / "dere_persona_config.json"


def load_settings(config_path: str | Path = CONFIG_PATH) -> dict:
    path = Path(config_path)
    return json.loads(path.read_text(encoding="utf-8"))
