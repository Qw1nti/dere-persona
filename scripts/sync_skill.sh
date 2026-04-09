#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE="$ROOT/skills/dere-persona/SKILL.md"

TARGETS=(
  "$ROOT/.agents/skills/dere-persona/SKILL.md"
  "$ROOT/.claude/skills/dere-persona/SKILL.md"
  "$ROOT/.cursor/skills/dere-persona/SKILL.md"
  "$ROOT/.windsurf/skills/dere-persona/SKILL.md"
  "$ROOT/plugins/dere-persona/skills/dere-persona/SKILL.md"
)

for target in "${TARGETS[@]}"; do
  mkdir -p "$(dirname "$target")"
  cp "$SOURCE" "$target"
done

printf 'Synced skill to %s targets\n' "${#TARGETS[@]}"
