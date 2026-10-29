# OSPREY

A defensive web-shield agent, rebuilt from scratch. CADENCE is the guide for how
an agent is shaped (local-first, skills-as-folders, fleet, sandbox, loopback web);
the Sentinel Swarm tarball is the guide for what it defends with (enrollment
charter, A0-A4 actions, kill switch, audit ledger, lab-validated patches).

**Main purpose:** protect *your own* websites from AI-agent attack swarms —
CyberStrikeAI-style 44-agent workflows, Cairn-style autonomous break-ins,
ARTEX-style password spraying — by hardening the doors they try, not by
becoming another swarm that knocks on other people's doors.

**Scope rule, non-negotiable:** OSPREY acts only on hosts and docroots listed
in a signed Defense Charter (`charter.example.json`). Anything else is refused.

## Quick start (mock mode, no model, no network scan)
```bash
pip install -e .
OSPREY_MOCK_LLM=true python3 -m osprey.cli doctor
python3 -m osprey.cli charter-check https://example.com --charter charter.example.json
python3 -m unittest discover -s tests -v
```

## What v0.1 does
- Charter enrolment + refusal of non-enrolled targets
- Security-header check, stray upload-form finder, Magento CVE-2026-75650 check
- Exposed agent-panel check (your own :8000-style panels)
- Webshell pattern scan + docroot integrity diff + secret-pattern scan
- A0-A4 proposal gating, hash-chained audit, kill switch, 10 defensive agent roles
- 5 skills: harden-nginx, write-waf-rule, triage-cve, detect-webshell, patch-from-advisory

## What it deliberately does NOT do
No unauthorised scanning, no exploitation, no auto destructive action, no
retaliation. Patches publish only after lab validation; A2+ needs approval.

See THREAT-MODEL.md for the CyberStrikeAI / Cairn / ARTEX mapping, and
ARCHITECTURE.md for the CADENCE + Sentinel lineage.
