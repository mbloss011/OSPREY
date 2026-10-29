---
name: write-waf-rule
description: Write a narrow, reversible WAF rule for an observed attack pattern on an enrolled site, with TTL and auto-rollback.
---
1. Name the exact pattern (path, parameter, payload shape) from enrolled-site evidence only.
2. Write the narrowest rule that blocks it, with a TTL. Broad ASN/geo blocks are A2 and need approval or canary.
3. Log matches for 24h before widening. Roll back on false positives.
