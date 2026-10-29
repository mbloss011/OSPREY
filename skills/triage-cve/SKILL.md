---
name: triage-cve
description: Triage a CVE against the enrolled stack only — affected version? exposed? exploitable? SSVC-style outcome: Track, Track*, Attend, Act.
---
1. Check the enrolled version, not the internet at large.
2. Score exploitation + exposure + mission impact + automatability.
3. Output a proposal with an action class (A0-A4), never an auto-fix for A2+.
