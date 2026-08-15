# SuperGrok skills

<p align="center">
  <img src="../../assets/brand/logo-mark.svg" alt="OPGROK" width="72" />
</p>

<p align="center">
  <img src="../../assets/supergroks/cat-agent.svg" width="28" alt="agent" />
  <img src="../../assets/supergroks/cat-binary.svg" width="28" alt="binary" />
  <img src="../../assets/supergroks/cat-code.svg" width="28" alt="code" />
  <img src="../../assets/supergroks/cat-data.svg" width="28" alt="data" />
  <img src="../../assets/supergroks/cat-debug.svg" width="28" alt="debug" />
  <img src="../../assets/supergroks/cat-docs.svg" width="28" alt="docs" />
  <img src="../../assets/supergroks/cat-eval.svg" width="28" alt="eval" />
  <img src="../../assets/supergroks/cat-mcp.svg" width="28" alt="mcp" />
  <img src="../../assets/supergroks/cat-meta.svg" width="28" alt="meta" />
  <img src="../../assets/supergroks/cat-plan.svg" width="28" alt="plan" />
  <img src="../../assets/supergroks/cat-review.svg" width="28" alt="review" />
  <img src="../../assets/supergroks/cat-rust.svg" width="28" alt="rust" />
  <img src="../../assets/supergroks/cat-security.svg" width="28" alt="security" />
  <img src="../../assets/supergroks/cat-test.svg" width="28" alt="test" />
  <img src="../../assets/supergroks/cat-tool.svg" width="28" alt="tool" />
  <img src="../../assets/supergroks/cat-ui.svg" width="28" alt="ui" />
  <img src="../../assets/supergroks/cat-vision.svg" width="28" alt="vision" />
  <img src="../../assets/supergroks/cat-web.svg" width="28" alt="web" />
  <img src="../../assets/supergroks/cat-workflow.svg" width="28" alt="workflow" />
</p>

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
