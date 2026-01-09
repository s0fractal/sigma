#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: fractal.sh <name> [options]

Creates a fractal chain topology:
- n-<name> repos (n=0..N) each with sigma as meta/root
- for n>=1, n-<name> embeds (n-1)-<name> as submodule at ./<name>

Options:
  --org <org>        GitHub org/user (default: s0fractal)
  --levels <N>       Max level N (default: 8)
  --sigma <repo>     Sigma repo name (default: sigma)
  --aggregator       Also create <name> repo with submodules 0..N
  --rings            Create ring aggregators per level (e.g. 0,1,2...) for dims
  --dims <csv>       Comma-separated dimensions for --rings (default: ts,rs)
  --ring-sigma       Add sigma as submodule in each ring
  --allow-existing   Allow cloning existing remotes to update structure
  --public           Create repos as public (default)
  --private          Create repos as private
  --ssh              Use git@github.com: URLs
  --https            Use https://github.com/ URLs (default)
  --workdir <path>   Working directory for temp clones (default: ./.fractal-gen/<name>)
  --dry-run          Print commands without executing
  -h, --help         Show this help
EOF
}

NAME=""
ORG="s0fractal"
MAX_LEVEL=8
SIGMA_REPO="sigma"
VISIBILITY="--public"
USE_SSH=0
WORKDIR=""
DRY_RUN=0
MAKE_AGGREGATOR=0
ALLOW_EXISTING=0
RINGS_MODE=0
RING_DIMS_CSV="ts,rs"
RING_INCLUDE_SIGMA=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --org) ORG="$2"; shift 2 ;;
    --levels) MAX_LEVEL="$2"; shift 2 ;;
    --sigma) SIGMA_REPO="$2"; shift 2 ;;
    --aggregator) MAKE_AGGREGATOR=1; shift ;;
    --rings) RINGS_MODE=1; shift ;;
    --dims) RING_DIMS_CSV="$2"; shift 2 ;;
    --ring-sigma) RING_INCLUDE_SIGMA=1; shift ;;
    --allow-existing) ALLOW_EXISTING=1; shift ;;
    --public) VISIBILITY="--public"; shift ;;
    --private) VISIBILITY="--private"; shift ;;
    --ssh) USE_SSH=1; shift ;;
    --https) USE_SSH=0; shift ;;
    --workdir) WORKDIR="$2"; shift 2 ;;
    --dry-run) DRY_RUN=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *)
      if [ -z "$NAME" ]; then
        NAME="$1"
        shift
      else
        echo "Unknown arg: $1" >&2
        usage
        exit 1
      fi
      ;;
  esac
done

if [ -z "$NAME" ]; then
  if [ "$RINGS_MODE" -eq 1 ]; then
    NAME="ring"
  else
    usage
    exit 1
  fi
fi

if ! command -v gh >/dev/null 2>&1; then
  echo "gh is required (GitHub CLI)" >&2
  exit 1
fi
if ! command -v git >/dev/null 2>&1; then
  echo "git is required" >&2
  exit 1
fi

if [ -z "$WORKDIR" ]; then
  WORKDIR="./.fractal-gen/$NAME"
fi

repo_url() {
  local repo="$1"
  if [ "$USE_SSH" -eq 1 ]; then
    echo "git@github.com:$ORG/$repo.git"
  else
    echo "https://github.com/$ORG/$repo.git"
  fi
}

run() {
  if [ "$DRY_RUN" -eq 1 ]; then
    echo "DRY: $*"
  else
    "$@"
  fi
}

repo_exists() {
  gh repo view "$ORG/$1" >/dev/null 2>&1
}

remote_has_refs() {
  local repo="$1"
  local url
  url="$(repo_url "$repo")"
  if [ "$DRY_RUN" -eq 1 ]; then
    return 1
  fi
  git ls-remote --heads "$url" >/dev/null 2>&1
}

ensure_repo() {
  local repo="$1"
  local desc="$2"
  if repo_exists "$repo"; then
    return 0
  fi
  run gh repo create "$ORG/$repo" $VISIBILITY --description "$desc"
}

ensure_seeded() {
  local repo="$1"
  local desc="$2"
  local repo_dir="$WORKDIR/_seed/$repo"
  ensure_repo "$repo" "$desc"
  if remote_has_refs "$repo"; then
    return 0
  fi
  run mkdir -p "$repo_dir"
  if [ "$DRY_RUN" -eq 1 ]; then
    return 0
  fi
  git -C "$repo_dir" init -b main
  git -C "$repo_dir" remote add origin "$(repo_url "$repo")"
  # Minimal skeleton: 0..N + chaos so empty repos are clonable and structured.
  for ((i=0; i<=MAX_LEVEL; i++)); do
    mkdir -p "$repo_dir/$i"
    : > "$repo_dir/$i/.gitkeep"
  done
  mkdir -p "$repo_dir/chaos"
  : > "$repo_dir/chaos/.gitkeep"
  if [ ! -f "$repo_dir/.gitkeep" ]; then
    printf "%s\n" "seed" > "$repo_dir/.gitkeep"
  fi
  git -C "$repo_dir" add .gitkeep
  git -C "$repo_dir" add -A
  git -C "$repo_dir" commit -m "⊕ seed"
  git -C "$repo_dir" push -u origin main
}

init_repo() {
  local repo="$1"
  local dir="$2"
  if remote_has_refs "$repo"; then
    if [ "$ALLOW_EXISTING" -eq 0 ]; then
      echo "Refusing to init $repo: remote has commits (no-clone mode)." >&2
      exit 1
    fi
    run mkdir -p "$(dirname "$dir")"
    run git clone "$(repo_url "$repo")" "$dir"
    return 0
  fi
  run mkdir -p "$dir"
  if [ "$DRY_RUN" -eq 1 ]; then
    return 0
  fi
  git -C "$dir" init -b main
  git -C "$dir" remote add origin "$(repo_url "$repo")"
}

has_submodule_path() {
  local dir="$1"
  local path="$2"
  if [ "$DRY_RUN" -eq 1 ]; then
    return 1
  fi
  if [ -e "$dir/$path/.git" ] || [ -f "$dir/$path/.git" ]; then
    return 0
  fi
  git -C "$dir" config -f .gitmodules --get-regexp "submodule\..*\.path" 2>/dev/null | awk '{print $2}' | grep -qx "$path"
}

add_submodule() {
  local dir="$1"
  local repo="$2"
  local path="$3"
  local url
  url="$(repo_url "$repo")"
  if has_submodule_path "$dir" "$path"; then
    return 0
  fi
  run git -C "$dir" submodule add "$url" "$path"
}

commit_and_push() {
  local dir="$1"
  if [ "$DRY_RUN" -eq 1 ]; then
    return 0
  fi
  if git -C "$dir" diff --quiet && git -C "$dir" diff --cached --quiet; then
    return 0
  fi
  run git -C "$dir" add .gitmodules
  run git -C "$dir" add -A
  run git -C "$dir" commit -m "⊕ fractal scaffold"
  if git -C "$dir" rev-parse --abbrev-ref --symbolic-full-name @{u} >/dev/null 2>&1; then
    run git -C "$dir" push
  else
    run git -C "$dir" push -u origin main
  fi
}

echo "🧬 Fractal generator: $NAME (0..$MAX_LEVEL) in $ORG"
echo "   workdir: $WORKDIR"

run mkdir -p "$WORKDIR"

# Seed sigma if empty so submodule add succeeds.
ensure_seeded "$SIGMA_REPO" "Sigma base for projections"

if [ "$RINGS_MODE" -eq 1 ]; then
  IFS=',' read -r -a RING_DIMS <<< "$RING_DIMS_CSV"

  for ((n=0; n<=MAX_LEVEL; n++)); do
    for dim in "${RING_DIMS[@]}"; do
      repo="${n}-${dim}"
      desc="Ring node $repo"
      ensure_repo "$repo" "$desc"
      repo_dir="$WORKDIR/$repo"
      init_repo "$repo" "$repo_dir"

      if [ "$DRY_RUN" -eq 0 ]; then
        for ((i=0; i<=MAX_LEVEL; i++)); do
          mkdir -p "$repo_dir/$i"
          : > "$repo_dir/$i/.gitkeep"
        done
        mkdir -p "$repo_dir/chaos"
        : > "$repo_dir/chaos/.gitkeep"
      fi

      add_submodule "$repo_dir" "$SIGMA_REPO" "meta/root"

      if [ "$n" -ge 1 ]; then
        add_submodule "$repo_dir" "$((n-1))-$dim" "$dim"
      fi

      commit_and_push "$repo_dir"
    done

    ring_repo="$n"
    ensure_repo "$ring_repo" "Ring $n"
    ring_dir="$WORKDIR/$ring_repo"
    init_repo "$ring_repo" "$ring_dir"

    for dim in "${RING_DIMS[@]}"; do
      add_submodule "$ring_dir" "${n}-${dim}" "$dim"
    done
    if [ "$RING_INCLUDE_SIGMA" -eq 1 ]; then
      add_submodule "$ring_dir" "$SIGMA_REPO" "sigma"
    fi

    commit_and_push "$ring_dir"
  done
else
  # 1) Create and scaffold n-<name> repos (chain)
  for ((n=0; n<=MAX_LEVEL; n++)); do
    repo="${n}-${NAME}"
    desc="Fractal node $repo"
    ensure_repo "$repo" "$desc"
    repo_dir="$WORKDIR/$repo"
    init_repo "$repo" "$repo_dir"

    # Minimal skeleton: 0..N + chaos
    if [ "$DRY_RUN" -eq 0 ]; then
      for ((i=0; i<=MAX_LEVEL; i++)); do
        mkdir -p "$repo_dir/$i"
        : > "$repo_dir/$i/.gitkeep"
      done
      mkdir -p "$repo_dir/chaos"
      : > "$repo_dir/chaos/.gitkeep"
    fi

    # sigma in meta/root
    add_submodule "$repo_dir" "$SIGMA_REPO" "meta/root"

    # For n>=1, add (n-1)-<name> as submodule at ./<name>
    if [ "$n" -ge 1 ]; then
      add_submodule "$repo_dir" "$((n-1))-$NAME" "$NAME"
    fi

    commit_and_push "$repo_dir"
  done

  if [ "$MAKE_AGGREGATOR" -eq 1 ]; then
    ensure_repo "$NAME" "Fractal aggregator $NAME"
    agg_dir="$WORKDIR/$NAME"
    init_repo "$NAME" "$agg_dir"

    if [ "$DRY_RUN" -eq 0 ]; then
      mkdir -p "$agg_dir/chaos"
      : > "$agg_dir/chaos/.gitkeep"
    fi

    for ((n=0; n<=MAX_LEVEL; n++)); do
      add_submodule "$agg_dir" "${n}-${NAME}" "$n"
    done

    commit_and_push "$agg_dir"
  fi
fi

echo "✅ Fractal topology complete."
