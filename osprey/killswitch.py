"""Kill switch: global / tenant / host scope + local DISARM file.

Checked before any action. A disarmed host keeps its kernel-level
reflex (if any) but OSPREY issues no new actions for it.
"""
from __future__ import annotations
from pathlib import Path

class KillSwitch:
    def __init__(self, disarm_file: str | Path = "/etc/osprey/DISARM"):
        self.disarm_file = Path(disarm_file); self._killed: set[str] = set()
    def kill(self, scope: str): self._killed.add(scope)
    def clear(self, scope: str): self._killed.discard(scope)
    def is_killed(self, scope: str) -> bool:
        if self.disarm_file.exists(): return True
        return scope in self._killed or "global" in self._killed
