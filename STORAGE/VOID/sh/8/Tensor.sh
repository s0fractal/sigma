#!/bin/bash
# 🛑 QUANTUM STATE: COLLAPSED FROM Tensor.sigma
# 🌊 FREQUENCY: sh | ENERGY: 8
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
export REPO_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
λ() { "$REPO_ROOT/sh/lambda.sh" "$@"; }
# --- 0. State ---
MATRIX_FILE="$REPO_ROOT/sigma/matrix.sigma"
export VECTOR_SPACE=()

# --- LOAD MATRIX (Combinator Pipeline) ---
# 1. Читаємо файл
# 2. Фільтруємо таблицю
# 3. Форматуємо вектори
# 4. Колапсуємо в масив

_load_matrix() {
    if [ ! -f "$MATRIX_FILE" ]; then return 1; fi

    while IFS= read -r vec; do
        VECTOR_SPACE+=("$vec")
    done < <(cat "$MATRIX_FILE" | \
        grep "|" | \
        grep -v "\-\-\-" | \
        grep -v "ID" | \
        while IFS='|' read -r id type path hex syn mute lift mass entropy imp; do
            # Clean values (Symbolic Trim)
            id_t=$(echo "$id" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')
            type_t=$(echo "$type" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')
            path_t=$(echo "$path" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')
            hex_t=$(echo "$hex" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')
            syn_t=$(echo "$syn" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')
            mute_t=$(echo "$mute" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//; s/^\"//; s/\"$//')
            lift_t=$(echo "$lift" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//; s/^\"//; s/\"$//')
            mass_t=$(echo "$mass" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')
            entropy_t=$(echo "$entropy" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')
            imp_t=$(echo "$imp" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//; s/^\"//; s/\"$//')
            
            echo "$id_t|$type_t|$path_t|$hex_t|$syn_t|$mute_t|$lift_t|$mass_t|$entropy_t|$imp_t"
        done)
}

_load_matrix

# --- TENSOR OPERATIONS ---

# get_vector <id>
get_vector() {
    local QUERY_ID=$1
    for VEC in "${VECTOR_SPACE[@]}"; do
        if [[ "$(echo "$VEC" | cut -d'|' -f1)" == "$QUERY_ID" ]]; then
            echo "$VEC"
            return
        fi
    done
}

# project_dim <index>
project_dim() {
    local IDX=$(( $1 + 1 ))
    for VEC in "${VECTOR_SPACE[@]}"; do
        echo "$VEC" | cut -d'|' -f$IDX
    done
}

# --- ENVIRONMENT EXPORT ---
export ALL_DIMS=($(project_dim 0))
export ALL_LAYERS=(0 1 2 3 4 5 6 7 8)
