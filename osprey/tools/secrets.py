"""Secret-pattern scan of text you own (own repo/docroot/config).

Findings are reported, never exfiltrated. Mirrors the TruffleHog lesson
from the Cairn panels: exposed panels leaked hundreds of secrets, 11%
still valid — so scan your own surface before an attacker does.
"""
from __future__ import annotations
import re
PATTERNS = {
    "aws_key": r"AKIA[0-9A-Z]{16}",
    "generic_api_key": r"(?i)(api[_-]?key|secret)\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}['\"]",
    "private_key_block": r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
    "bearer": r"Bearer [A-Za-z0-9_\-\.]{20,}",
}
def scan_text(text: str) -> list[str]:
    return [name for name, pat in PATTERNS.items() if re.search(pat, text)]
