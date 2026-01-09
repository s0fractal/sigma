#!/bin/bash
# 🛑 QUANTUM STATE: COLLAPSED FROM I.sigma
# 🌊 FREQUENCY: sh | ENERGY: 0
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
export REPO_ROOT="$(dirname "$SCRIPT_DIR")"
λ() { "$REPO_ROOT/sh/lambda.sh" "$@"; }

# I (Identity): Просто пропускає дані далі
I() {
    cat -
}
