# --- Stage 1: Build Rust binary ---
FROM rust:1.79 as rust-builder
WORKDIR /app

# Copy entire repo to have Cargo.toml and sources
COPY . .

# Build the Rust CLI with terminal feature
RUN cargo build --release --features terminal --manifest-path grok-chat-app/Cargo.toml

# --- Stage 2: Python app ---
FROM python:3.11-slim as runtime
WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates && rm -rf /var/lib/apt/lists/*

# Copy Python app
COPY webapp/requirements.txt ./webapp/requirements.txt
RUN pip install --no-cache-dir -r webapp/requirements.txt
COPY webapp /app/webapp

# Copy Rust binary
COPY --from=rust-builder /app/grok-chat-app/target/release/grok-chat-app /app/grok-chat-app

ENV PATH="/app:${PATH}"
ENV PYTHONUNBUFFERED=1

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
