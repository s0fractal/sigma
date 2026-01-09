#!/bin/bash
#🛑 QUANTUM STATE: COLLAPSED FROM True.sigma
#🌊 FREQUENCY: sh | ENERGY: 3
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
export REPO_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
source "$REPO_ROOT/sh/1/K.sh"
λ() { "$REPO_ROOT/sh/lambda.sh" "$@"; }

# True: Alias for K
True() {
    K "$@"
}
