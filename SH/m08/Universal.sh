# λ Portal (Polymorphic Dispatcher)
λ() {
    local x="$1"
    shift
    if [ $# -eq 0 ]; then
        echo "$x"
        return
    fi
    
    local f="$1"
    shift
    
    # Recursive Pipe
    if [ $# -gt 0 ]; then
        local result=$(eval "$f" "$x")
        λ "$result" "$@"
    else
        eval "$f" "$x"
    fi
}
```
