import os
import re
from pathlib import Path

# Σ-GLYPH GENETIC REPAIR: Mass DNA Purge
M32_DIR = Path("/Users/s0fractal/SIGMA/sigma/m32")

for path in M32_DIR.glob("*.sigma"):
    content = path.read_text(encoding="utf-8")
    if "DNA: - SATOSHI" in content:
        name = path.stem
        print(f"🧬 Repairing DNA: {name}")
        
        # Replace YAML DNA
        content = re.sub(r"DNA: - SATOSHI", f"DNA: {name}", content)
        
        # Replace @[dna] block content
        content = re.sub(r"@\[dna\]\n- SATOSHI", f"@[dna]\n{name}", content)
        
        # Reset checksum for sealing
        content = re.sub(r"🔒:.*", "🔒: VALIDATING...", content)
        
        path.write_text(content, encoding="utf-8")

print("✅ Genetic Repair Complete.")
