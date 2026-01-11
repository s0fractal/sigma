```bash
# entropy_to_stratum: Predict folder from entropy
entropy_to_stratum() {
    local entropy=$1
    if [ "$entropy" -eq -1 ]; then echo "z00"; return; fi
    if [ "$entropy" -eq 0 ]; then echo "m00"; return; fi
    local prefix="p"
    [ "$entropy" -lt 0 ] && prefix="m"
    local abs_e=${entropy#-}
    local bucket=$((abs_e / 1024))
    printf "%s%02d\n" "$prefix" "$bucket"
}
```
