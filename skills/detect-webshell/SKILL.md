---
name: detect-webshell
description: Hunt for web-shell footholds in an enrolled docroot — new files, upload-form outputs, and known shell patterns.
---
1. Diff the file inventory against the last known-good inventory.
2. Scan added/changed files for shell patterns; quarantine (read-only, tool-less reader) for review.
3. Never delete or execute a suspect file automatically — that is A4 territory.
