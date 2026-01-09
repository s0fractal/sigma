#!/bin/bash
#🛑 QUANTUM STATE: COLLAPSED FROM S.sigma
#🌊 FREQUENCY: sh | ENERGY: 1
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
export REPO_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
λ() { "$REPO_ROOT/sh/lambda.sh" "$@"; }

# S (Fuse): x z (y z)
S() {
    local f="$1"
    local g="$2"
    local z="$3"
    local gz=$(eval "$g" "$z")
    eval "$f" "$z" "$gz"
}
