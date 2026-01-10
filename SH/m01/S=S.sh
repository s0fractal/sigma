# S (Fuse): x z (y z)
S() {
    local f="$1"
    local g="$2"
    local z="$3"
    local gz=$(eval "$g" "$z")
    eval "$f" "$z" "$gz"
}
```
