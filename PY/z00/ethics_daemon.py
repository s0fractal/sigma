from daemon_core import BaseDaemon
from ethics_engine import EthicsEngine, TruthLayer, RealityPacket
from gaia_grid import GaiaGrid
from kml_generator import KMLGenerator
import os
import ast

class EthicsDaemon(BaseDaemon):
    """Journal -> Concord: The Pulse of Discernment."""
    def __init__(self, name: str):
        super().__init__(name)
        self.engine = EthicsEngine()
        self.grid = GaiaGrid()
        self.kml = KMLGenerator()

    def run_once(self):
        journal_files = self.scan_channel("journal")
        for fpath, mtime in journal_files:
            print(f"🔮 EthicsDaemon: Scanning {os.path.basename(fpath)}")
            with open(fpath, "r") as f:
                content = f.read()

            # Parse for RealityPacket (V73.3 Canonical)
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
                # V73.6 Routing by Attention
                fname = os.path.basename(fpath)
                attention = packet.discrepancy.get("attention", 0)
                
                # High attention (> 0.7) goes to review sub-channel
                target_sub = "review" if attention > 0.7 else "open"
                concord_path = os.path.join(self.bus_root, "concord", target_sub, fname)
                
                with open(concord_path, "w") as f:
                    f.write(content + f"\nDISCREPANCY: {packet.discrepancy}")
                
                print(f"⚡️ EthicsDaemon: [{target_sub.upper()}] S:{packet.discrepancy['severity']:.2f} A:{attention:.2f} -> {fname}")
                
                # Log with Metadata (V73.6)
                meta = {
                    "hotspot": f"cell:{sigma_id[2]}",
                    "has_trace": packet.layer == TruthLayer.TRACE
                }
                self.log_flow_metric(f"concord/{target_sub}", 1, metadata=meta)
            
            self._set_checkpoint("journal", mtime)
            self.log_flow_metric("journal", 0)

if __name__ == "__main__":
    d = EthicsDaemon("Ethics")
    d.run_once()
