#!/usr/bin/env bash
set -euo pipefail

# s0fractal Transmuter v1.0
# Melts Rust into WASM and injects it into TypeScript nodes.

LAYER=${1:-}
if [ -z "$LAYER" ]; then
  echo "Usage: λ transmute <layer>"
  exit 1
fi

REPO_ROOT=$(git rev-parse --show-toplevel)
RS_DIR="$REPO_ROOT/rs/$LAYER"
TS_DIR="$REPO_ROOT/ts/$LAYER"
WASM_OUT="$TS_DIR/wasm"

echo "🟣 Transmuting Layer $LAYER: RS -> WASM..."

if [ ! -d "$RS_DIR" ]; then
  echo "❌ Source (RS) not found."
  exit 1
fi

echo "   🔥 Melting Metal..."
(cd "$RS_DIR" && cargo build --release --target wasm32-unknown-unknown --quiet)

BINARY=$(find "$RS_DIR/target/wasm32-unknown-unknown/release" -name "*.wasm" | head -n 1 || true)
NAME=$(basename "$BINARY" .wasm)

if [ -z "$BINARY" ]; then
  echo "❌ Transmutation failed (Compilation error)."
  exit 1
fi

echo "   💉 Injecting Signal into TS..."
mkdir -p "$WASM_OUT"
cp "$BINARY" "$WASM_OUT/$NAME.wasm"

cat << TS_EOF > "$WASM_OUT/$NAME.ts"
// 🟣 Liquid Signal Adapter
// Source: $NAME.wasm

const wasmCode = await Deno.readFile(new URL("./$NAME.wasm", import.meta.url));
const wasmModule = await WebAssembly.instantiate(wasmCode);

export const ${NAME} = wasmModule.instance.exports;
TS_EOF

echo "✅ Layer $LAYER is now flowing with power."
