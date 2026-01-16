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

    def log_flow_metric(self, channel: str, processed_count: int = 1):
        """Updates flow_state.json with throughput metrics."""
        fstate = os.path.join(self.bus_root, "flow_state.json")
        data = {"rates": {}, "backlog": {}}
        if os.path.exists(fstate):
            try:
                with open(fstate, "r") as f: data = json.load(f)
            except: pass
        
        # Update Rate (Counter)
        now = time.strftime("%Y-%m-%d %H:%M")
        channel_key = f"{self.name}:{channel}"
        data["rates"][channel_key] = data["rates"].get(channel_key, 0) + processed_count
        
        # Update Backlog Scan
        ch_path = os.path.join(self.bus_root, channel)
        if os.path.exists(ch_path):
            data["backlog"][channel] = len(os.listdir(ch_path))
            
        with open(fstate, "w") as f:
            json.dump(data, f, indent=4)

    def move_to(self, fpath: str, target_channel: str):
        """Atomic move between channels."""
        fname = os.path.basename(fpath)
        dest = os.path.join(self.bus_root, target_channel, fname)
        os.rename(fpath, dest)
        self.log_flow_metric(target_channel)
        return dest
