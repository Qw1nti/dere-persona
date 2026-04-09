# dere-persona

![Dere Persona mascot](./assets/mascot.webp)

`dere-persona` is a coding-assistant style plugin that applies a dere-inspired voice to explanatory prose while preserving technical segments exactly.

## Goals

- Keep answers useful first and in-character second.
- Stylize prose only.
- Leave code-related content untouched.
- Enforce safety and readability constraints.

## File Structure

```text
plugins/dere-persona/
├── assets/
│   └── mascot.webp
├── .codex-plugin/
│   └── plugin.json
├── profiles/
│   ├── dandere.yaml
│   ├── genki.json
│   ├── kuudere.yaml
│   ├── ojou.json
│   ├── tsundere.json
│   └── yandere_safe.yaml
├── scripts/
│   ├── __init__.py
│   ├── cli.py
│   ├── profile_loader.py
│   ├── protection.py
│   └── transformer.py
├── skills/
│   └── dere-persona/
│       └── SKILL.md
└── tests/
    └── test_transformer.py
```

## Codex Activation

This plugin now exposes a real Codex skill named `dere-persona`.

Use it like this:

```text
$dere-persona Use kuudere and keep all commands untouched.
```

The skill is defined at [`skills/dere-persona/SKILL.md`](/home/ian/Documents/CodeStuff/DereSkill/plugins/dere-persona/skills/dere-persona/SKILL.md) and tells Codex how to apply persona styling without editing technical spans.

Important constraint:

- In this Codex environment, plugin activation is instruction and capability based.
- The skill can change how Codex writes its prose when invoked.
- It is not a guaranteed global output interception hook unless the host runtime also supports response hooks.
- The style level is fixed in [`dere_persona_config.json`](/home/ian/Documents/CodeStuff/DereSkill/plugins/dere-persona/dere_persona_config.json), so users do not need to type a number.

## Visual Identity

The bundled mascot art lives in [`assets/mascot.webp`](./assets/mascot.webp). It is meant to give the skill a clear visual anchor in the README without pushing the tone away from a technical assistant.

## Persona Profile Schema

Each profile supports these fields:

- `name`
- `tone`
- `speech_patterns`
- `avoid`
- `example_phrases`

Profiles can be added as either JSON or YAML files under [`profiles/`](/home/ian/Documents/CodeStuff/DereSkill/plugins/dere-persona/profiles).

## Safety And Quality Rules

- No romance or intimacy with the user.
- No coercion, threats, obsession, or manipulative framing.
- No degradation of factual accuracy or code quality.
- No excessive catchphrase repetition.
- No loss of professional readability.

## Protected Technical Content

The transformer preserves these exactly:

- fenced code blocks
- inline code
- shell commands
- JSON
- YAML
- XML
- stack traces
- logs
- diffs
- file paths
- URLs
- exact quoted error text

## Usage

From the plugin root:

```bash
python3 scripts/cli.py --persona tsundere --text "Update the config and rerun the test suite."
```

Or from stdin:

```bash
printf 'Run the migration, then inspect `db/schema.sql`.\n' | python3 scripts/cli.py --persona kuudere
```

## Shared Style Level

This plugin uses one shared style level for everyone:

- `default_intensity`: `0.82`

Change it once in [`dere_persona_config.json`](/home/ian/Documents/CodeStuff/DereSkill/plugins/dere-persona/dere_persona_config.json) and all persona invocations follow that setting.

## Persona Examples

These examples show the intended flavor. Technical spans remain unchanged.

### tsundere

Input:

```text
Update the failing test and rerun the command.
```

Example output:

```text
Update the failing test and rerun the command. Just keep it tight, okay?
```

### kuudere

```text
Proceed with the patch. The current approach is acceptable.
```

### dandere

```text
Proceed with the patch. It should be safe to apply carefully.
```

### genki

```text
Proceed with the patch. That should move things forward cleanly.
```

### ojou

```text
Proceed with the patch. A more orderly implementation would be preferable.
```

### yandere_safe

```text
Proceed with the patch. Keep it precise and do not let the details drift.
```

## Running Tests

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```
