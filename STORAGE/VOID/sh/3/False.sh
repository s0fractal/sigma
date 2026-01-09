#!/bin/bash
#🛑 QUANTUM STATE: COLLAPSED FROM False.sigma
#🌊 FREQUENCY: sh | ENERGY: 3
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
export REPO_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
source "$REPO_ROOT/sh/2/F.sh"
λ() { "$REPO_ROOT/sh/lambda.sh" "$@"; }

# False: Alias for F
False() {
    F "$@"
}
