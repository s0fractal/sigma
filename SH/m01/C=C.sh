# C (Flip): f x y -> f y x
C() {
    local f="$1"
    local arg1="$2"
    local arg2="$3"
    eval "$f" "$arg2" "$arg1"
}
```
