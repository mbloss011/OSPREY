# OSPREY architecture (v0.1, rebuilt from scratch)

Guide, not copy: CADENCE supplies the shape — local-first Python, OpenAI-compatible
LLM adapter (LM Studio default, mock mode), skills as folders (agentskills.io layout),
loopback-only web, bearer token, sandbox verify commands, fleet coordinator+workers.
The Sentinel tarball supplies the defensive tools — enrollment charter, A0-A4 action
classes, kill switch, hash-chained audit, decision layers (guardrails -> SSVC-style
triage -> risk score), and a validation lab gate before any patch is published.

```
enrolled site/host
  -> scout (own surface) -> triage (small model + rules) -> analyst
  -> forensics / hardening / coder (sandbox, verify commands)
  -> validator (lab pass required) -> proposal (A0-A4)
  -> decision: auto (A0 / A1-if-thresholds) | approval | canary | two-person (A4)
  -> action + hash-chained audit + kill-switch check at every step
```

v0.1 ships: charter, config, LLM adapter + mock, A0-A4, audit ledger, kill switch,
10 agent cards, webshield tools (headers, upload forms, Magento CVE-2026-75650,
exposed-panel check, webshell patterns), integrity diff, secret scan, loopback API,
CLI, 5 skills, 11 tests. No network scanning, no XDP, no NATS — those are Phase 2
(Go edge agent + JetStream backbone, ported as a fresh implementation, not a copy).
