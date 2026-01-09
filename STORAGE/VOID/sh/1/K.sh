#!/bin/bash
#🛑 QUANTUM STATE: COLLAPSED FROM K.sigma
#🌊 FREQUENCY: sh | ENERGY: 1
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
export REPO_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
λ() { "$REPO_ROOT/sh/lambda.sh" "$@"; }

# K (Constant): Ігнорує потік, видає аргумент
K() {
    cat > /dev/null
    echo "$1"
}
