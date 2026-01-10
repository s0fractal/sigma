#!/bin/bash
# s0fractal Sovereign Gemini v1.0
# Deps: curl, jq

# Load Vault
[ -f "$HOME/.s0_vault" ] && source "$HOME/.s0_vault"

if [ -z "$GEMINI_API_KEY" ]; then
    echo "❌ Error: GEMINI_API_KEY not found in ~/.s0_vault"
    exit 1
fi

# Read Input
if [ -p /dev/stdin ]; then
    PROMPT=$(cat)
else
    PROMPT="$*"
fi

if [ -z "$PROMPT" ]; then
    echo "Usage: gemini <text>"
    exit 1
fi

# Prepare Payload
JSON=$(jq -n --arg t "$PROMPT" '{contents: [{parts: [{text: $t}]}]}')
MODEL="gemini-2.0-flash-exp" # Або gemini-1.5-flash

# Execute
curl -s "https://generativelanguage.googleapis.com/v1beta/models/$MODEL:generateContent?key=$GEMINI_API_KEY" \
    -H "Content-Type: application/json" \
    -d "$JSON" | \
    jq -r '.candidates[0].content.parts[0].text // .error.message'
