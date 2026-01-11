# parse_physics: Extract entropy from stdin/file
parse_physics() {
    local file_content
    if [ -f "$1" ]; then file_content=$(cat "$1"); else file_content=$(cat -); fi
    echo "$file_content" | awk '/⚖️PHYSICS:/ {p=1; next} p && /---/ {p=0} p {print}' | sed 's/[^a-zA-Z0-9:]//g' | awk -F':' '{print $1"="$2}' | xargs | tr ' ' '\n'
}
