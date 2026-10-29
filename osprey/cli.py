"""osprey CLI: doctor, enroll-check, scan helpers, audit verify."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
from . import __version__
from .charter import Charter
from .config import Config
from .audit import AuditLedger
from .tools import webshield, integrity, secrets as secret_tools

def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="osprey")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("doctor")
    c = sub.add_parser("charter-check"); c.add_argument("url"); c.add_argument("--charter", required=True)
    s = sub.add_parser("headers"); s.add_argument("--json", required=True)
    w = sub.add_parser("webshell-scan"); w.add_argument("text")
    a = sub.add_parser("audit-verify"); a.add_argument("--file", required=True)
    args = p.parse_args(argv)
    if args.cmd == "doctor":
        cfg = Config(); print(f"osprey {__version__} | mock_llm={cfg.mock_llm} | bind={cfg.bind_host}:{cfg.bind_port} (loopback) | models big={cfg.big_model} small={cfg.small_model}")
        return 0
    if args.cmd == "charter-check":
        ch = Charter.from_file(args.charter); errs = ch.validate()
        if errs: print("charter invalid:", "; ".join(errs)); return 2
        print(json.dumps({"url": args.url, "enrolled": ch.is_enrolled_url(args.url)})); return 0
    if args.cmd == "headers":
        print(json.dumps(webshield.check_headers(json.loads(args.json)), indent=2)); return 0
    if args.cmd == "webshell-scan":
        print(json.dumps({"matches": webshield.scan_text_for_webshell(args.text)})); return 0
    if args.cmd == "audit-verify":
        print(json.dumps({"valid": AuditLedger(args.file).verify()})); return 0
    return 2

if __name__ == "__main__":
    sys.exit(main())
