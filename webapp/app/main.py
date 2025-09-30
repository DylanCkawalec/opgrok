import os
import subprocess
import uuid
from typing import Optional, List, Dict

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(APP_ROOT, "..", ".."))
RUST_BIN = os.path.join(REPO_ROOT, "grok-chat-app", "target", "release", "grok-chat-app")

# In-memory sessions (ephemeral)
sessions: Dict[str, List[Dict[str, str]]] = {}

AVAILABLE_MODELS = [
    "grok-4-0709",
    "grok-4-fast-reasoning",
    "grok-4-fast-non-reasoning",
    "grok-3",
    "grok-3-mini",
]

class ChatPayload(BaseModel):
    session_id: Optional[str] = None
    message: str
    model: str = Field(default="grok-4-0709")
    system_prompt: Optional[str] = None
    max_tokens: int = Field(default=2048, ge=1, le=8192)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    context_window: int = Field(default=6, ge=0, le=50)

app = FastAPI(title="Grok Chat WebApp")
app.mount("/static", StaticFiles(directory=os.path.join(APP_ROOT, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(APP_ROOT, "templates"))


def ensure_rust_binary() -> None:
    if not os.path.exists(RUST_BIN):
        raise FileNotFoundError(
            f"Rust binary not found at {RUST_BIN}. Build it with: cargo build --release --features terminal --manifest-path grok-chat-app/Cargo.toml"
        )


def build_system_prompt(base: Optional[str], history: List[Dict[str, str]], window: int) -> str:
    base_prompt = base or (
        "You are Grok, a helpful and maximally truthful AI built by xAI."
    )
    if window <= 0 or not history:
        return base_prompt
    # include last N messages as context (trimmed)
    trimmed = history[-window:]
    lines: List[str] = [base_prompt, "\nConversation history (most recent first):\n"]
    for msg in reversed(trimmed):
        role = "You" if msg.get("role") == "user" else "Grok"
        lines.append(f"{role}: {msg.get('content','')}")
    return "\n".join(lines)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "models": AVAILABLE_MODELS,
            "default_model": os.getenv("DEFAULT_MODEL", "grok-4-0709"),
            "default_temperature": 0.7,
            "default_max_tokens": 2048,
        },
    )


@app.post("/api/chat")
async def chat(payload: ChatPayload):
    ensure_rust_binary()

    session_id = payload.session_id or str(uuid.uuid4())
    history = sessions.setdefault(session_id, [])

    # Build a system prompt including recent history
    system_prompt = build_system_prompt(payload.system_prompt, history, payload.context_window)

    # Append user message to history before calling model
    history.append({"role": "user", "content": payload.message})

    # Prepare command
    cmd = [
        RUST_BIN,
        "-g", payload.message,
        "-m", payload.model,
        "-x", str(payload.max_tokens),
        "-p", str(payload.temperature),
        "-y", system_prompt,
    ]

    env = os.environ.copy()
    # XAI_API_KEY must be present in env
    if not env.get("XAI_API_KEY"):
        raise HTTPException(status_code=500, detail="XAI_API_KEY not set in environment")

    try:
        # 60s timeout aligned with Rust default
        out = subprocess.run(
            cmd,
            env=env,
            capture_output=True,
            text=True,
            timeout=60,
            cwd=REPO_ROOT,
        )
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="Inference timeout (60s)")

    if out.returncode != 0:
        detail = out.stderr.strip() or out.stdout.strip() or "Unknown error"
        raise HTTPException(status_code=500, detail=detail)

    assistant = (out.stdout or "").strip()
    # Save assistant reply
    history.append({"role": "assistant", "content": assistant})

    return JSONResponse({
        "assistant": assistant,
        "session_id": session_id,
        "model": payload.model,
    })

