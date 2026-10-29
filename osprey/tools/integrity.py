"""File-integrity for enrolled docroots: hash, inventory, spot the new file.

A web-shell foothold usually arrives as a NEW file in an unexpected
directory, not as an edit to a known file. This inventories a docroot
and diffs it against a prior inventory.
"""
from __future__ import annotations
import hashlib, json
from pathlib import Path

def inventory(docroot: str | Path) -> dict[str, str]:
    out = {}
    for p in sorted(Path(docroot).rglob("*")):
        if p.is_file():
            out[str(p.relative_to(docroot))] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out

def diff_inventories(old: dict, new: dict) -> dict:
    return {"added": sorted(set(new) - set(old)),
            "removed": sorted(set(old) - set(new)),
            "changed": sorted(k for k in set(old) & set(new) if old[k] != new[k])}
