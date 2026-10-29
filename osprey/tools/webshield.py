"""Web-shield checks for ENROLLED sites only.

These are pure functions over data you already own (headers, HTML you
fetched from your own site, a version string from your own install).
v0.1 deliberately does no live crawling of arbitrary URLs — the caller
must pass a Charter and the check refuses non-enrolled targets.
"""
from __future__ import annotations
import re
from ..charter import Charter

REQUIRED_HEADERS = ["strict-transport-security", "content-security-policy",
                    "x-content-type-options", "referrer-policy"]

def check_headers(headers: dict) -> list[dict]:
    low = {k.lower(): v for k, v in headers.items()}
    return [{"check": f"header:{h}", "status": "pass" if h in low else "fail",
             "detail": "present" if h in low else "missing — hardening proposal, not auto-fix"}
            for h in REQUIRED_HEADERS]

def find_upload_forms(html: str) -> list[dict]:
    """Stray upload forms are the foothold Cairn-style agents aim for."""
    forms = []
    for m in re.finditer(r"<form[^>]*>(.*?)</form>", html, re.I | re.S):
        tag = m.group(0)
        if 'type="file"' in tag.lower() or "type='file'" in tag.lower():
            act = re.search(r'action="([^"]*)"', tag, re.I)
            forms.append({"kind": "upload_form", "action": act.group(1) if act else "(same page)",
                          "advice": "inventory it: is this form intended, authed, and type/size-checked?"})
    return forms

def _ver_tuple(v: str):
    return tuple(int(x) for x in re.findall(r"\d+", v))

def check_magento(version: str) -> dict:
    """StyleSmuggler CVE-2026-75650: Adobe Commerce 2.4.4-2.4.9,
    Magento Open Source 2.4.6-2.4.9 need Adobe's hotfix."""
    v = _ver_tuple(version)
    affected = (2, 4, 4) <= v <= (2, 4, 9)
    return {"product": "magento/adobe-commerce", "version": version,
            "cve": "CVE-2026-75650", "affected": affected,
            "action": "apply Adobe hotfix + verify" if affected else "not in affected range"}

def check_exposed_panel(url: str, charter: Charter) -> dict:
    """Agent control panels (Cairn-style, often :8000) left open on your
    own host leak targets, findings and secrets. Refuses non-enrolled URLs."""
    if not charter.is_enrolled_url(url):
        return {"url": url, "status": "refused", "reason": "not enrolled in charter"}
    return {"url": url, "status": "check",
            "advice": "confirm this panel requires login, is not public, and is not on :8000 unauthed"}

WEBSHELL_PATTERNS = [r"eval\s*\(\s*\$_", r"base64_decode\s*\(\s*\$_", r"shell_exec\s*\(",
                     r"move_uploaded_file\s*\(\s*\$_FILES", r"preg_replace\s*\(.*\/e"]

def scan_text_for_webshell(text: str) -> list[str]:
    return [p for p in WEBSHELL_PATTERNS if re.search(p, text)]
