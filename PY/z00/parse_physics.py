```python
import re
def parse_physics(text: str) -> dict:
    physics = {"OP": 0, "FLAGS": 0, "PHASE": 0, "AMPLITUDE": 0, "ENTROPY": 0}
    # Match the header
    header_match = re.search(r"(?:⚖️)?\s*PHYSICS(?:\s*\(Wave Function\))?:?\s*\n+", text, re.MULTILINE)
    if header_match:
        start_idx = header_match.end()
        remaining = text[start_idx:].lstrip("\n")

        # Parse line by line until we hit a non-property line
        found_any = False
        for line in remaining.split("\n"):
            clean_line = line.split("#")[0].strip()
            if not clean_line: continue

            if ":" in clean_line:
                key, val = clean_line.split(":", 1)
                key = re.sub(r'[^\w]', '', key).strip().upper()
                if key in physics:
                    found_any = True
                    val = val.strip()
                    try:
                        if val.startswith("0x"): physics[key] = int(val, 16)
                        else: physics[key] = int(re.search(r'-?\d+', val).group())
                    except: continue
                elif found_any: # If we see a key that's NOT in physics after finding some, it might be a new section
                    break
            else: # No colon -> end of physics block
                break
    return physics
```
