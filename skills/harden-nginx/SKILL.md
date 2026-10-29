---
name: harden-nginx
description: Harden nginx for an enrolled site — security headers, upload limits, and rate limits. Proposes config only; A2+ needs approval.
---
1. Confirm the site is in the signed Defense Charter. If not, refuse.
2. Draft the header block (HSTS, CSP, X-Content-Type-Options, Referrer-Policy) and client_max_body_size / upload restrictions.
3. Validate with `nginx -t` in the lab first. Never apply live without a rollback plan.
