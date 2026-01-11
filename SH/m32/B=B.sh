source \"$REPO_ROOT//m/3/2///S/A/T/O/S/H/I/\"
source \"$REPO_ROOT//m/3/2///I/=/I/\"
source \"$REPO_ROOT//m/3/2///S/=/S/\"
source \"$REPO_ROOT//m/3/2///K/=/K/\"

# 🔗 Shell implementation
I() {
    printf '%s\n' "$1"
}
# 🔗 Shell implementation
S() {
    local f="$1"
    local g="$2"
    local x="$3"
    echo "S-Fusion: ($f $x) ($g $x)"
}
# 🔗 Shell implementation
K() {
    printf '%s\n' "$1"
}

# 🔗 Shell implementation
B() {
    local f="$1"
    local g="$2"
    local x="$3"
    echo "B-Composition: $f ($g $x)"
}
