#!/usr/bin/env bash
# OPGROK CLI — craft, run, and build SuperGrok harnesses from the clone root.
# Resolve this script (follow the ./opgrok symlink) then treat that as repo root.
set -euo pipefail

_src="${BASH_SOURCE[0]}"
while [[ -L "${_src}" ]]; do
    _dir="$(cd -- "$(dirname -- "${_src}")" &>/dev/null && pwd)"
    _src="$(readlink "${_src}")"
    [[ "${_src}" != /* ]] && _src="${_dir}/${_src}"
done
SCRIPT_DIR="$(cd -- "$(dirname -- "${_src}")" &>/dev/null && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
cd "${REPO_ROOT}"

PY=(python3)
CRAFT="${REPO_ROOT}/core/tools/craft_harness.py"
BUILD="${REPO_ROOT}/core/tools/build_harness.py"
RUN="${REPO_ROOT}/core/tools/run_harness.py"
APEX="${REPO_ROOT}/core/tools/apex_cli.py"
VALIDATE="${REPO_ROOT}/core/tools/validate_supergroks.py"

die() { echo "error: $*" >&2; exit 1; }

load_env() {
    local envf="${REPO_ROOT}/.env"
    [[ -f "${envf}" ]] || return 0
    while IFS='=' read -r key value; do
        [[ "${key}" =~ ^[A-Z_][A-Z0-9_]*$ ]] || continue
        value="${value%\'}"; value="${value#\'}"
        value="${value%\"}"; value="${value#\"}"
        if [[ -z "${!key:-}" ]]; then
            export "${key}=${value}"
        fi
    done < <(grep -E '^[A-Z_][A-Z0-9_]*=' "${envf}" || true)
}

craft_harness() {
    local goal="${*:-}"
    [[ -n "${goal}" ]] || die "usage: opgrok craft \"<goal>\""
    "${PY[@]}" "${APEX}" detect "${goal}" || true
    "${PY[@]}" "${CRAFT}" "${goal}"
}

apex_cmd() {
    local goal="${*:-}"
    [[ -n "${goal}" ]] || die "usage: opgrok apex \"<goal>\""
    "${PY[@]}" "${APEX}" detect "${goal}"
    "${PY[@]}" "${CRAFT}" "${goal}"
}

build_harness_cmd() {
    local slug="${1:-}"
    shift || true
    [[ -n "${slug}" ]] || die "usage: opgrok build <slug> [--install]"
    "${PY[@]}" "${BUILD}" "${slug}" "$@"
}

run_harness_cmd() {
    local slug="${1:-}"
    shift || true
    [[ -n "${slug}" ]] || die "usage: opgrok run <slug> [--goal ...] [--dry-run]"
    local bin="${REPO_ROOT}/core/binaries/${slug}/bin/opgrok-${slug}"
    if [[ -x "${bin}" ]]; then
        exec "${bin}" "$@"
    fi
    "${PY[@]}" "${RUN}" "${slug}" --repo "${REPO_ROOT}" "$@"
}

list_harnesses() {
    local root="${REPO_ROOT}/core/binaries"
    local reg="${root}/registry.json"
    if [[ -f "${reg}" ]]; then
        cat "${reg}"
        return 0
    fi
    if [[ ! -d "${root}" ]]; then
        echo "no harnesses yet — craft one with: opgrok craft \"<goal>\""
        return 0
    fi
    local found=0
    for d in "${root}"/*/; do
        [[ -d "${d}" ]] || continue
        local slug
        slug="$(basename "${d}")"
        [[ "${slug}" == _* ]] && continue
        echo "${slug}"
        found=1
    done
    [[ "${found}" -eq 1 ]] || echo "no harnesses yet — craft one with: opgrok craft \"<goal>\""
}

show_usage() {
    cat << 'EOF'
OPGROK — SuperGrok harness factory (CLI)

  craft "<goal>"              Hire SuperGroks, seal WC, write the package
  apex "<goal>"               Detect mode, then craft
  run <slug> [--dry-run]      Live Grok run (or package-law dry-run)
  build <slug> [--install]    Compile; optional copy to ~/.opgrok/bin
  harnesses                   List packages in this clone
  route "<intent>"            Preview matching SuperGroks
  validate                    Check the skill catalog
  optimize <slug>             Isolate crate before cargo build
  howto                       Factory card
  learn                       Lessons from past crafts

A fresh clone:

  cp .env.example .env          # set XAI_API_KEY
  ./opgrok craft "your goal"
  ./opgrok run <slug> --dry-run
  ./opgrok run <slug>           # live; needs the key

craft does not call the API. A product binary exists only after a live
run harvests sources and cargo --require-cargo succeeds.

Docs: README.md · core/skills/opgrok/SKILL.md · core/harness/SPEC.md
EOF
}

COMMAND="${1:-help}"
case "${COMMAND}" in
    craft|@opgrok|opgrok)
        shift || true
        craft_harness "$@"
        ;;
    apex|mode)
        shift || true
        apex_cmd "$@"
        ;;
    howto|how-to)
        "${PY[@]}" "${APEX}" howto
        ;;
    learn)
        "${PY[@]}" "${APEX}" learn
        ;;
    build)
        shift || true
        build_harness_cmd "$@"
        ;;
    run)
        shift || true
        load_env
        run_harness_cmd "$@"
        ;;
    install)
        shift || true
        build_harness_cmd "${1:-}" --install
        ;;
    harnesses|bins)
        list_harnesses
        ;;
    route)
        shift || true
        "${PY[@]}" "${APEX}" route "$*"
        ;;
    validate)
        "${PY[@]}" "${VALIDATE}"
        ;;
    optimize)
        shift || true
        slug="${1:-}"
        [[ -n "${slug}" ]] || die "usage: opgrok optimize <slug>"
        PYTHONPATH="${REPO_ROOT}/core${PYTHONPATH:+:$PYTHONPATH}" \
            "${PY[@]}" -c "from toolkit.rust_opt import optimize_crate; import json; print(json.dumps(optimize_crate('${slug}'), indent=2))"
        ;;
    help|h|--help|-h)
        show_usage
        ;;
    *)
        if [[ "${COMMAND}" != help ]]; then
            craft_harness "$@"
        else
            show_usage
            exit 1
        fi
        ;;
esac
