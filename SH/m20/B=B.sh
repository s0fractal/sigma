# B (Compose): f(g(x)) -> g | f
B() {
    local f="$1"
    local g="$2"
    eval "$g" | eval "$f"
}
