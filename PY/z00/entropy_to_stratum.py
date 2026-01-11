def entropy_to_stratum(entropy: int) -> str:
    if entropy == -1: return "z00"
    if entropy == 0: return "m00"
    prefix = "m" if entropy < 0 else "p"
    bucket = abs(entropy) // 1024
    return f"{prefix}{bucket:02}"
