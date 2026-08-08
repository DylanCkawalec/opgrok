# SuperGrok skills

```
core/skills/
  _framework/          # glossary, registry, navigation, category index
  leslie/              # specification master
  opgrok/              # harness craft
  <category>/
    <role>/            # smith | forge | scout | trace | audit | seal
      SKILL.md
      IDENTITY.txt
```

- **150 SuperGroks** = 25 categories x 6 roles
- **Call:** `/<category>-<role>` (e.g. `/rust-smith`)
- **Binary id:** `opgrok.sg.<category>-<role>`
- **Identity:** `Name-Hash` in SKILL.md + `core/registry/named-hashes.json`
- **Generate:** `python3 core/tools/generate_supergroks.py`
- **Validate:** `python3 core/tools/validate_supergroks.py`

Roles:
| Role | Job |
|------|-----|
| smith | smallest correct unit |
| forge | end-to-end path |
| scout | map before edit |
| trace | RCA chain |
| audit | checklist findings |
| seal | win gate + freeze |

Grok Build discovery:

```toml
[skills]
paths = ["<repo>/core/skills"]
```
