#!/usr/bin/env bash
# OPGROK install — wire CLI + paths for nested monorepo layout

set -euo pipefail

echo "OPGROK setup"
echo "============"
echo "Kernel: @opgrok harnesses (core/) · Apps: optional UI shell (apps/)"
echo ""

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "${REPO_ROOT}"

chmod +x "${REPO_ROOT}/opgrok" 2>/dev/null || true
chmod +x "${REPO_ROOT}/ops/scripts/opgrok.sh"
chmod +x "${REPO_ROOT}/core/tools/"*.py 2>/dev/null || true

if [[ ! -f .env ]] && [[ -f .env.example ]]; then
  cp .env.example .env
  echo "Created .env — set XAI_API_KEY (must be enabled at console.x.ai)"
fi

SHELL_RC="${HOME}/.zshrc"
[[ -f "${HOME}/.bashrc" ]] && SHELL_RC="${HOME}/.bashrc"

OPGROK_ALIAS="alias opgrok='${REPO_ROOT}/ops/scripts/opgrok.sh'"
if ! grep -q "opgrok" "${SHELL_RC}" 2>/dev/null; then
  {
    echo ""
    echo "# OPGROK"
    echo "${OPGROK_ALIAS}"
  } >> "${SHELL_RC}"
  echo "Added opgrok alias to ${SHELL_RC}"
else
  echo "opgrok alias already present in ${SHELL_RC}"
fi

echo ""
echo "Layout:"
echo "  core/   SuperGroks + harness craft/run + toolkit + Rust"
echo "  apps/   optional web / chat / n8n"
echo "  ops/    this installer + opgrok.sh"
echo ""
echo "Next:"
echo "  source ${SHELL_RC}   # if alias was added"
echo "  # set XAI_API_KEY in .env"
echo "  python3 core/tools/craft_harness.py \"your goal\""
echo "  python3 core/tools/run_harness.py <slug> --dry-run"
echo "  # docs: README.md  LAYOUT.md  core/README.md"
