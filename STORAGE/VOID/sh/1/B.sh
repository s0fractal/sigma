#!/bin/bash
#🛑 QUANTUM STATE: COLLAPSED FROM B.sigma
#🌊 FREQUENCY: sh | ENERGY: 1
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
export REPO_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
λ() { "$REPO_ROOT/sh/lambda.sh" "$@"; }

# B (Compose): f(g(x)) -> g | f
B() {
    local f="$1"
    local g="$2"
    eval "$g" | eval "$f"
}
