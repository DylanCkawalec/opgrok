#!/usr/bin/env bash
# Wire the OPGROK CLI for this clone. Does not touch apps or a UI.
set -euo pipefail

echo "OPGROK setup"
echo "============"

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "${REPO_ROOT}"

chmod +x "${REPO_ROOT}/opgrok" 2>/dev/null || true
chmod +x "${REPO_ROOT}/ops/scripts/opgrok.sh"
chmod +x "${REPO_ROOT}/core/tools/"*.py 2>/dev/null || true

if [[ ! -f .env ]] && [[ -f .env.example ]]; then
  cp .env.example .env
  echo "Created .env — set XAI_API_KEY (enabled at console.x.ai)"
fi

if [[ "${1:-}" == "--alias" ]]; then
  SHELL_RC="${HOME}/.zshrc"
  [[ -f "${HOME}/.bashrc" ]] && SHELL_RC="${HOME}/.bashrc"
  OPGROK_ALIAS="alias opgrok='${REPO_ROOT}/ops/scripts/opgrok.sh'"
  if ! grep -q "opgrok=" "${SHELL_RC}" 2>/dev/null; then
    {
      echo ""
      echo "# OPGROK"
      echo "${OPGROK_ALIAS}"
    } >> "${SHELL_RC}"
    echo "Added opgrok alias to ${SHELL_RC}"
  else
    echo "opgrok alias already present in ${SHELL_RC}"
  fi
fi

echo ""
echo "This clone:"
echo "  core/   SuperGroks + harness craft/run + toolkit + Rust"
echo "  ops/    this installer + ./opgrok"
echo ""
echo "Next:"
echo "  # set XAI_API_KEY in .env"
echo "  python3 core/tools/craft_harness.py \"your goal\""
echo "  python3 core/tools/run_harness.py <slug> --repo . --dry-run"
echo "  python3 core/tools/run_harness.py <slug> --repo ."
echo ""
echo "Optional:  ./ops/install.sh --alias"
echo "Grok Build: ln -sfn \"\$(pwd)/core/skills/opgrok\" ~/.grok/skills/opgrok"
