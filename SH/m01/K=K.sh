# K (Constant): Ігнорує потік, видає аргумент
K() {
    cat > /dev/null
    echo "$1"
}
```
