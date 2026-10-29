"""Action classes A0-A4, borrowed in concept from the Sentinel blueprint.

A0 observe: auto. A1 reversible+narrow (TTL block, rate-limit, tarpit):
auto only if risk score high and collateral low. A2 reversible+broad
(WAF rule, geo block): approval or canary + auto-rollback. A3 intrusive
(upgrade, restart, sysctl): approval + window + rollback plan.
A4 destructive/irreversible (isolate, key rotation, wipe):
two-person, never auto.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

class ActionClass(str, Enum):
    A0 = "A0"; A1 = "A1"; A2 = "A2"; A3 = "A3"; A4 = "A4"

@dataclass
class Proposal:
    action_class: ActionClass
    description: str
    p_malicious: float = 0.0
    expected_collateral: float = 0.0
    approved: bool = False
    def auto_allowed(self) -> bool:
        if self.action_class == ActionClass.A0:
            return True
        if self.action_class == ActionClass.A1:
            return self.p_malicious >= 0.9 and self.expected_collateral <= 0.01
        return False
    def needs_approval(self) -> bool:
        return not self.auto_allowed()
