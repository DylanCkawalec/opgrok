# Application shell (optional)

These apps are **clients** of the OPGROK core. You do **not** need them to craft or run SuperGrok harnesses.

| App | Path | Role |
|-----|------|------|
| **Web** | [`web/`](web/) | FastAPI UI — chat + workflow builder (default port **420**) |
| **Chat** | [`chat/`](chat/) | Rust terminal / optional server chat (workspace crate) |
| **n8n** | [`n8n/`](n8n/), [`n8n-nodes/`](n8n-nodes/) | Local automation runtime + custom nodes |

## When to use apps

- You want a browser UI for chat/workflows next to harness development.
- You are integrating n8n-style automations as a separate product surface.

## When to ignore apps

- You only use `@opgrok` from Grok Build or `core/tools/*` from the CLI.
- You are packaging harness binaries into `core/binaries/`.

## Start / stop (process manager)

From repo root:

```bash
# requires .env with XAI_API_KEY; Node 18+ for n8n modes
./opgrok start      # web + n8n
./opgrok chat       # web only
./opgrok status
./opgrok stop
```

Scripts live under `ops/scripts/`. Paths assume monorepo layout (`apps/web`, not the old `webapp/`).

## Brand assets in the web UI

| Surface | How |
|---------|-----|
| `/assets/*` | FastAPI mount of monorepo `assets/` (logos, protocol art) |
| `/static/assets/*` | Icons + tokens copied under `web/app/static/assets/` |
| `/` | Chat — OPGROK logo, harness graph welcome, API key pill |
| `/harnesses` | Craft + list + dry/live run SuperGrok packages |
| `/workflows` | n8n builder with OPGROK nav |
| `GET /api/health` | `{ xai_key_present, repo_root, … }` |

Palette: void / amber / cyan via `assets/tokens.css`.

## Rule

**Core owns SuperGroks and harnesses. Apps do not.**  
Do not add SuperGrok `SKILL.md` files under `apps/`.
