source \"$REPO_ROOT/m32/SATOSHI\

# Σ-GLYPH Git Binding
alias save="git add . && git commit -m"
alias sync="git pull --rebase && git push"
alias pulse="git log -n 5 --oneline --graph"

# Auto-Archival Command
archive_pulse() {
    local msg=$1
    echo "📦 Archiving Pulse: $msg"
    git add .
    git commit -m "💎 Archival Pulse: $msg"
    git push
}
