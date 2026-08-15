# OPGROK

<p align="center">
  <img src="assets/brand/readme-hero.png" alt="OPGROK" />
</p>
<p align="center">
  <strong>Turn any goal into a team of Grok agents — shipped as one reusable binary.</strong>
</p>
<p align="center">
  <a href="https://console.x.ai">xAI API</a> · 150 specialist agents · Python + Rust · v1.0.0
</p>

Give OPGROK a goal. It hires specialist SuperGroks, seals a Winning Condition, and packages that team as a binary you can run again. Clone this repo and work from the clone root — this is a **CLI factory**, not a folder to invent inside some other project.

---

## 1. Install

**You need:** Python 3.10+ and an API key from [console.x.ai](https://console.x.ai). Install Rust (`cargo`) if you want SuperGrok-written product crates to compile.

```bash
git clone https://github.com/DylanCkawalec/opgrok.git
cd opgrok
cp .env.example .env
```

Open `.env` and set:

```bash
XAI_API_KEY=xai-...
```

Make the CLI executable (already is in a fresh clone):

```bash
chmod +x ./opgrok
./opgrok howto
```

That is the whole install. Packages you craft later land in `core/binaries/` on **your** machine.

---

## 2. Teach Grok (one prompt)

In [Grok Build](https://grok.x.ai) (or any Grok session with this clone open), paste:

```
Install OPGROK from this clone and set up the /opgrok skill.

1. Find the repo root by locating core/tools/craft_harness.py. cd there.
2. If .env is missing, copy .env.example to .env and tell me to put an
   XAI_API_KEY from https://console.x.ai in it. Do not invent a key.
3. Wire the skill so /opgrok loads this clone:

   mkdir -p ~/.grok/skills
   ln -sfn "$(pwd)/core/skills/opgrok" ~/.grok/skills/opgrok

4. Optionally add this clone to Grok Build skills.paths:
   /absolute/path/to/this/opgrok/core/skills
5. Run: python3 core/tools/validate_supergroks.py
6. Run: ./opgrok howto
7. Confirm the skill symlink and that LESLIE GATE: PASS.
8. Stop. Do not invent a goal. Wait for me to type /opgrok <goal>.

You are the foreman. SuperGroks write the product. Never invent a
local ./opgrok/ folder in some other repo.
```

After that, `/opgrok` in Grok Build is this factory.

---

## 3. Use it

### In Grok Build

```
/opgrok
/opgrok build a landing page with hero and pricing
/opgrok review this Rust crate for correctness and ship a reusable audit binary
```

Bare `/opgrok` prints the card and waits. With a goal, Grok **crafts** the harness (hire + Winning Condition + package), then **runs it live** so SuperGroks emit the product.

### From the terminal

```bash
./opgrok craft "review this repo for security issues"
./opgrok run <slug> --dry-run          # package check, no API
./opgrok run <slug>                    # live — SuperGroks call Grok
```

Same steps without the wrapper:

```bash
python3 core/tools/craft_harness.py --slug review-this-repo --hire 8 \
  "review this repo for security issues"
python3 core/tools/run_harness.py review-this-repo --repo . --dry-run
PYTHONUNBUFFERED=1 OPGROK_REQUIRE_LIVE=1 python3 -u \
  core/tools/run_harness.py review-this-repo --repo .
```

Watch a live run:

```bash
tail -f core/binaries/<slug>/STATUS
```

### What “done” means

| You just did | What you have |
|--------------|----------------|
| `craft` | A **scaffold** — graph, README, Winning Condition, runner. No API yet. |
| `run --dry-run` | Package-law check. Still not the product. |
| **Live** `run` | SuperGroks write sources into `product/`. If cargo `--require-cargo` succeeds, that is the **product** binary. |

`craft` does not call the xAI API. `ledger.total_tokens == 0` or an empty `product/` means the product was not built.

The agent in Grok is the **foreman**. SuperGroks are the smiths. The foreman must not write `product/` or `crate/src/` by hand.

---

## Commands

| Command | What it does |
|---------|--------------|
| `./opgrok craft "goal"` | Hire SuperGroks, seal the condition, write the package |
| `./opgrok run <slug>` | Run the harness (`--dry-run` skips the API) |
| `./opgrok build <slug>` | Compile (`--install` copies to `~/.opgrok/bin`) |
| `./opgrok apex "goal"` | Detect mode, then craft |
| `./opgrok route "intent"` | Preview which SuperGroks match |
| `./opgrok validate` | Check the skill catalog |
| `./opgrok harnesses` | List packages in this clone |
| `./opgrok howto` | Print the factory card |

Install a finished harness on your `PATH`:

```bash
./opgrok build <slug> --install
export PATH="$HOME/.opgrok/bin:$PATH"
opgrok-<slug> --goal "..."
```

---

## Configuration

Copy `.env.example` to `.env`. Useful keys:

| Variable | Default | Purpose |
|----------|---------|---------|
| `XAI_API_KEY` | — | Required for live runs |
| `OPGROK_MODEL` | `grok-4.6` | Strong / forge nodes |
| `OPGROK_MODEL_FAST` | `grok-4.5` | Scout / docs nodes |
| `OPGROK_MODEL_JUDGE` | `grok-4.6` | Decisive judge |
| `OPGROK_MAX_TOKENS_PRODUCER` | `32768` | Room for forge/smith/seal to emit full files |
| `OPGROK_PARALLEL` | `1` | Run ready nodes together |
| `OPGROK_MEMORY` | `1` | Remember the blackboard across runs |
| `OPGROK_JUDGE` | `1` | Append a judge node |
| `OPGROK_ALLOW_SHELL` | `0` | Off by default |

Do not pass `--max-tokens 8192` on producers. grok-4.6 reasoning can fill 8k before any JSON.

---

## SuperGroks

178 indexed skills under `core/skills/<category>/<role>/SKILL.md`:

| Kind | Count | Example |
|------|------:|---------|
| Specialists | 150 | `/rust-smith`, `/plan-scout` |
| Navigators | 25 | `/cat-code`, `/cat-agent` |
| Core | 2 | `/opgrok`, `/leslie` |
| Special | 1 | `/meta-asset-creator` |

**6 roles:** `smith` (smallest unit) · `forge` (end-to-end) · `scout` (map first) · `trace` (root cause) · `audit` (checklist) · `seal` (gate + freeze)

Foreman rules: [`core/skills/opgrok/SKILL.md`](core/skills/opgrok/SKILL.md).

---

## More

- [core/README.md](core/README.md) — kernel layout
- [core/toolkit/README.md](core/toolkit/README.md) — runtime modules
- [core/harness/SPEC.md](core/harness/SPEC.md) — harness law
- [core/skills/README.md](core/skills/README.md) — catalog

**Principles:** Grok is the brain. Spec before code. One harness = one binary + one README. The CLI is the product.

**Safety:** API keys stay in `.env`. Shell tools stay off unless `OPGROK_ALLOW_SHELL=1`. Security agents audit and harden — they do not author exploits.
