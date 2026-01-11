import re
def parse_physics(text: str) -> dict:
    physics = {"OP": 0, "FLAGS": 0, "PHASE": 0, "AMPLITUDE": 0, "ENTROPY": 0}
    phys_match = re.search(r"(?:⚖️)?PHYSICS:\s*\n((?:\s+[\w\W]+?:\s*[\-\dxA-F]+\n?)*)", text, re.MULTILINE)
    if phys_match:
        block = phys_match.group(1)
        for line in block.split("\n"):
            if ":" in line:
                key, val = line.split(":", 1)
                key = re.sub(r'[^\w]', '', key).strip().upper()
                val = val.strip()
                try:
                    # EXACT MATCH ONLY
                    if key in physics:
                        if val.startswith("0x"): physics[key] = int(val, 16)
                        else: physics[key] = int(val)
                except: continue
    return physics
