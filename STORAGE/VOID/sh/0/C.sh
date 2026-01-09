#!/bin/bash
# 🛑 QUANTUM STATE: COLLAPSED FROM C.sigma
# 🌊 FREQUENCY: sh | ENERGY: 0
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
export REPO_ROOT="$(dirname "$SCRIPT_DIR")"
source "$REPO_ROOT/sh/0/I.sh"
λ() { "$REPO_ROOT/sh/lambda.sh" "$@"; }

# C (Flip): f x y -> f y x
C() {
    local f="$1"
    local arg1="$2"
    local arg2="$3"
    eval "$f" "$arg2" "$arg1"
}
