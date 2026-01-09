#!/bin/bash
# s0fractal Ribosome v1.0
# Fetches proteins (WASM) from DNS TXT.
# Usage: λ feed <glyph>

set -euo pipefail

GLYPH="${1:-}"
DOMAIN="${S0FRACTAL_DNS_DOMAIN:-s0fractal.io}"
CACHE_DIR="$HOME/.cache/s0fractal/proteins"

if [ -z "$GLYPH" ]; then
    echo "Usage: ./ribosome.sh <glyph>"
    exit 1
fi

mkdir -p "$CACHE_DIR"
CACHE_FILE="$CACHE_DIR/$GLYPH.wasm"
META_FILE="$CACHE_DIR/$GLYPH.meta"

echo "🧬 Ribosome: seeking protein '$GLYPH'..."

# 1. Local cache
if [ -f "$CACHE_FILE" ]; then
    echo "   ⚡ Found in local cache."
    echo "$CACHE_FILE"
    exit 0
fi

# 2. DNS query
RECORDS=$(dig +short TXT "$GLYPH.sigma.$DOMAIN" | tr -d '"')
if [ -z "$RECORDS" ]; then
    echo "   ❌ Void signal. No DNS record for '$GLYPH'."
    exit 1
fi

echo "   📡 Signal received."

# 3. Parse first record (v=1; t=...)
RECORD=$(echo "$RECORDS" | head -n 1)
TYPE=$(echo "$RECORD" | sed -n 's/.*t=\\([^;]*\\).*/\\1/p')
BODY=$(echo "$RECORD" | sed -n 's/.*b=\\([^;]*\\).*/\\1/p')
REF=$(echo "$RECORD" | sed -n 's/.*ref=\\([^;]*\\).*/\\1/p')
IPFS=$(echo "$RECORD" | sed -n 's/.*ipfs=\\([^;]*\\).*/\\1/p')

if [ "$TYPE" = "p" ] && [ -n "$BODY" ]; then
    echo "   🧪 Synthesizing WASM protein..."
    echo "$BODY" | base64 -d > "$CACHE_FILE"
    echo "   ✅ Protein stored: $CACHE_FILE"
    echo "$CACHE_FILE"
    exit 0
fi

if [ "$TYPE" = "h" ] && [ -n "$REF" ]; then
    echo "   🔗 Host pointer -> $REF"
    echo "REDIRECT:$REF" > "$META_FILE"
    echo "$META_FILE"
    exit 0
fi

if [ "$TYPE" = "s" ] && [ -n "$IPFS" ]; then
    echo "   🧬 Spore pointer -> $IPFS"
    echo "SPORE:$IPFS" > "$META_FILE"
    echo "$META_FILE"
    exit 0
fi

echo "   ⚠️  Unknown or incomplete record: $RECORD"
exit 1
