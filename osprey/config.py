"""Env-driven config, CADENCE-style: local-first, no hardcoded hosts/models."""
from __future__ import annotations
import os
from dataclasses import dataclass

@dataclass
class Config:
    lmstudio_base_url: str = os.environ.get("LMSTUDIO_BASE_URL", "http://127.0.0.1:1234/v1")
    big_model: str = os.environ.get("OSPREY_BIG_MODEL", "ornith-1.5-9b")
    small_model: str = os.environ.get("OSPREY_SMALL_MODEL", "liquid/lfm2-1.2b")
    api_token: str = os.environ.get("OSPREY_API_TOKEN", "")
    bind_host: str = "127.0.0.1"  # loopback only, like CADENCE
    bind_port: int = int(os.environ.get("OSPREY_PORT", "8775"))
    data_dir: str = os.environ.get("OSPREY_DATA_DIR", ".osprey")
    mock_llm: bool = os.environ.get("OSPREY_MOCK_LLM", "false").lower() == "true"
