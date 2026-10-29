"""Loopback-only HTTP API, stdlib only (no FastAPI dep in v0.1).

GET /health, GET /roles, POST /charter/check {url} — all local.
Bearer token required when OSPREY_API_TOKEN is set.
"""
from __future__ import annotations
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from .agents import ROLES
from .config import Config

def make_handler(cfg: Config, charter=None):
    class H(BaseHTTPRequestHandler):
        def log_message(self, *a): pass
        def _send(self, code, obj):
            b = json.dumps(obj).encode(); self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
        def do_GET(self):
            if self.path == "/health": return self._send(200, {"status": "ok", "version": "0.1.0"})
            if self.path == "/roles": return self._send(200, {"roles": ROLES})
            return self._send(404, {"detail": "not found"})
        def do_POST(self):
            if cfg.api_token and self.headers.get("Authorization") != f"Bearer {cfg.api_token}":
                return self._send(401, {"detail": "unauthorized"})
            n = int(self.headers.get("Content-Length", 0) or 0)
            body = json.loads(self.rfile.read(n) or b"{}")
            if self.path == "/charter/check" and charter is not None:
                return self._send(200, {"url": body.get("url", ""),
                                        "enrolled": charter.is_enrolled_url(body.get("url", ""))})
            return self._send(404, {"detail": "not found"})
    return H

def serve(cfg: Config, charter=None):
    HTTPServer((cfg.bind_host, cfg.bind_port), make_handler(cfg, charter)).serve_forever()
