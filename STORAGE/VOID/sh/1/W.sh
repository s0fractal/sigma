#!/bin/bash
#🛑 QUANTUM STATE: COLLAPSED FROM W.sigma
#🌊 FREQUENCY: sh | ENERGY: 1
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
export REPO_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
λ() { "$REPO_ROOT/sh/lambda.sh" "$@"; }

# W (Witness): Дублює потік
W() {
    tee >(cat)
}
