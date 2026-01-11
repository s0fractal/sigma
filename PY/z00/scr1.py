import hashlib
import re

# Σ-GLYPH SCR-1: Stable Canonical Resonance
# V2.3.1 - Standard Implementation

def canonicalize_sigma(text: str) -> bytes:
    """
    SCR-1 Canonicalization Algorithm:
    1. Normalize CRLF to LF.
    2. Remove trailing whitespace on each line.
    3. Remove the 🧬IDENTITY header line anywhere.
    4. Remove everything from the last '\n🔒:' or '\nCHECKSUM:' to the end.
    5. Ensure the result ends with exactly one '\n'.
    6. Return UTF-8 bytes.
    """
    # 1. Normalize Line Endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    
    # 2. Strip Seal (from the last \n🔒: or \nCHECKSUM: to the end)
    # We find the last occurrence of either marker preceded by a newline.
    markers = ["\n🔒:", "\nCHECKSUM:"]
    last_idx = -1
    for m in markers:
        idx = text.rfind(m)
        if idx > last_idx:
            last_idx = idx
            
    if last_idx != -1:
        text = text[:last_idx]
    
    # 3. Process lines: trailing whitespace and Identity filtering
    lines = text.split("\n")
    processed_lines = []
    for line in lines:
        stripped_line = line.rstrip()
        # Remove 🧬IDENTITY or IDENTITY lines
        if re.match(r"^(🧬IDENTITY:|IDENTITY:)", stripped_line.strip()):
            continue
        processed_lines.append(stripped_line)
        
    # 4. Join and ensure single final newline
    # Note: strip() might be too aggressive if leading/trailing empty lines are normative.
    # The standard says "remove trailing whitespace on each line".
    # And "Identity MUST NOT depend on... aesthetic markers".
    # But it also says "CanonicalBody = entire file excluding...".
    # Let's join and then handle the final newline.
    
    # Re-join
    result = "\n".join(processed_lines)
    
    # Ensure final newline exists and is exactly one '\n'
    # First, strip existing trailing newlines to be safe, then add one.
    result = result.rstrip("\n") + "\n"
    
    return result.encode("utf-8")

def get_node_hash(text: str) -> str:
    """Convenience for SHA-256 of canonical bytes."""
    return hashlib.sha256(canonicalize_sigma(text)).hexdigest()
