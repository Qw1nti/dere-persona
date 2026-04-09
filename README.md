# dere-persona

An absurd Codex skill/plugin that makes the assistant talk like a dere archetype while leaving technical content alone.

[![Last Commit](https://img.shields.io/github/last-commit/Qw1nti/dere-persona?style=for-the-badge)](https://github.com/Qw1nti/dere-persona/commits/main)
[![License](https://img.shields.io/github/license/Qw1nti/dere-persona?style=for-the-badge)](https://github.com/Qw1nti/dere-persona/blob/main/LICENSE)
[![Repo](https://img.shields.io/github/stars/Qw1nti/dere-persona?style=for-the-badge)](https://github.com/Qw1nti/dere-persona)

Install • Usage • Personas • Safety • Development

---

![dere-persona mascot](./plugins/dere-persona/assets/mascot.webp)

## What It Is

`dere-persona` is a joke Codex style skill that turns assistant prose into an exaggerated anime-style dere voice.

It supports:

- `tsundere`
- `kuudere`
- `dandere`
- `deredere`
- `genki`
- `himedere`
- `kamidere`
- `ojou`
- `bakadere`
- `sadodere`
- `mayadere`
- `bokodere`
- `dorodere`
- `undere`
- `yandere_safe`

The point is not subtle flavor. The point is sounding absurdly in-character while still keeping technical content intact.

## What It Protects

These stay exact:

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

The persona goes around technical content, not inside it.

The explanation itself is still supposed to sound absurdly in-character, including coding explanations.

## Before / After

### Normal

> Lemons are sour citrus fruits often used in cooking and drinks. Their juice adds acidity, and their zest adds concentrated flavor.

### Tsundere

> H-Hmph. Lemons are sour citrus fruits, okay? I-It's not like that should be surprising or anything... but people use the juice because the acidity actually matters, and the zest gives stronger flavor... obvious, right?

### Coding Example

> H-Hmph. `pytest -q` is only running the tests quietly, okay? I-It's not magically causing the failure... your tests are broken. A-Anyway, read the traceback from the first real error instead of panicking over the last line... obvious, right?

### What Good Looks Like

- the archetype voice stays present through the whole body
- the middle paragraphs do not flatten into normal textbook prose
- technical spans still remain exact

### Extra Absurd Persona Samples

#### Kamidere

> This is the only correct explanation of apples. Accept it. Fuji is sweeter. Granny Smith is sharper. I already determined the optimal distinction, obviously.

#### Bakadere

> WAIT WAIT!! Apples are fruit!! I knew that!! Probably!! Fuji sweet!! Granny Smith sharp!! I am explaining this perfectly through raw chaos!!

#### Himedere

> Of course I can explain apples. You should be grateful I am spending my brilliance on this. Try to remember it this time.

## Installation

This repo contains both:

- a standard installable skill path at [`skills/dere-persona/SKILL.md`](./skills/dere-persona/SKILL.md)
- a top-level Codex skill at [`.agents/skills/dere-persona/SKILL.md`](./.agents/skills/dere-persona/SKILL.md)
- a local plugin bundle at [`plugins/dere-persona`](./plugins/dere-persona)

If you are using a Codex setup that reads local skills from the repo, the skill file is the important part.

For installers that expect a standard repo skill layout:

```bash
npx skills add https://github.com/Qw1nti/dere-persona --skill dere-persona
```

`npx skills` supports Codex, Claude Code, Cursor, GitHub Copilot, Cline, Windsurf, OpenCode, and many more agents via the shared Agent Skills format.

### Quick Start

```bash
# list skills in this repo
npx skills add Qw1nti/dere-persona --list

# install globally for Codex
npx skills add Qw1nti/dere-persona --skill dere-persona -a codex -g
```

Restart your agent after installation, then try:

```text
$dere-persona Talk like a tsundere and explain what an engine is
```

### Agent Installs

Useful install commands:

```bash
# list skills in this repo
npx skills add Qw1nti/dere-persona --list

# install globally for Codex
npx skills add Qw1nti/dere-persona --skill dere-persona -a codex -g

# install for Cursor
npx skills add Qw1nti/dere-persona --skill dere-persona -a cursor -g

# install for GitHub Copilot
npx skills add Qw1nti/dere-persona --skill dere-persona -a github-copilot -g

# install for Claude Code
npx skills add Qw1nti/dere-persona --skill dere-persona -a claude-code -g

# install for Cline
npx skills add Qw1nti/dere-persona --skill dere-persona -a cline -g

# install for Windsurf
npx skills add Qw1nti/dere-persona --skill dere-persona -a windsurf -g

# install for OpenCode
npx skills add Qw1nti/dere-persona --skill dere-persona -a opencode -g
```

Examples of agent ids supported by `npx skills` include:

- `codex`
- `claude-code`
- `cursor`
- `github-copilot`
- `cline`
- `windsurf`
- `opencode`
- `openclaw`
- `goose`
- `roo`
- `qwen-code`
- `kiro-cli`
- `command-code`
- `continue`
- `gemini-cli`
- `replit`

Project-local install also works if you omit `-g`.

### Agent Matrix

| Agent | Install Command |
| --- | --- |
| Codex | `npx skills add Qw1nti/dere-persona --skill dere-persona -a codex -g` |
| Claude Code | `npx skills add Qw1nti/dere-persona --skill dere-persona -a claude-code -g` |
| Cursor | `npx skills add Qw1nti/dere-persona --skill dere-persona -a cursor -g` |
| GitHub Copilot | `npx skills add Qw1nti/dere-persona --skill dere-persona -a github-copilot -g` |
| Cline | `npx skills add Qw1nti/dere-persona --skill dere-persona -a cline -g` |
| Windsurf | `npx skills add Qw1nti/dere-persona --skill dere-persona -a windsurf -g` |
| OpenCode | `npx skills add Qw1nti/dere-persona --skill dere-persona -a opencode -g` |

## Usage

Trigger it with prompts like:

```text
$dere-persona Talk like a tsundere and tell me about apples
```

```text
$dere-persona Use genki mode and explain oranges
```

```text
$dere-persona Use ojou mode and explain databases
```

```text
$dere-persona Use kamidere mode and explain why `pytest -q` is failing
```

```text
$dere-persona Use bakadere mode and explain what an engine is
```

Stop it with:

```text
normal mode
```

or:

```text
stop dere
```

## Supported Personas

### tsundere

- defensive
- sharp
- embarrassed
- dramatic
- stammers and pauses everywhere

### kuudere

- cold
- clipped
- minimal
- blunt
- overly certain

### dandere

- shy
- quiet
- hesitant
- apologetic
- pause-heavy

### genki

- loud
- hyper
- excitable
- all-caps bursts
- maximum momentum

### ojou

- elegant
- smug
- theatrical
- refined
- `Ara ara...`

### yandere_safe

- intense
- watchful
- overfocused
- controlled
- unsettling but sanitized

### deredere

- warm
- cheerful
- explosively supportive
- celebratory

### himedere

- prideful
- demanding
- praise-seeking
- self-important

### kamidere

- absolute
- god-complex
- authoritative
- absurdly certain

### bakadere

- chaotic
- clumsy
- playful
- somehow successful

### sadodere

- teasing
- smug
- playfully cruel
- mocking

### mayadere

- reluctant
- hostile at first
- cooperative later
- annoyed into helping

### bokodere

- rough
- blunt
- tough
- impatient

### dorodere

- bitter
- pessimistic
- heavy
- expecting failure

### undere

- agreeable
- adaptive
- user-following
- compliant

## Testing

After installing and restarting your agent, try:

```text
$dere-persona Talk like a tsundere and explain what an engine is
```

```text
$dere-persona Use genki mode and explain what JSON is
```

```text
$dere-persona Use kamidere mode and explain why `pytest -q` is failing
```

```text
$dere-persona Use bakadere mode and explain this command: `npm test`
```

Good output should:

- stay in-character for most of the explanation
- avoid collapsing into textbook prose in the middle
- keep technical spans exact

## Troubleshooting

### I installed it but `$dere-persona` does not appear

- restart the agent completely
- verify the installed path contains `skills/dere-persona/SKILL.md`
- try `npx skills add Qw1nti/dere-persona --list`
- reinstall with the explicit agent id and `-g`

### The skill appears but the output is still too mild

- start a fresh session after installation
- invoke the skill explicitly with `$dere-persona`
- test with a simple casual prompt first
- then test with a coding prompt

### It sounds like normal prose with an anime intro and outro

That is the main failure mode this repo is trying to avoid.

Good output should:

- sound in-character through the full explanation
- keep most sentences flavored by the archetype
- avoid flattening into neutral textbook paragraphs halfway through

## Safety

This is joke-mode presentation only.

Hard limits:

- no romance or intimacy with the user
- no coercion, threats, obsession, or manipulative framing
- no changing technical content
- no touching protected spans

`yandere_safe` is intentionally restricted so it stays intense without becoming threatening or possessive.

## Repo Layout

```text
.
├── .agents/
│   ├── plugins/marketplace.json
│   └── skills/dere-persona/SKILL.md
├── skills/
│   └── dere-persona/SKILL.md
├── plugins/
│   └── dere-persona/
│       ├── .codex-plugin/plugin.json
│       ├── README.md
│       ├── assets/
│       ├── profiles/
│       ├── scripts/
│       └── tests/
├── LICENSE
└── README.md
```

## Development

Run tests:

```bash
cd plugins/dere-persona
python3 -m unittest discover -s tests -p 'test_*.py'
```

Quick local CLI check:

```bash
cd plugins/dere-persona
python3 scripts/cli.py --persona tsundere --text 'Tell me about apples.'
```

## Notes

- The style level is shared and fixed in [`dere_persona_config.json`](./plugins/dere-persona/dere_persona_config.json)
- The current target is intentionally absurd
- If the response is still too mild, the right place to push harder is the skill instructions and persona sentence transforms
