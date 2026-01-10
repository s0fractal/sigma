#!/bin/bash
# 🧬 SIGMA GRAPH EXTRACTOR
# Scans .sigma files and generates a Mermaid diagram of the SOURCE supply chain.

REPO_ROOT="/Users/s0fractal/void"
SIGMA_DIR="$REPO_ROOT/sigma"
OUTPUT_FILE="$REPO_ROOT/sigma/graph.md"

echo "# Sigma Dependency Graph 🧬🕸️📊" > "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo '```mermaid' >> "$OUTPUT_FILE"
echo "graph TD" >> "$OUTPUT_FILE"

# Process each .sigma file
find "$SIGMA_DIR" -maxdepth 1 -name "*.sigma" | while read -r file; do
    # Extract Glyph/Name
    NAME=$(basename "$file" .sigma)
    
    # Extract FM
    FM=$(awk '/^---$/ {count++; next} count==1 {print}' "$file")
    ENERGY=$(echo "$FM" | grep "^⚡ENERGY:" | cut -d':' -f2 | xargs)
    GLYPH=$(echo "$FM" | grep "^GLYPH:" | cut -d':' -f2 | xargs)
    [ -z "$GLYPH" ] && GLYPH="$NAME"
    
    # Node definition with Energy
    NODE_ID="${NAME}"
    echo "  ${NODE_ID}[\"$GLYPH (E$ENERGY)\"]" >> "$OUTPUT_FILE"
    
    # Extract Sources
    echo "$FM" | sed -n '/^SOURCE:/,/^[A-Z]\|---/p' | grep "origin:" | cut -d':' -f2- | while read -r origin_line; do
        origin=$(echo "$origin_line" | xargs)
        if [ -n "$origin" ] && [ "$origin" != "null" ]; then
            # If literal path, clean it up
            if [[ "$origin" =~ [/.] ]]; then
                CLEAN_ORIGIN=$(basename "$origin" | cut -d'.' -f1)
            else
                CLEAN_ORIGIN="$origin"
            fi
            echo "  ${CLEAN_ORIGIN} --> ${NODE_ID}" >> "$OUTPUT_FILE"
        fi
    done
done

echo '```' >> "$OUTPUT_FILE"

echo "✅ Graph generated at $OUTPUT_FILE"
