# OSPREY threat model — what it defends against, and what it refuses to do

Source threats (Oct 2026 reporting, Trend Micro / NorForge / Microsoft):
- CyberStrikeAI: 44 agents automating recon -> vuln validation -> exploitation -> C2 -> persistence -> exfil -> reporting, in the target's language, with fake login pages. 19+ orgs validated in days.
- Cairn: autonomous agents vs 1,200+ sites, ~10% success, ~$5/task, web-shell uploader foothold, memcached session + PHP object + old Zend chains, exposed control panels leaking secrets.
- ARTEX: password spraying across 2,250+ M365 tenants, privileged persistence.
- AI phishing/intent: fluent, personalised, template-free lures; device-code phishing.

## OSPREY's defensive mapping
| Attack step | OSPREY defence (enrolled site only) |
|---|---|
| Mass recon / scanning | Rate-limit + tarpit (A1, TTL), header hardening, exposed-panel check |
| Vuln validation | Own-stack CVE triage skill, Magento CVE-2026-75650 hotfix check, patch-from-advisory (lab-validated) |
| Web-shell upload | Upload-form inventory, docroot integrity diff, webshell pattern scan, quarantine-not-delete |
| Session-store / PHP object abuse | Harden session store config, audit serialisation handling in own code |
| Fake login pages | Brand-impersonation watch for your own domains (report + takedown request, never retaliation) |
| Password spraying | Spray detection in own auth logs, lockout + MFA enforcement proposals |
| C2 / persistence | New-file / new-cron / new-service inventory diff on enrolled hosts |
| Exfiltration | Outbound-size anomaly proposals from own logs, audit ledger |
| Exposed agent panels | Panel check: login required, not public, not unauthed on :8000 |

## Hard refusals
- No scanning, probing, or exploitation of any host not in a signed charter.
- No auto A4 action. No offensive action against a third party, ever — including "retaliation" against an attacker.
- The LLM proposes; OPA-style guardrails + human approval dispose. Kill switch stops all new actions.
