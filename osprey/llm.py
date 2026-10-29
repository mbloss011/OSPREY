"""OpenAI-compatible LLM adapter + deterministic mock (CADENCE pattern).

The LLM never sits in a packet path, never executes anything, and never
overrides a guardrail. It proposes; the decision engine disposes.
"""
from __future__ import annotations
from .config import Config

class MockLLM:
    def complete(self, prompt: str) -> str:
        return ("MOCK-ANALYSIS: triage the finding, propose only reversible, "
                "enrolled-host actions, and flag anything needing human approval.")

class OpenAICompatLLM:
    def __init__(self, cfg: Config):
        self.cfg = cfg
    def complete(self, prompt: str) -> str:
        # Lazy import so the mock path needs no extra deps.
        import httpx, json
        r = httpx.post(f"{self.cfg.lmstudio_base_url}/chat/completions",
                       json={"model": self.cfg.big_model,
                             "messages": [{"role": "user", "content": prompt}]},
                       timeout=60)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]

def get_llm(cfg: Config):
    return MockLLM() if cfg.mock_llm else OpenAICompatLLM(cfg)
