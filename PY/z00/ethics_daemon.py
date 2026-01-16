from daemon_core import BaseDaemon
from ethics_engine import EthicsEngine, TruthLayer, RealityPacket
from gaia_grid import GaiaGrid
from kml_generator import KMLGenerator
import os
import ast
import time

class EthicsDaemon(BaseDaemon):
    """Journal -> Concord: The Pulse of Discernment."""
    MAX_ENERGY_PER_CYCLE = 5.0 # V73.8 Homeostasis limit

    def __init__(self, name: str):
        super().__init__(name)
        self.engine = EthicsEngine()
        self.grid = GaiaGrid()
        self.kml = KMLGenerator()

    def run_once(self):
        journal_files = self.scan_channel("journal")
        spores_to_process = []
        
        # 1. First pass: Parse and calculate current energy
        for fpath, mtime in journal_files:
            with open(fpath, "r") as f:
                content = f.read()

            links = {}
            if "geo_trace:" in content:
                val = content.split("geo_trace:")[1].split("\n")[0].strip()
                try: links["geo_trace"] = ast.literal_eval(val)
                except: links["geo_trace"] = val
            elif "GEO:" in content:
                links["geo_trace"] = content.split("GEO:")[1].split("\n")[0].strip()

            if "geo_claim:" in content:
                links["geo_claim"] = content.split("geo_claim:")[1].split("\n")[0].strip()
            elif "GEO_MODEL:" in content:
                links["geo_claim"] = content.split("GEO_MODEL:")[1].split("\n")[0].strip()
            
            sigma_id = (0, "sea", "void", "global")
            if "ΣID:" in content:
                val = content.split("ΣID:")[1].split("\n")[0].strip()
                sigma_id = ast.literal_eval(val)

            packet = RealityPacket(
                content=content,
                layer=TruthLayer.TRACE if any(x in content for x in ["TRACE", "GEO:", "geo_trace:"]) else TruthLayer.MODEL,
                sigma_id=sigma_id,
                links=links
            )
            
            if packet.discrepancy:
                # Apply V73.8 Decay
                packet.apply_metabolic_decay(time.time())
                spores_to_process.append((fpath, mtime, packet))
        
        # 2. Sort by Energy (Highest First)
        spores_to_process.sort(key=lambda x: x[2].discrepancy.get("energy", 0), reverse=True)
        
        # 3. Process within Energy Budget
        current_energy = 0
        for fpath, mtime, packet in spores_to_process:
            energy = packet.discrepancy.get("energy", 0)
            if current_energy + energy > self.MAX_ENERGY_PER_CYCLE:
                print(f"⚠️ Ethics: Energy budget exceeded ({current_energy:.2f}/{self.MAX_ENERGY_PER_CYCLE}). Deferring {os.path.basename(fpath)}")
                continue
            
            current_energy += energy
            fname = os.path.basename(fpath)
            attention = packet.discrepancy.get("attention", 0)
            
            # Lattice Reference Pattern (V73.7)
            target_sub = "review" if attention > 0.7 else "open"
            target_path = os.path.join(self.bus_root, "concord", target_sub, fname)
            
            ref_content = f"REF: journal/{fname}\n"
            ref_content += f"DIGEST: {packet.digest}\n"
            ref_content += f"DISCREPANCY: {packet.discrepancy}\n"
            ref_content += f"ATTENTION_EXP: {time.time() + 3600}\n"
            
            with open(target_path, "w") as f:
                f.write(ref_content)
            
            print(f"⚡️ Ethics: [REF:{target_sub.upper()}] E:{energy:.2f} -> {fname}")
            
            # Log with Metadata
            meta = {"hotspot": f"cell:{packet.sigma_id[2]}", "has_trace": packet.layer == TruthLayer.TRACE}
            self.log_flow_metric(f"concord/{target_sub}", 1, metadata=meta)
            self._set_checkpoint("journal", mtime)

        self.log_flow_metric("journal", 0)

if __name__ == "__main__":
    d = EthicsDaemon("Ethics")
    d.run_once()
