"""Split assistant text into prose and protected technical spans."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Segment:
    text: str
    protected: bool


FENCED_BLOCK_RE = re.compile(r"```[\w+-]*\n.*?```", re.DOTALL)
INLINE_PROTECTED_RE = re.compile(
    r"""
    (`[^`\n]+`) |
    ("[^"\n]*(?:error|exception|failed|invalid|not\ found)[^"\n]*") |
    ('[^'\n]*(?:error|exception|failed|invalid|not\ found)[^'\n]*') |
    (https?://[^\s)>]+) |
    ((?:[A-Za-z]:)?(?:\.\.?/|/)[A-Za-z0-9._\-/]+) |
    (\b[\w.\-]+/[\w./\-]+\b)
    """,
    re.IGNORECASE | re.VERBOSE,
)

COMMAND_RE = re.compile(
    r"^\s*(?:[$#]\s+|"
    r"(?:git|npm|pnpm|yarn|python3?|pytest|pip|uv|node|bash|sh|ls|cd|cat|cp|mv|rm|mkdir|curl|wget|docker|kubectl|make|cmake|cargo|go|java|javac|gradle|./)[^\n]*)",
    re.IGNORECASE,
)
STACK_TRACE_RE = re.compile(
    r"(?m)^(?:Traceback \(most recent call last\):|\s+File \".+\", line \d+,|Exception in thread |\s+at\s+.+\(.+\)|Caused by: .+|[A-Za-z_][\w.]*Error: .+)"
)
LOG_LINE_RE = re.compile(
    r"(?m)^(?:\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(?:[.,]\d+)?(?:Z|[+-]\d{2}:\d{2})?\s+\w+|"
    r"\[(?:TRACE|DEBUG|INFO|WARN|WARNING|ERROR|FATAL)\]|"
    r"(?:TRACE|DEBUG|INFO|WARN|WARNING|ERROR|FATAL):)"
)
DIFF_RE = re.compile(r"(?m)^(?:diff --git|index [0-9a-f]+\.\.[0-9a-f]+|--- |\+\+\+ |@@ )")
XML_RE = re.compile(r"^\s*<([A-Za-z_][\w:.-]*)(?:\s[^>]*)?>.*</\1>\s*$", re.DOTALL)
YAML_PAIR_RE = re.compile(r"(?m)^\s*[\w.-]+\s*:\s*.+$")


def split_text(text: str) -> list[Segment]:
    segments: list[Segment] = []
    cursor = 0
    for match in FENCED_BLOCK_RE.finditer(text):
        if match.start() > cursor:
            segments.extend(_split_non_fenced_text(text[cursor:match.start()]))
        segments.append(Segment(match.group(0), True))
        cursor = match.end()
    if cursor < len(text):
        segments.extend(_split_non_fenced_text(text[cursor:]))
    return [segment for segment in segments if segment.text]


def _split_non_fenced_text(text: str) -> list[Segment]:
    parts = re.split(r"(\n\s*\n)", text)
    segments: list[Segment] = []
    for part in parts:
        if not part:
            continue
        if re.fullmatch(r"\n\s*\n", part):
            segments.append(Segment(part, True))
            continue
        if _looks_like_protected_block(part):
            segments.append(Segment(part, True))
            continue
        segments.extend(_split_inline_protected(part))
    return segments


def _split_inline_protected(text: str) -> list[Segment]:
    cursor = 0
    segments: list[Segment] = []
    for match in INLINE_PROTECTED_RE.finditer(text):
        if match.start() > cursor:
            segments.append(Segment(text[cursor:match.start()], False))
        segments.append(Segment(match.group(0), True))
        cursor = match.end()
    if cursor < len(text):
        segments.append(Segment(text[cursor:], False))
    return segments


def _looks_like_protected_block(block: str) -> bool:
    stripped = block.strip()
    if not stripped:
        return True
    if COMMAND_RE.match(stripped):
        return True
    if STACK_TRACE_RE.search(block):
        return True
    if LOG_LINE_RE.search(block):
        return True
    if DIFF_RE.search(block):
        return True
    if _looks_like_json(stripped):
        return True
    if _looks_like_yaml(block):
        return True
    if XML_RE.match(stripped):
        return True
    return False


def _looks_like_json(text: str) -> bool:
    if not text or text[0] not in "{[":
        return False
    try:
        json.loads(text)
        return True
    except json.JSONDecodeError:
        return False


def _looks_like_yaml(text: str) -> bool:
    lines = [line for line in text.splitlines() if line.strip()]
    if len(lines) < 2:
        return False
    pair_count = sum(1 for line in lines if YAML_PAIR_RE.match(line))
    list_count = sum(1 for line in lines if line.lstrip().startswith("- "))
    return pair_count >= 2 or (pair_count >= 1 and list_count >= 1)
