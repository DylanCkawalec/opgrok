# Documentation index

## Start here

| Doc | Audience |
|-----|----------|
| [../README.md](../README.md) | Everyone — product overview, quick start, cheatsheet |
| [../core/README.md](../core/README.md) | Core harness kernel |
| [../assets/README.md](../assets/README.md) | Brand + UI asset library |
| [../assets/assets.md](../assets/assets.md) | Asset plan, tokens, Imagine prompts |

## Core deep-dives

| Doc | Topic |
|-----|--------|
| [../core/toolkit/README.md](../core/toolkit/README.md) | Grok-native toolkit (models, memory, tools, judge…) |
| [../core/harness/SPEC.md](../core/harness/SPEC.md) | Harness law |
| [../core/skills/README.md](../core/skills/README.md) | SuperGrok catalog |
| [../core/skills/opgrok/SKILL.md](../core/skills/opgrok/SKILL.md) | `@opgrok` procedure |
| [../core/skills/leslie/SKILL.md](../core/skills/leslie/SKILL.md) | Leslie Winning Conditions |
| [../apps/README.md](../apps/README.md) | Optional web / chat / n8n shell |

## External

- [Leslie — specification-master agent](https://github.com/DylanCkawalec/Leslie)

## API troubleshooting

If the xAI API "never fires":

1. Confirm root `.env` has an **enabled** `XAI_API_KEY` (console.x.ai).
2. Restart the web server so it reloads env (`REPO_ROOT` is monorepo root).
3. Hit `GET /api/health` → `xai_key_present: true`.
4. Harness dry-run does **not** call the API by design — use live run.
