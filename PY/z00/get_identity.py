import re
import hashlib
def get_identity(text: str, glyph_name: str) -> bytes:
    id_match = re.search(r"🧬IDENTITY:\s*([a-fA-F0-9]{64})", text)
    if id_match: return bytes.fromhex(id_match.group(1))
    
    first_block_match = re.search(r"@\[\w+\]\n(.*?)\n(?=@\[|$)", text, re.DOTALL)
    content = first_block_match.group(1).strip() if first_block_match else glyph_name
    return hashlib.sha256(content.encode("utf-8")).digest()
