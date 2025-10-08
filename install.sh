#!/usr/bin/env bash
# OPGROK Installation - One gentle command to prepare everything

echo "🌟 Welcome to OPGROK"
echo "Setting up your AI workflow automation platform..."
echo ""

# Add opgrok to PATH for this session
REPO_ROOT="$(pwd)"
export PATH="${REPO_ROOT}:${PATH}"

# Make opgrok directly executable
chmod +x "${REPO_ROOT}/opgrok" 2>/dev/null || true
chmod +x "${REPO_ROOT}/scripts/opgrok.sh"

# Create .env if missing
if [[ ! -f .env ]] && [[ -f .env.example ]]; then
    cp .env.example .env
    echo "📝 Created .env from template"
    echo "   Please add your XAI_API_KEY:"
    echo "   nano .env"
    echo ""
fi

# Add to shell profile for permanent PATH
SHELL_RC="${HOME}/.zshrc"
if [[ -f "${HOME}/.bashrc" ]]; then
    SHELL_RC="${HOME}/.bashrc"
fi

OPGROK_ALIAS="alias opgrok='${REPO_ROOT}/scripts/opgrok.sh'"

if ! grep -q "opgrok" "${SHELL_RC}" 2>/dev/null; then
    echo "" >> "${SHELL_RC}"
    echo "# OPGROK - AI Workflow Automation" >> "${SHELL_RC}"
    echo "${OPGROK_ALIAS}" >> "${SHELL_RC}"
    echo "✅ Added opgrok to your shell profile"
else
    echo "✅ opgrok already in shell profile"
fi

echo ""
echo "🎉 Installation complete!"
echo ""
echo "To use opgrok command now:"
echo "  source ${SHELL_RC}"
echo "  opgrok start"
echo ""
echo "Or directly:"
echo "  bash scripts/opgrok.sh start"
echo "  ./scripts/opgrok.sh start"
echo ""
echo "Your familiar friend still works:"
echo "  bash scripts/run_n8n_local.sh"
echo ""
