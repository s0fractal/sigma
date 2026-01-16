import os
import json
import time
import hashlib
from typing import Dict, List, Optional

class BaseDaemon:
    """The metabolic core for all SIGMA Workers (Daemons)."""
    def __init__(self, name: str, bus_root: str = "/Users/s0fractal/SIGMA/bus"):
        self.name = name
        self.bus_root = bus_root
        self.checkpoint_file = os.path.join(bus_root, "checkpoint.json")

    def _get_checkpoint(self, channel: str) -> int:
        if not os.path.exists(self.checkpoint_file):
            return 0
        with open(self.checkpoint_file, "r") as f:
            data = json.load(f)
            return data.get(channel, 0)

    def _set_checkpoint(self, channel: str, offset: int):
        data = {}
        if os.path.exists(self.checkpoint_file):
            with open(self.checkpoint_file, "r") as f:
                data = json.load(f)
        data[channel] = offset
        with open(self.checkpoint_file, "w") as f:
            json.dump(data, f, indent=4)

    def scan_channel(self, channel: str):
        """Scans a channel for new files based on checkpoint mtime."""
        channel_path = os.path.join(self.bus_root, channel)
        if not os.path.exists(channel_path):
            return []
        
        last_mtime = self._get_checkpoint(channel)
        files = []
        for f in os.listdir(channel_path):
            fpath = os.path.join(channel_path, f)
            mtime = os.path.getmtime(fpath)
            if mtime > last_mtime:
                files.append((fpath, mtime))
        
        # Sort by mtime to ensure sequential processing
        files.sort(key=lambda x: x[1])
        return files

    def run_once(self):
        """Standard work cycle. Override in subclass."""
        raise NotImplementedError("Daemons must implement run_once()")

    def log_flow_metric(self, channel: str, processed_count: int = 1, metadata: dict = None):
        """Updates flow_state.json with throughput, hotspots, and coverage."""
        fstate = os.path.join(self.bus_root, "flow_state.json")
        data = {"rates": {}, "backlog": {}, "hotspots": [], "coverage": 0.0}
        if os.path.exists(fstate):
            try:
                with open(fstate, "r") as f: 
                    loaded = json.load(f)
                    data.update(loaded)
            except: pass
        
        # Ensure V73.6 keys exist even if loading from legacy JSON
        if "hotspots" not in data: data["hotspots"] = []
        if "coverage" not in data: data["coverage"] = 0.0
        if "rates" not in data: data["rates"] = {}
        if "backlog" not in data: data["backlog"] = {}
        
        # Update Rate (Counter)
        channel_key = f"{self.name}:{channel}"
        data["rates"][channel_key] = data["rates"].get(channel_key, 0) + processed_count
        
        # Update Backlog Scan
        ch_path = os.path.join(self.bus_root, channel)
        if os.path.exists(ch_path):
            data["backlog"][channel] = len(os.listdir(ch_path))
        
        # Metadata context (Hotspots/Coverage)
        if metadata:
            if "hotspot" in metadata:
                if metadata["hotspot"] not in data["hotspots"]:
                    data["hotspots"].append(metadata["hotspot"])
                    data["hotspots"] = data["hotspots"][-5:] # Keep top 5
            if "has_trace" in metadata:
                # Weighted moving average for coverage
                prev_cov = data.get("coverage", 0.0)
                is_trace = 1.0 if metadata["has_trace"] else 0.0
                data["coverage"] = (prev_cov * 0.9) + (is_trace * 0.1)
            
        with open(fstate, "w") as f:
            json.dump(data, f, indent=4)

    def move_to(self, fpath: str, target_channel: str):
        """Atomic move between channels."""
        fname = os.path.basename(fpath)
        dest = os.path.join(self.bus_root, target_channel, fname)
        os.rename(fpath, dest)
        self.log_flow_metric(target_channel)
        return dest
