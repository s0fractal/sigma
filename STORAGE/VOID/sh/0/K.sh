#!/bin/bash
# 🛑 QUANTUM STATE: COLLAPSED FROM K.sigma
# 🌊 FREQUENCY: sh | ENERGY: 0
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
export REPO_ROOT="$(dirname "$SCRIPT_DIR")"
source "$REPO_ROOT/sh/0/I.sh"
λ() { "$REPO_ROOT/sh/lambda.sh" "$@"; }

# K (Constant): Ігнорує потік, видає аргумент
K() {
    cat > /dev/null
    echo "$1"
}
