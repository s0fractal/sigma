#!/bin/bash
# 🛑 QUANTUM STATE: COLLAPSED FROM W.sigma
# 🌊 FREQUENCY: sh | ENERGY: 2
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
export REPO_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
λ() { "$REPO_ROOT/sh/lambda.sh" "$@"; }
# W (Fork/Witness): Дублює потік у файл або процес, повертає потік далі
# Usage: echo "data" | W "log.txt" | ...
W() {
    local TARGET=$1
    if [ -z "$TARGET" ]; then
        tee # Просто дублює в stdout (подвійний потік)
    else
        tee "$TARGET"
    fi
}
