#!/bin/bash
# 🛑 QUANTUM STATE: COLLAPSED FROM E.sigma
# 🌊 FREQUENCY: sh | ENERGY: 0
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
export REPO_ROOT="$(dirname "$SCRIPT_DIR")"
source "$REPO_ROOT/sh/0/I.sh"
λ() { "$REPO_ROOT/sh/lambda.sh" "$@"; }

# E (Effect): Виконує команду, але пропускає оригінальний потік далі
E() {
    local cmd="$1"
    tee >(eval "$cmd" > /dev/null)
}
