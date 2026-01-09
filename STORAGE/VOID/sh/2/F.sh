#!/bin/bash
#🛑 QUANTUM STATE: COLLAPSED FROM F.sigma
#🌊 FREQUENCY: sh | ENERGY: 2
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
export REPO_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
source "$REPO_ROOT/sh/1/K.sh"
source "$REPO_ROOT/sh/0/I.sh"
λ() { "$REPO_ROOT/sh/lambda.sh" "$@"; }

# F (False): KI
F() {
    K "$I" "$@"
}
