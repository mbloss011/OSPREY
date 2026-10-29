"""Defense Charter: the enrollment boundary.

OSPREY acts only on sites/hosts listed in a charter the owner signed.
Anything not enrolled is out of scope, full stop. This is the direct
answer to agent swarms that spray thousands of unauthorised targets:
OSPREY's swarm never leaves its own fence.
"""
from __future__ import annotations
import json, re
from dataclasses import dataclass, field
from pathlib import Path

HOST_RE = re.compile(r"^(?=.{1,253}$)([a-z0-9-]+\.)+[a-z]{2,}$", re.I)
URL_RE = re.compile(r"^https?://[a-z0-9.-]+(:\d+)?(/.*)?$", re.I)

@dataclass
class Charter:
    owner: str
    hosts: list[str] = field(default_factory=list)
    docroots: list[str] = field(default_factory=list)
    signed_by: str = ""
    def is_enrolled_host(self, host: str) -> bool:
        h = host.lower().strip()
        return h in [x.lower() for x in self.hosts]
    def is_enrolled_url(self, url: str) -> bool:
        if not URL_RE.match(url or ""):
            return False
        host = url.split("://", 1)[1].split("/", 1)[0].split(":", 1)[0]
        return self.is_enrolled_host(host)
    def is_enrolled_path(self, path: str) -> bool:
        p = str(Path(path).resolve())
        return any(p == str(Path(d).resolve()) or p.startswith(str(Path(d).resolve()) + "/")
                   for d in self.docroots)
    @classmethod
    def from_file(cls, path: str | Path) -> "Charter":
        data = json.loads(Path(path).read_text())
        return cls(owner=data["owner"], hosts=data.get("hosts", []),
                   docroots=data.get("docroots", []), signed_by=data.get("signed_by", ""))
    def validate(self) -> list[str]:
        errs = []
        if not self.owner: errs.append("owner is required")
        if not self.signed_by: errs.append("signed_by is required — an unsigned charter enrols nothing")
        if not self.hosts and not self.docroots: errs.append("charter enrols no hosts or docroots")
        for h in self.hosts:
            if not HOST_RE.match(h): errs.append(f"invalid host: {h}")
        return errs
