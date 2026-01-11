source \"$REPO_ROOT//m/3/2///S/A/T/O/S/H/I/\"
source \"$REPO_ROOT//m/3/2///W/=/W/\"
source \"$REPO_ROOT//m/3/2///I/=/I/\"

# 🔗 Shell implementation
W() {
    local f="$1"
    local x="$2"
    echo "W-Fork: $f $x $x"
}
# 🔗 Shell implementation
I() {
    printf '%s\n' "$1"
}

# 🔗 Shell implementation
M() {
    local x="$1"
    $x $x
}
