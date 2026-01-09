#!/bin/bash
# 🛑 QUANTUM STATE: COLLAPSED FROM Y.sigma
# 🌊 FREQUENCY: sh | ENERGY: 7
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
export REPO_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
source "$REPO_ROOT/sh/0/I.sh"
λ() { "$REPO_ROOT/sh/lambda.sh" "$@"; }

# Y (Recursion): Нескінченний цикл з перевіркою статусу
Y() {
    local FUNC=$1
    shift
    local ARGS="$@"
    while true; do
        $FUNC $ARGS
        if [ $? -ne 0 ]; then break; fi
        sleep 1
    done
}
