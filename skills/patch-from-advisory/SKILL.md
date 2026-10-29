---
name: patch-from-advisory
description: Turn a vendor advisory (e.g. Adobe hotfix for CVE-2026-75650) into a lab-validated patch proposal for an enrolled site.
---
1. Confirm the advisory applies to the enrolled version.
2. Build the patch in a sandbox, run verify commands, get a lab pass.
3. Publish the proposal only after lab validation. Human approves the live apply.
