# OPGROK

<p align="center">
  <img src="assets/brand/readme-hero.png" alt="OPGROK" />
</p>
<p align="center">
  <strong>Turn any goal into a team of Grok agents — shipped as one reusable binary.</strong>
</p>
<p align="center">
  <a href="https://console.x.ai">xAI API</a> · 150 specialist agents · Python + Rust
</p>

---

## Why this exists

If you run Grok Build local, you already write prompts that do real work — code reviews, security audits, data pipelines, site builds. Every time you want similar work done, you re-prompt from scratch. OPGROK fixes that: it takes a workflow or project prompt and freezes it into a binary you can run again and again. Your past prompts become reusable tools.

One prompt in. One binary out. Run it whenever you want, through the xAI API or the Grok terminal.

---

## What it does

Give it a goal. It hires the right specialist agents, wires them into a pipeline, and packages that pipeline as a single binary you can run again without re-planning.

```bash
./opgrok craft "build a landing page with hero and pricing"
./opgrok run build-a-landing-page-with-hero-and-pricing
```

### Examples

A binary can be as simple or as intricate as your goal demands — from a single-pass review to a multi-stage pipeline with parallel branches, memory across runs, and a judge node that reviews the final output.

| Goal | What the binary does |
|------|---------------------|
| `audit a Python codebase for security issues` | Scout maps the repo → smith isolates each module → audit checks against a security checklist → seal produces a report with severity ratings |
| `build a marketing site with hero, pricing, and wireframes` | Scout drafts structure → forge writes copy and layout → smith generates components → review audits consistency → docs produces a handoff README |
| `review a Rust crate for correctness and performance` | Scout maps the crate → trace profiles hot paths → audit checks idioms → forge proposes fixes → seal gates the final review |
| `generate a data pipeline spec with dry-run counts` | Plan scouts requirements → data smith designs the schema → data forge writes the transform → data audit verifies counts → docs ships the spec |
| `triage a failing CI pipeline` | Debug scout reads the logs → debug trace isolates the root cause → code smith writes the fix → test seal verifies green CI |

Each row is one craft command. Each binary is reusable — run it on a new repo, a new codebase, a new dataset, without re-planning.

---

## How it works

```
goal → route agents → seal winning condition → build graph → package binary → run via Grok API → result
```

1. **Route** — match your goal to specialist agents (SuperGroks) by intent and purpose
2. **Seal** — write a falsifiable winning condition (what does success look like?)
3. **Graph** — arrange hired agents into an ordered DAG
4. **Package** — compile to one binary + one README
5. **Run** — each node calls the xAI Grok API with its skill injected
6. **Result** — output bubbles up from the final node

---

## SuperGroks

178 indexed skills under `core/skills/<category>/<role>/SKILL.md`:

| Kind | Count | Example |
|------|------:|---------|
| Specialists | 150 | `/rust-smith`, `/plan-scout` |
| Navigators | 25 | `/cat-code`, `/cat-agent` |
| Core | 2 | `/opgrok`, `/seal` |
| Special | 1 | `/meta-asset-creator` |

**6 roles:** `smith` (smallest unit) · `forge` (end-to-end) · `scout` (map first) · `trace` (root cause) · `audit` (checklist) · `seal` (gate + freeze)

---

## Quick start

**Prerequisites:** Python 3.10+, `XAI_API_KEY` from [console.x.ai](https://console.x.ai). Rust and Node are optional.

```bash
git clone https://github.com/DylanCkawalec/opgrok.git
cd opgrok
cp .env.example .env   # set XAI_API_KEY=...
./opgrok craft "your goal here"
./opgrok run <slug> --dry-run   # no API calls
./opgrok run <slug>             # live — calls xAI per node
```

Install a harness globally:

```bash
./opgrok build <slug> --install
export PATH="$HOME/.opgrok/bin:$PATH"
opgrok-<slug> --goal "..."
```

---

## CLI

| Command | What it does |
|---------|-------------|
| `./opgrok craft "goal"` | Hire agents, seal condition, build package |
| `./opgrok run <slug>` | Run harness (add `--dry-run` to skip API) |
| `./opgrok build <slug>` | Compile binary (+ `--install` for global) |
| `./opgrok route "intent"` | Preview which agents match |
| `./opgrok validate` | Check the skill catalog |
| `./opgrok harnesses` | List built harnesses |
| `./opgrok start` | Launch optional web UI (port 420) |
| `./opgrok stop` | Stop web UI |

---

## Repository

```
opgrok/
├── core/       agents, harness craft/run, toolkit, Rust control plane
├── apps/       optional web/chat/n8n UI
├── ops/        install + CLI scripts
├── assets/     brand + UI assets
└── docs/       doc index
```

---

## Configuration

Key environment variables (see `.env.example`):

| Variable | Default | Purpose |
|----------|---------|---------|
| `XAI_API_KEY` | — | Required — from console.x.ai |
| `OPGROK_MODEL` | `grok-4` | Strong model for heavy nodes |
| `OPGROK_MODEL_FAST` | `grok-3-mini` | Fast model for light nodes |
| `OPGROK_PARALLEL` | `1` | Run ready nodes concurrently |
| `OPGROK_MEMORY` | `1` | Persist blackboard across runs |
| `OPGROK_JUDGE` | `1` | Append a judge node to review |
| `OPGROK_ALLOW_SHELL` | `0` | Off by default — enable shell tools |

---

## Docs

- [core/README.md](core/README.md) — core product reference
- [core/toolkit/README.md](core/toolkit/README.md) — toolkit capabilities
- [core/harness/SPEC.md](core/harness/SPEC.md) — harness spec
- [core/skills/README.md](core/skills/README.md) — agent catalog layout
- [apps/README.md](apps/README.md) — optional app shell
- [docs/README.md](docs/README.md) — doc index

---

## Principles

1. **Grok is the brain** — OPGROK adds structure, memory, and packaging.
2. **Spec before code** — winning conditions, not silent code dumps.
3. **One harness = one binary + one README** — no doc sprawl.
4. **Agents are contracts** — independent, composable, binary-ready.
5. **Apps are optional** — the core runs from CLI without any UI.

---

## Safety

- API keys stay in `.env` — never committed.
- Shell tools off unless `OPGROK_ALLOW_SHELL=1`.
- Security agents audit and harden — they do not author exploits.
