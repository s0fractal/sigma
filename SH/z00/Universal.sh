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
    
    # Check if f is a function or command
    if ! command -v "$f" >/dev/null 2>&1; then
        # If not a command, treat as literal/echo
        if [ $# -gt 0 ]; then
            λ "$f" "$@"
        else
            echo "$f"
        fi
        return
    fi

    # Recursive Pipe
    if [ $# -gt 0 ]; then
        local result=$( "$f" "$x" )
        λ "$result" "$@"
    else
        "$f" "$x"
    fi
}
