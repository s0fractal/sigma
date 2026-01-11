```python
def entropy_to_stratum(entropy: int) -> str:
    if entropy == -1 or entropy == 0: return "z00"
    prefix = "m" if entropy < 0 else "p"
    bucket = abs(entropy) // 1024
    if bucket > 32: bucket = 32
    return f"{prefix}{bucket:02}"
```
