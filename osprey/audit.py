"""Hash-chained audit ledger: every proposal, verdict and action, append-only.

Each line carries sha256(prev_hash + payload) so a tampered line breaks
the chain. Verification is a pure function, no server needed.
"""
from __future__ import annotations
import hashlib, json
from pathlib import Path

def _h(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()

class AuditLedger:
    def __init__(self, path: str | Path):
        self.path = Path(path); self.path.parent.mkdir(parents=True, exist_ok=True)
    def append(self, event: dict) -> dict:
        prev = "GENESIS"
        if self.path.exists() and self.path.stat().st_size:
            prev = json.loads(self.path.read_text().strip().splitlines()[-1])["hash"]
        payload = json.dumps(event, sort_keys=True)
        rec = {"prev": prev, "event": event, "hash": _h(prev + payload)}
        with self.path.open("a") as f: f.write(json.dumps(rec) + "\n")
        return rec
    def verify(self) -> bool:
        prev = "GENESIS"
        if not self.path.exists(): return True
        for line in self.path.read_text().strip().splitlines():
            if not line: continue
            rec = json.loads(line)
            if rec["prev"] != prev: return False
            if rec["hash"] != _h(prev + json.dumps(rec["event"], sort_keys=True)): return False
            prev = rec["hash"]
        return True
