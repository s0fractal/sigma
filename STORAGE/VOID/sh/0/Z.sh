#!/bin/bash
# 🛑 QUANTUM STATE: COLLAPSED FROM Z.sigma
# 🌊 FREQUENCY: sh | ENERGY: 0
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
export REPO_ROOT="$(dirname "$SCRIPT_DIR")"
source "$REPO_ROOT/sh/0/I.sh"
λ() { "$REPO_ROOT/sh/lambda.sh" "$@"; }

# Z (Wait): Засинає на вказаний час
Z() {
    sleep "$1"
    cat -
}
