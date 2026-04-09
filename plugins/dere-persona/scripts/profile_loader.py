"""Profile loading for dere-persona."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class PersonaProfile:
    name: str
    tone: str
    speech_patterns: dict[str, list[str]]
    avoid: list[str]
    example_phrases: list[str]


REQUIRED_FIELDS = {
    "name",
    "tone",
    "speech_patterns",
    "avoid",
    "example_phrases",
}


def load_profile(profile_name: str, profiles_dir: str | Path) -> PersonaProfile:
    """Load a persona profile from JSON or YAML."""
    profiles_path = Path(profiles_dir)
    candidates = [
        profiles_path / f"{profile_name}.json",
        profiles_path / f"{profile_name}.yaml",
        profiles_path / f"{profile_name}.yml",
    ]
    for path in candidates:
        if path.exists():
            data = _load_profile_file(path)
            return _coerce_profile(data)
    raise FileNotFoundError(f"Unknown persona profile: {profile_name}")


def _load_profile_file(path: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8")
    if path.suffix == ".json":
        return json.loads(raw)
    if path.suffix in {".yaml", ".yml"}:
        return _parse_simple_yaml(raw)
    raise ValueError(f"Unsupported profile format: {path.suffix}")


def _coerce_profile(data: dict[str, Any]) -> PersonaProfile:
    missing = REQUIRED_FIELDS - data.keys()
    if missing:
        names = ", ".join(sorted(missing))
        raise ValueError(f"Profile missing required fields: {names}")
    return PersonaProfile(
        name=str(data["name"]),
        tone=str(data["tone"]),
        speech_patterns=_coerce_speech_patterns(data["speech_patterns"]),
        avoid=[str(item) for item in data["avoid"]],
        example_phrases=[str(item) for item in data["example_phrases"]],
    )


def _coerce_speech_patterns(value: Any) -> dict[str, list[str]]:
    if not isinstance(value, dict):
        raise ValueError("speech_patterns must be an object")
    output: dict[str, list[str]] = {}
    for key, items in value.items():
        if isinstance(items, list):
            output[str(key)] = [str(item) for item in items]
        else:
            output[str(key)] = [str(items)]
    return output


def _parse_simple_yaml(raw: str) -> dict[str, Any]:
    """
    Parse a deliberately small YAML subset used by the bundled profile files.

    Supported shapes:
    - `key: value`
    - `key:`
      `  child: value`
      `  child:`
      `    - item`
    - `key:`
      `  - item`
    """

    root: dict[str, Any] = {}
    current_map: dict[str, Any] | None = None
    current_list_key: str | None = None
    parent_key: str | None = None

    for raw_line in raw.splitlines():
        line = raw_line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue

        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()

        if indent == 0:
            current_map = None
            current_list_key = None
            parent_key = None

            key, _, value = stripped.partition(":")
            key = key.strip()
            value = value.strip()
            if value:
                root[key] = _strip_quotes(value)
            else:
                root[key] = {}
                current_map = root[key]
                parent_key = key
            continue

        if stripped.startswith("- "):
            item = _strip_quotes(stripped[2:].strip())
            if current_map is not None and current_list_key is not None:
                current_map.setdefault(current_list_key, []).append(item)
            elif parent_key is not None:
                if not isinstance(root[parent_key], list):
                    root[parent_key] = []
                root[parent_key].append(item)
            else:
                raise ValueError("Invalid YAML list placement")
            continue

        key, _, value = stripped.partition(":")
        key = key.strip()
        value = value.strip()

        if current_map is None and parent_key is not None:
            root[parent_key] = {}
            current_map = root[parent_key]

        if current_map is None:
            raise ValueError("Invalid YAML structure")

        if value:
            current_map[key] = _strip_quotes(value)
            current_list_key = None
        else:
            current_map[key] = []
            current_list_key = key

    return root


def _strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value

