# SuperGrok navigation (MCP & inference)

How OPGROK and MCP should traverse skills.

## 1. Entry points (always available)

| Call | Role |
|------|------|
| `/opgrok` | Enter OPGrok Mode — craft a reusable harness binary |
| `/leslie` | Seal Winning Conditions; validate catalog |
| `/meta-asset-creator` | Brand / visual asset library |
| `/cat-<category>` | Navigate one category's roles |

## 2. Traversal algorithm (recommended)

```text
goal text
  → try /opgrok if multi-agent or complex
  → else match category via keywords / MCP_CATALOG.supergroks_by_category keys
  → load /cat-<category> navigator
  → pick /<category>-<role> by intent/purpose/when_to_use
  → load SKILL.md path from REGISTRY
  → execute or add to harness graph
```

## 3. Files for machines

| File | Use |
|------|-----|
| `REGISTRY.json` | Full skill records (authoritative) |
| `MCP_CATALOG.json` | Compact by-category routing |
| `AGENT_GLOSSARY.json` | Alphabetical agent array |
| `AGENT_GLOSSARY.md` | Human glossary |
| `CATEGORY_INDEX.md` | Category → role list |
| `NAVIGATION.md` | This file |

## 4. MCP tool mapping

| Tool | Behavior |
|------|----------|
| `sg_categories` | List categories + counts from MCP_CATALOG |
| `sg_nav` | Return navigator skill for a category |
| `sg_list` | List SuperGroks (optional category filter) |
| `sg_route` | Score intent against name/intent/purpose/tags |
| `sg_describe` | One skill record |
| `sg_load` | Full SKILL.md body |

## 5. Coverage snapshot

- **Total skills:** 178
- **By kind:** core=2, navigator=25, special=1, supergrok=150
- **Categories:** 27
- **Updated:** 2026-08-08T18:51:28.359155+00:00

## 6. Uniqueness rules

- Global `name` unique (slash command identity)
- `sg_id` unique
- Path = `core/skills/.../SKILL.md`
- SuperGrok nest = `<category>/<role>`
