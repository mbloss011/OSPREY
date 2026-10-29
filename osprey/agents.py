"""OSPREY swarm roles — defensive only, mirroring CADENCE's fleet idea
(1 coordinator + workers) and Sentinel's role split.

director: singleton, decomposes an incident into worker tasks.
scout: maps ONLY the enrolled site's own surface (headers, forms, routes).
triage: small-model, high-volume sorting + enrichment (geo/ASN/intel lookup).
analyst: reads evidence, writes the incident picture.
forensics: evidence + webshell/signature scan of enrolled docroots.
hardening: proposes config/WAF patches; never applies A2+ without approval.
reader: TOOL-LESS — the only role allowed to read quarantined text.
coder: writes patches in a sandbox; publish only after lab validation.
validator: runs the lab/verify commands, reports pass/fail.
watcher: read-only observer with its own kill-switch view.
"""
from __future__ import annotations
from dataclasses import dataclass

ROLES = ["director", "scout", "triage", "analyst", "forensics",
         "hardening", "reader", "coder", "validator", "watcher"]

@dataclass
class AgentCard:
    role: str
    tools: tuple[str, ...] = ()
    toolless: bool = False
    scale_to_zero: bool = False

CARDS = {
    "director": AgentCard("director", ("task.publish", "memory.query"), False, False),
    "scout": AgentCard("scout", ("webshield.scan",), False, False),
    "triage": AgentCard("triage", ("intel.lookup", "enrich.geoip"), False, False),
    "analyst": AgentCard("analyst", ("evidence.read", "memory.query"), False, False),
    "forensics": AgentCard("forensics", ("evidence.get", "webshell.scan"), False, True),
    "hardening": AgentCard("hardening", ("config.diff", "patch.propose"), False, True),
    "reader": AgentCard("reader", (), True, False),
    "coder": AgentCard("coder", ("patch.write", "lab.submit", "verify.run"), False, False),
    "validator": AgentCard("validator", ("lab.submit", "lab.result"), False, False),
    "watcher": AgentCard("watcher", ("read_only", "kill_switch"), False, False),
}
