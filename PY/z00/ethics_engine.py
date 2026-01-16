from enum import Enum
from typing import Any, Dict, Optional, Tuple
import time
import hashlib

class TruthLayer(Enum):
    TRACE = "TRACE"   # Hard evidence, anchors, physical records
    MODEL = "MODEL"   # Logical deductions, calculations, code output
    MYTH = "MYTH"     # Intent, vision, poetry, interpretation
    ANOMALY = "ANOMALY" # Divergence from harmony (Was: VIRUS)

class RealityPacket:
    """A standardized impulse in the Lattice with V72.1 Discernment."""
    def __init__(self, content: str, layer: TruthLayer, sigma_id: Tuple[int, str, str, str], 
                 source: str = "unknown", links: Dict = None, geo_confidence: float = 0.0,
                 claim_type: str = "literal"):
        self.content = content
        self.layer = layer
        self.sigma_id = sigma_id # (T, S, C_self, F)
        self.source = source
        self.links = links or {} # {"geo": [List of (coord, weight)], "geo_model": "..."}
        self.geo_confidence = geo_confidence
        self.claim_type = claim_type # literal | symbolic | hearsay
        self.ts = time.time()
        self.digest = hashlib.sha256(f"{content}:{self.ts}".encode()).hexdigest()
        
        # Law Enforcement
        self.discrepancy = None
        
        # Multi-Trace Aggregation
        geo_traces = self.links.get("geo", [])
        if isinstance(geo_traces, str): # Backward compatibility
            geo_traces = [(geo_traces, 1.0)]
            self.links["geo"] = geo_traces

        # Mismatch Calculation (V72.1 Refined)
        if geo_traces and "geo_model" in self.links:
            # Calculate Cluster Center
            avg_lat, avg_lon, total_w = 0, 0, 0
            for coord, weight in geo_traces:
                lat, lon = [float(x) for x in coord.split(",")]
                avg_lat += lat * weight
                avg_lon += lon * weight
                total_w += weight
            
            center_lat, center_lon = avg_lat/total_w, avg_lon/total_w
            
            # Claim point
            m_lat, m_lon = [float(x) for x in self.links["geo_model"].split(",")]
            
            # Geodesic-ish distance
            dist = ((center_lat - m_lat)**2 + (center_lon - m_lon)**2)**0.5
            
            # Severity Logic
            severity = dist * (total_w / max(1, len(geo_traces)))
            if self.claim_type == "symbolic":
                severity *= 0.3 # Reduce pain for symbols
            
            if severity > 0.2: # Threshold
                self.discrepancy = {
                    "type": "ATTRIBUTION_MISMATCH",
                    "claim": self.links["geo_model"],
                    "trace_center": f"{center_lat},{center_lon}",
                    "severity": min(1.0, severity),
                    "status": "OPEN",
                    "claim_type": self.claim_type
                }
                print(f"🔮 Ethics: V72.1 Discrepancy -> {self.claim_type}:{severity:.2f}")

    def _generate_digest(self) -> str:
        # This method is no longer called by __init__ based on the provided snippet.
        # Its implementation needs to be updated to reflect the new attributes if it's still used elsewhere.
        # For now, I'll adapt it to the new attributes, assuming it might be called manually.
        data = f"{self.ts}:{self.layer.value}:{self.source}:{self.sigma_id}:{self.content}"
        return hashlib.sha256(data.encode()).hexdigest()

    def to_dict(self) -> dict:
        return {
            "content": self.content,
            "layer": self.layer.value,
            "source": self.source,
            "domain": self.domain,
            "ts": self.ts,
            "digest": self.digest
        }

class EthicsEngine:
    """Validated reality: Ensures claims are grounded in the appropriate layers."""
    def __init__(self):
        self.anchors: Dict[str, RealityPacket] = {} # Verified TRACE packets

    def ingest(self, packet: RealityPacket):
        """Standardizes a reality packet."""
        if packet.layer == TruthLayer.TRACE:
            self.anchors[packet.digest] = packet
            print(f"⚖️ Ethics: TRACE Anchor secured ({packet.digest[:8]})")
        else:
            print(f"⚖️ Ethics: {packet.layer.value} ingested from {packet.source}")

    def validate_conductance(self, value: float) -> str:
        """Sanity check for the R=0 (Zero Impedance) claim."""
        if value >= 1.0:
            return "⚠️ R=0 detected. Triggering SENSE_REQUEST for external verification (Antibiotic V69)."
        if value < 0.2:
            return "🔴 High Impedance: Ethics quarantine advised."
        return "🟢 Optimal Flow."

    def validate_claim(self, claim: RealityPacket) -> bool:
        """Validates if a claim is grounded (Ethics Rule)."""
        if claim.layer == TruthLayer.TRACE:
            return True # Traces are self-validating anchors
        
        if claim.layer == TruthLayer.MODEL:
            # Models must be deterministic (mock validation for now)
            return True
        
        if claim.layer == TruthLayer.MYTH:
            # Myths are valid if they don't overwrite Traces
            return True
        
        return False

    def check_discrepancy(self, p1: RealityPacket, p2: RealityPacket) -> Optional[dict]:
        """Detects friction between layers."""
        if p1.layer == TruthLayer.TRACE and p2.layer == TruthLayer.TRACE:
            if p1.content != p2.content:
                return {
                    "type": "TRACE_CONFLICT",
                    "severity": 1.0,
                    "msg": f"Two contradictory traces from {p1.source} and {p2.source}"
                }
        
        if p1.layer == TruthLayer.TRACE and p2.layer == TruthLayer.MYTH:
            # Note: Myth is interpreted as 'intent' or 'perception'
            # If myth claims a fact that contradicts trace, it's a discrepancy
            pass
            
        return None
