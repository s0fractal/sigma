import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from akasha import SemanticAkasha
import protocol

def test_semantic_resonance():
    print("🧪 Testing Masterman Semantic Resonance (V52.0)...")
    akasha = SemanticAkasha(protocol.ROOT)
    
    # Define semantic shells
    void_shell = {"root": "EMPTY_CENTER", "state": "ZERO_IMPEDANCE", "logic": "SGL"}
    cosmit_shell = {"root": "HYBRID_NODE", "state": "RESONANCE", "logic": "SGL"}
    noisy_shell = {"root": "ENTROPY", "logic": "HEX_TECH"}
    
    # Put blobs with semantics
    h_void = akasha.put_with_semantics(b"SOVEREIGN_VOID_DNA", void_shell)
    h_cosmit = akasha.put_with_semantics(b"COSMIT_DNA", cosmit_shell)
    h_noise = akasha.put_with_semantics(b"NOISE", noisy_shell)
    
    print(f"   Void Hash:   {h_void[:16]}...")
    print(f"   Cosmit Hash: {h_cosmit[:16]}...")
    
    # Calculate resonance
    res_vc = akasha._calculate_vector_resonance(void_shell, cosmit_shell)
    res_vn = akasha._calculate_vector_resonance(void_shell, noisy_shell)
    
    print(f"   Void <-> Cosmit Resonance: {res_vc:.4f} (Expected ~0.2)")
    print(f"   Void <-> Noise Resonance:  {res_vn:.4f} (Expected ~0.25)")
    
    # Find by resonance
    matches = akasha.find_by_resonance({"logic": "SGL"}, threshold=0.1)
    print(f"   Search for 'logic: SGL' found {len(matches)} matches.")
    
    if len(matches) >= 2:
        print("✅ SEMANTIC RESONANCE VERIFIED.")
    else:
        print("❌ SEMANTIC RESONANCE FAILED.")

if __name__ == "__main__":
    test_semantic_resonance()
