import unittest
from src.core import div_round_half_up, clamp_i16, SigmaNodeV1, WaveVectorQ
from src.interference import interfere

class TestSigmaCore(unittest.TestCase):
    def test_div_round_half_up(self):
        # ... existing ...
        self.assertEqual(div_round_half_up(10, 3), 3)
        self.assertEqual(div_round_half_up(11, 3), 4)
        self.assertEqual(div_round_half_up(5, 2), 3)
        self.assertEqual(div_round_half_up(-5, 2), -3)
        self.assertEqual(div_round_half_up(0, 5), 0)
        self.assertEqual(div_round_half_up(-32768, 1), -32768)

    def test_serialization(self):
        # Create a mock node
        atom = b"\x00" * 32
        wave = WaveVectorQ(8192, 65535, -32768)
        node = SigmaNodeV1(0x00, 0x01, wave, atom=atom)
        
        packed = node.pack()
        self.assertEqual(len(packed), 8 + 32)
        
        unpacked = SigmaNodeV1.unpack(packed)
        self.assertEqual(unpacked.op, 0)
        self.assertEqual(unpacked.wave.ph, 8192)
        self.assertEqual(unpacked.atom, atom)

    def test_interference(self):
        # I (0, 65535, -32768) and K (32768, 65535, -32768)
        # Delta = 32768, Resonance = -32767
        # amp_factor = ((-32767 + 32767) * 65535) / 65534 = 0
        w1 = WaveVectorQ(0, 65535, -32768)
        w2 = WaveVectorQ(32768, 65535, -32768)
        
        res = interfere(w1, w2)
        self.assertEqual(res.ph, 0)
        self.assertEqual(res.am, 0)
        self.assertEqual(res.en, -32768)
        
        # Self-interference (In-phase)
        # Delta = 0, Resonance = 32767
        # amp_factor = ((32767 + 32767) * 65535) / 65534 = 65535
        # new_am = 65535 * 65535 / 65535 = 65535
        res_self = interfere(w1, w1)
        self.assertEqual(res_self.am, 65535)

if __name__ == "__main__":
    unittest.main()
